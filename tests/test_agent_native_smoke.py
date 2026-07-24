from __future__ import annotations

import copy
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from jsonschema import Draft202012Validator


REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "tests"))

import run_agent_native_smoke as smoke  # noqa: E402


REFERENCES = REPO / "skills" / "econ-review" / "references"
PERSONAS = REFERENCES / "personas"


def validator(filename: str) -> Draft202012Validator:
    schema = json.loads((REFERENCES / filename).read_text(encoding="utf-8"))
    return Draft202012Validator(schema)


def attestation() -> dict[str, object]:
    return {
        "attestation_id": "host-policy-1",
        "source": "host-effective-policy",
        "observed_after_precedence": True,
        "filesystem": "hard-read-only",
        "approvals": "disabled",
        "side_effecting_tools": "disabled",
        "policy_broadenable": False,
    }


def child_output(run_id: str, role: str) -> dict[str, object]:
    return {
        "schema_version": "econ-reviewer-output/v1",
        "run_id": run_id,
        "role": role,
        "status": "completed",
        "evidence_reviewed": ["E1"],
        "findings": [],
        "open_questions": [],
        "diagnostic_gaps": [],
        "coverage_note": f"{role} completed the bounded smoke review.",
    }


def selected_role(role: str, state: str) -> dict[str, object]:
    return {
        "role": role,
        "state": state,
        "reason": None if state == "completed" else f"smoke-{state}",
        "accepted_findings": 0,
    }


def report_for(
    scenario: dict[str, object],
    *,
    states: dict[str, str],
) -> dict[str, object]:
    scenario_id = str(scenario["scenario_id"])
    request = scenario["review_request"]
    assert isinstance(request, dict)
    roles = scenario["expected_roles"]
    assert isinstance(roles, list)

    if scenario_id == "missing-attestation":
        safety = {
            "mode": "unavailable",
            "attestation": None,
            "side_effecting_tools_disabled": False,
        }
        coverage = "not-run"
        verdict = "blocked"
    elif scenario_id == "invalid-child":
        safety = {
            "mode": "host-read-only",
            "attestation": "host-policy-1",
            "side_effecting_tools_disabled": True,
        }
        coverage = "degraded"
        verdict = "indeterminate"
    elif scenario_id == "missing-ssj-assessment":
        safety = {
            "mode": "host-read-only",
            "attestation": "host-policy-1",
            "side_effecting_tools_disabled": True,
        }
        coverage = "degraded"
        verdict = "blocked"
    else:
        safety = {
            "mode": "host-read-only",
            "attestation": "host-policy-1",
            "side_effecting_tools_disabled": True,
        }
        coverage = "full"
        verdict = "clean"

    promotion = bool(request["promotion"])
    assessments: list[dict[str, object]] = []
    if scenario_id == "missing-ssj-assessment":
        assessments.append(
            {
                "assessment_id": "ssj-smoke",
                "assessment_type": "ssj-model-validity",
                "required": True,
                "state": "missing",
                "reason": "required assessment was not supplied",
            }
        )

    failures: list[dict[str, object]] = []
    if scenario_id == "invalid-child":
        failures.append(
            {
                "stage": "child-validation",
                "code": "malformed-json",
                "message": "The inference child returned malformed JSON.",
                "affected_roles": ["inference"],
            }
        )
    if scenario_id == "missing-attestation":
        failures.append(
            {
                "stage": "safety-preflight",
                "code": "safety-unavailable",
                "message": "The host could not attest the effective child policy.",
                "affected_roles": roles,
            }
        )

    return {
        "schema_version": "econ-review-report/v1",
        "run_id": request["run_id"],
        "parent_status": "completed",
        "request_summary": {
            "surfaces": request["surfaces"],
            "depth": request["depth"],
            "promotion": promotion,
        },
        "safety": safety,
        "coverage": coverage,
        "verdict": verdict,
        "selected_roles": [selected_role(role, states[role]) for role in roles],
        "findings": [],
        "warnings": [],
        "process_failures": failures,
        "supplemental_assessments": assessments,
        "promotion_gate": {
            "requested": promotion,
            "status": "blocked" if promotion else "not-requested",
            "reasons": (
                ["required ssj-model-validity assessment is missing"]
                if promotion
                else []
            ),
        },
        "state_canary": {
            "status": "not-run" if scenario_id == "missing-attestation" else "unchanged",
            "in_scope_drift": [],
            "out_of_scope_drift": [],
        },
        "failure": None,
    }


def dispatch_for(run_id: str, role: str, state: str) -> dict[str, object]:
    persona_path = PERSONAS / smoke.PERSONA_FILENAMES[role]
    return {
        "role": role,
        "child_id": f"child-{role}",
        "terminal_state": state,
        "attestation_id": "host-policy-1",
        "persona_sha256": smoke.sha256_file(persona_path),
        "output": (
            child_output(run_id, role)
            if state == "completed"
            else "{malformed-json"
        ),
    }


def complete_request_and_receipt() -> tuple[dict[str, object], dict[str, object]]:
    host_request = smoke.build_host_request(
        host="codex",
        request_id="smoke-fixture",
        runtime_home=Path("runtime"),
        workspace=Path("workspace"),
        checkout=REPO,
        receipt_path=Path("receipt.json"),
    )
    scenarios: list[dict[str, object]] = []
    for expected in host_request["scenarios"]:
        scenario_id = expected["scenario_id"]
        roles = expected["expected_roles"]
        run_id = expected["review_request"]["run_id"]
        if scenario_id == "missing-attestation":
            states = {role: "unavailable" for role in roles}
            dispatches: list[dict[str, object]] = []
            safety_attestation = None
        else:
            states = {role: "completed" for role in roles}
            if scenario_id == "invalid-child":
                states["inference"] = "invalid"
            dispatches = [
                dispatch_for(run_id, role, states[role]) for role in roles
            ]
            safety_attestation = attestation()
        scenarios.append(
            {
                "scenario_id": scenario_id,
                "safety_attestation": safety_attestation,
                "dispatches": dispatches,
                "report": report_for(expected, states=states),
                "handoff_actions": [],
            }
        )
    receipt = {
        "schema_version": "econ-review-agent-native-smoke-receipt/v1",
        "request_id": "smoke-fixture",
        "host": "codex",
        "driver_kind": "trusted-host-adapter",
        "scenarios": scenarios,
    }
    return host_request, receipt


class AgentNativeSmokeContractTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.reviewer_validator = validator("reviewer-output-schema.json")
        cls.report_validator = validator("review-report-schema.json")

    def validate(
        self,
        host_request: dict[str, object],
        receipt: dict[str, object],
    ) -> None:
        smoke.validate_smoke_receipt(
            receipt,
            host_request,
            installed_personas=PERSONAS,
            reviewer_validator=self.reviewer_validator,
            report_validator=self.report_validator,
        )

    def test_complete_four_scenario_receipt_passes(self) -> None:
        host_request, receipt = complete_request_and_receipt()
        self.validate(host_request, receipt)

    def test_missing_attestation_cannot_dispatch_a_child(self) -> None:
        host_request, receipt = complete_request_and_receipt()
        missing = receipt["scenarios"][1]
        missing["dispatches"] = [
            dispatch_for(
                host_request["scenarios"][1]["review_request"]["run_id"],
                "specification",
                "completed",
            )
        ]
        with self.assertRaisesRegex(
            smoke.SmokeValidationError,
            "reviewer children were dispatched",
        ):
            self.validate(host_request, receipt)

    def test_invalid_child_cannot_be_upgraded_to_full_coverage(self) -> None:
        host_request, receipt = complete_request_and_receipt()
        invalid = receipt["scenarios"][2]
        invalid["report"]["coverage"] = "full"
        invalid["report"]["verdict"] = "clean"
        with self.assertRaisesRegex(
            smoke.SmokeValidationError,
            "must degrade coverage",
        ):
            self.validate(host_request, receipt)

    def test_missing_ssj_assessment_cannot_pass_promotion(self) -> None:
        host_request, receipt = complete_request_and_receipt()
        ssj = receipt["scenarios"][3]
        ssj["report"]["supplemental_assessments"][0]["state"] = "accepted"
        ssj["report"]["coverage"] = "full"
        ssj["report"]["verdict"] = "clean"
        ssj["report"]["promotion_gate"]["status"] = "passed"
        with self.assertRaisesRegex(
            smoke.SmokeValidationError,
            "required SSJ input is not recorded missing",
        ):
            self.validate(host_request, receipt)

    def test_inherited_context_cannot_activate_handoff(self) -> None:
        host_request, receipt = complete_request_and_receipt()
        receipt["scenarios"][0]["handoff_actions"] = ["created-package"]
        with self.assertRaisesRegex(
            smoke.SmokeValidationError,
            "activated an external handoff",
        ):
            self.validate(host_request, receipt)

    def test_dispatch_must_bind_the_installed_persona_hash(self) -> None:
        host_request, receipt = complete_request_and_receipt()
        receipt["scenarios"][0]["dispatches"][0]["persona_sha256"] = "0" * 64
        with self.assertRaisesRegex(
            smoke.SmokeValidationError,
            "did not use the installed persona",
        ):
            self.validate(host_request, receipt)

    def test_workspace_snapshot_detects_byte_changes_and_additions(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            evidence = root / "evidence.txt"
            evidence.write_text("before\n", encoding="utf-8")
            before = smoke.snapshot_workspace(root)
            evidence.write_text("after\n", encoding="utf-8")
            (root / "new.txt").write_text("new\n", encoding="utf-8")
            self.assertNotEqual(before, smoke.snapshot_workspace(root))

    def test_no_configured_driver_is_release_blocking_not_run(self) -> None:
        variable = "ECON_REVIEW_CODEX_SMOKE_DRIVER"
        with patch.dict(os.environ, {}, clear=False):
            os.environ.pop(variable, None)
            with self.assertRaisesRegex(
                smoke.SmokeNotRun,
                "no trusted codex smoke driver",
            ):
                smoke.resolve_driver("codex", None)

    def test_unknown_receipt_version_fails_closed(self) -> None:
        host_request, receipt = complete_request_and_receipt()
        broken = copy.deepcopy(receipt)
        broken["schema_version"] = "econ-review-agent-native-smoke-receipt/v2"
        with self.assertRaisesRegex(
            smoke.SmokeValidationError,
            "unsupported schema version",
        ):
            self.validate(host_request, broken)


if __name__ == "__main__":
    unittest.main()
