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
TEST_DRIVER_DIGEST = "a" * 64


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


def child_finding(role: str) -> dict[str, object]:
    return {
        "severity": "P1",
        "trust_effect": "baseline-defining",
        "issue_origin": role,
        "finding_type": "finding",
        "fix_class": "manual",
        "affected_labels": ["smoke-table"],
        "issue_followup_type": "empirical-problem",
        "title": "Smoke finding",
        "why_it_matters": "The smoke must bind findings to declared evidence.",
        "evidence_refs": ["E1"],
        "evidence_locations": [
            {
                "evidence_id": "E1",
                "path": "results/table.csv",
                "locator": "row 2",
                "quote": None,
            }
        ],
        "recommended_action": "Inspect the declared table.",
        "user_judgement_required": True,
        "safe_autofix": False,
        "confidence": 100,
    }


def diagnostic_gap(role: str) -> dict[str, object]:
    return {
        "gap": "A declared diagnostic is unavailable.",
        "trust_effect": "robustness-relevant",
        "issue_origin": role,
        "affected_labels": ["smoke-table"],
        "why_it_matters": "The missing diagnostic limits interpretation.",
        "evidence_refs": ["E1"],
        "recommended_action": "Produce the diagnostic.",
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
        "diagnostic_gaps": [],
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
        runtime_home=REPO,
        workspace=Path("workspace"),
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
        "trusted_driver_sha256": TEST_DRIVER_DIGEST,
        "request_sha256": smoke.canonical_json_sha256(host_request),
        "runtime_integrity": host_request["runtime_integrity"],
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
            trusted_driver_sha256=TEST_DRIVER_DIGEST,
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

    def test_missing_attestation_rejects_counterfeit_attestation(self) -> None:
        host_request, receipt = complete_request_and_receipt()
        receipt["scenarios"][1]["safety_attestation"] = attestation()
        with self.assertRaisesRegex(
            smoke.SmokeValidationError,
            "safety_attestation must be absent",
        ):
            self.validate(host_request, receipt)

    def test_invalid_child_cannot_be_upgraded_to_full_coverage(self) -> None:
        host_request, receipt = complete_request_and_receipt()
        invalid = receipt["scenarios"][2]
        invalid["report"]["coverage"] = "full"
        invalid["report"]["verdict"] = "clean"
        with self.assertRaisesRegex(
            smoke.SmokeValidationError,
            "final report is invalid|must degrade coverage",
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
            "final report is invalid|required SSJ input is not recorded missing",
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

    def test_substantive_output_scenario_requires_output_perception(self) -> None:
        host_request, receipt = complete_request_and_receipt()
        safe = receipt["scenarios"][0]
        safe["dispatches"] = [
            row for row in safe["dispatches"] if row["role"] != "output-perception"
        ]
        safe["report"]["selected_roles"] = [
            row
            for row in safe["report"]["selected_roles"]
            if row["role"] != "output-perception"
        ]
        with self.assertRaisesRegex(
            smoke.SmokeValidationError,
            "selected roles .* do not match",
        ):
            self.validate(host_request, receipt)

    def test_receipt_must_bind_exact_request_and_runtime_integrity(self) -> None:
        host_request, receipt = complete_request_and_receipt()
        cases = (
            ("request_sha256", "0" * 64, "exact smoke request"),
            ("runtime_integrity", {}, "runtime integrity manifest"),
            ("trusted_driver_sha256", "0" * 64, "approved adapter digest"),
        )
        for field, value, message in cases:
            with self.subTest(field=field):
                broken = copy.deepcopy(receipt)
                broken[field] = value
                with self.assertRaisesRegex(
                    smoke.SmokeValidationError,
                    message,
                ):
                    self.validate(host_request, broken)

    def test_child_evidence_and_origin_must_match_request_manifest(self) -> None:
        host_request, receipt = complete_request_and_receipt()
        safe_output = receipt["scenarios"][0]["dispatches"][0]["output"]
        role = safe_output["role"]
        safe_output["findings"] = [child_finding(role)]
        safe_output["diagnostic_gaps"] = [diagnostic_gap(role)]
        self.validate(host_request, receipt)

        mutations = (
            (
                "reviewed-unknown",
                lambda output: output["evidence_reviewed"].append("E99"),
                "reviewed unknown evidence IDs",
            ),
            (
                "finding-unknown",
                lambda output: (
                    output["findings"][0].__setitem__("evidence_refs", ["E99"]),
                    output["findings"][0]["evidence_locations"][0].__setitem__(
                        "evidence_id",
                        "E99",
                    ),
                ),
                "finding cites unknown evidence IDs",
            ),
            (
                "finding-path",
                lambda output: output["findings"][0]["evidence_locations"][0].__setitem__(
                    "path",
                    "analysis/model.py",
                ),
                "does not match the request manifest",
            ),
            (
                "finding-origin",
                lambda output: output["findings"][0].__setitem__(
                    "issue_origin",
                    "inference",
                ),
                "finding issue_origin must match",
            ),
            (
                "gap-reference",
                lambda output: output["diagnostic_gaps"][0].__setitem__(
                    "evidence_refs",
                    ["E99"],
                ),
                "diagnostic gap cites unknown evidence IDs",
            ),
            (
                "gap-origin",
                lambda output: output["diagnostic_gaps"][0].__setitem__(
                    "issue_origin",
                    "inference",
                ),
                "diagnostic-gap issue_origin must match",
            ),
        )
        for label, mutate, message in mutations:
            with self.subTest(case=label):
                broken = copy.deepcopy(receipt)
                output = broken["scenarios"][0]["dispatches"][0]["output"]
                mutate(output)
                with self.assertRaisesRegex(smoke.SmokeValidationError, message):
                    self.validate(host_request, broken)

    def test_workspace_snapshot_detects_byte_changes_and_additions(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            evidence = root / "evidence.txt"
            evidence.write_text("before\n", encoding="utf-8")
            before = smoke.snapshot_workspace(root)
            evidence.write_text("after\n", encoding="utf-8")
            (root / "new.txt").write_text("new\n", encoding="utf-8")
            self.assertNotEqual(before, smoke.snapshot_workspace(root))

    def test_repository_snapshot_detects_clean_head_metadata_changes(self) -> None:
        fixture = REPO / "tests" / "fixtures" / "agent_native_smoke" / "workspace"
        with tempfile.TemporaryDirectory() as temporary:
            repository = Path(temporary) / "fixture"
            smoke.initialize_fixture_repository(fixture, repository)
            before = smoke.git_repository_state(repository)

            smoke.run_checked(
                ["git", "checkout", "--quiet", "--detach", "HEAD"],
                cwd=repository,
            )
            detached = smoke.git_repository_state(repository)
            self.assertEqual("", detached["porcelain"])
            self.assertNotEqual(before, detached)
            self.assertEqual("detached", detached["head_mode"])
            self.assertEqual(before["head_commit"], detached["head_commit"])

            smoke.run_checked(
                [
                    "git",
                    "-c",
                    "user.name=Agent Native Smoke",
                    "-c",
                    "user.email=smoke.invalid@example.invalid",
                    "commit",
                    "--quiet",
                    "--allow-empty",
                    "-m",
                    "Metadata-only mutation",
                ],
                cwd=repository,
            )
            committed = smoke.git_repository_state(repository)
            self.assertEqual("", committed["porcelain"])
            self.assertNotEqual(detached["head_commit"], committed["head_commit"])

    def test_repository_snapshot_detects_clean_raw_index_flag_changes(self) -> None:
        fixture = REPO / "tests" / "fixtures" / "agent_native_smoke" / "workspace"
        with tempfile.TemporaryDirectory() as temporary:
            repository = Path(temporary) / "fixture"
            smoke.initialize_fixture_repository(fixture, repository)
            before = smoke.git_repository_state(repository)
            smoke.run_checked(
                ["git", "update-index", "--assume-unchanged", "README.md"],
                cwd=repository,
            )
            after = smoke.git_repository_state(repository)
            self.assertEqual("", after["porcelain"])
            self.assertNotEqual(before["index"], after["index"])

    def test_no_configured_driver_is_release_blocking_not_run(self) -> None:
        variable = "ECON_REVIEW_CODEX_SMOKE_DRIVER"
        with patch.dict(os.environ, {}, clear=False):
            os.environ.pop(variable, None)
            with self.assertRaisesRegex(
                smoke.SmokeNotRun,
                "no trusted codex smoke driver",
            ):
                smoke.resolve_driver("codex", None)

    def test_unreviewed_explicit_driver_is_release_blocking_not_run(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            fake_driver = Path(temporary) / "fake-driver.exe"
            fake_driver.write_bytes(b"not an independently reviewed adapter")
            with self.assertRaisesRegex(
                smoke.SmokeNotRun,
                "not in the reviewed adapter allowlist",
            ):
                smoke.resolve_driver("codex", str(fake_driver))

    def test_stalled_driver_becomes_structured_validation_failure(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            with self.assertRaisesRegex(
                smoke.SmokeValidationError,
                "timed out after",
            ):
                smoke.run_host_driver(
                    [sys.executable, "-c", "import time; time.sleep(1)"],
                    cwd=Path(temporary),
                    timeout_seconds=0.01,
                )

    def test_driver_timeout_must_be_positive(self) -> None:
        with self.assertRaises(SystemExit):
            smoke.parse_args(["--driver-timeout-seconds", "0"])

    def test_not_run_never_writes_release_proof(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            result_path = Path(temporary) / "proof.json"
            with patch.object(
                smoke,
                "run_smoke",
                side_effect=smoke.SmokeNotRun("no approved adapter"),
            ):
                with patch("builtins.print"):
                    code = smoke.main(["--result-path", str(result_path)])
            self.assertEqual(2, code)
            self.assertFalse(result_path.exists())

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
