from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator


REPO = Path(__file__).resolve().parents[1]
REFERENCES = REPO / "skills" / "econ-review" / "references"
FIXTURES = REPO / "tests" / "fixtures" / "reviewer_payloads"

SCHEMA_FILES = {
    "request": "review-request-schema.json",
    "reviewer": "reviewer-output-schema.json",
    "domain": "domain-assessment-schema.json",
    "report": "review-report-schema.json",
}
VERSIONS = {
    "request": "econ-review-request/v1",
    "reviewer": "econ-reviewer-output/v1",
    "domain": "econ-domain-assessment/v1",
    "report": "econ-review-report/v3",
}


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def valid_request() -> dict[str, Any]:
    triggers = {
        "provenance_risk": False,
        "sample_construction": False,
        "nontrivial_estimation": False,
        "inferential_claims": True,
        "substantive_outputs": True,
        "custom_implementation": False,
        "custom_changes_sample": False,
        "custom_changes_rerun": False,
        "custom_changes_outputs": False,
        "causal_design": False,
        "dynamic_objects": False,
        "robustness_hierarchy": False,
        "cross_software": False,
        "cross_language": False,
        "cross_language_data_construction": False,
        "cross_language_environment": False,
        "reproducibility": False,
        "bundle_target": False,
    }
    return {
        "schema_version": "econ-review-request/v1",
        "run_id": "fixture-run",
        "invocation": "direct",
        "caller": None,
        "resolution_context": None,
        "surfaces": ["empirical-results"],
        "depth": "standard",
        "promotion": False,
        "interpretation": True,
        "scope": {
            "target_paths": ["results/table.tex"],
            "authority_paths": ["analysis/model.py"],
            "base_ref": None,
            "blind_spots": [],
        },
        "evidence_manifest": [
            {
                "evidence_id": "E1",
                "path": "results/table.tex",
                "kind": "table",
                "description": "Canonical result table",
                "required": True,
            }
        ],
        "triggers": triggers,
        "timeout_policy": {"mode": "none", "seconds": None},
        "supplemental_assessments": [],
    }


def valid_domain_assessment() -> dict[str, Any]:
    return {
        "schema_version": "econ-domain-assessment/v1",
        "assessment_id": "domain-1",
        "assessment_type": "structural-model-validity",
        "subject": "Structural model implementation",
        "status": "complete",
        "producer": {
            "kind": "skill",
            "name": "econ-model-check",
            "version": "1",
        },
        "evidence_reviewed": ["E1"],
        "observations": [
            {
                "observation_id": "O1",
                "topic": "Jacobian timing",
                "summary": "The supplied timing convention is internally consistent.",
                "importance": "material",
                "evidence_refs": ["E1"],
                "limitations": [],
            }
        ],
        "limitations": [],
        "coverage_note": "The declared domain object was assessed.",
    }


def valid_report() -> dict[str, Any]:
    return {
        "schema_version": "econ-review-report/v3",
        "run_id": "fixture-run",
        "parent_status": "completed",
        "request_summary": {
            "surfaces": ["empirical-results"],
            "depth": "standard",
            "promotion": False,
        },
        "safety": {
            "mode": "prompt-and-canary",
        },
        "coverage": "full",
        "verdict": "clean",
        "selected_roles": [
            {
                "role": "inference",
                "state": "completed",
                "reason": None,
                "accepted_findings": 0,
                "review_method": "parent",
                "worker_ids": [],
                "evidence_reviewed": ["E1"],
                "coverage_note": "Parent checked the stated inference convention.",
            }
        ],
        "delegation": {"max_starts": 0, "max_concurrent": 0, "budget_changes": [], "workers": []},
        "findings": [],
        "warnings": [],
        "diagnostic_gaps": [],
        "process_failures": [],
        "supplemental_assessments": [],
        "promotion_gate": {
            "requested": False,
            "status": "not-requested",
            "reasons": [],
        },
        "state_canary": {
            "status": "unchanged",
            "in_scope_drift": [],
            "out_of_scope_drift": [],
        },
        "failure": None,
    }


def canonical_finding() -> dict[str, Any]:
    return {
        "finding_id": "F1",
        "severity": "P1",
        "trust_effect": "promotion-blocking",
        "issue_origin": "inference",
        "fix_class": "gated",
        "affected_labels": ["table-main"],
        "issue_followup_type": "empirical-problem",
        "title": "Inference convention is not documented",
        "why_it_matters": "The promoted uncertainty claim cannot be audited.",
        "evidence_refs": ["E1"],
        "evidence_locations": [
            {
                "evidence_id": "E1",
                "path": "results/table.tex",
                "locator": "line 12",
                "quote": None,
            }
        ],
        "recommended_action": "Document and verify the inference convention.",
        "user_judgement_required": True,
        "confidence": 100,
        "sources": [{"kind": "reviewer-role", "source_id": "inference"}],
        "disagreement": None,
    }


def canonical_gap() -> dict[str, Any]:
    return {
        "gap_id": "G1",
        "gap": "Cluster-count evidence is absent.",
        "trust_effect": "promotion-blocking",
        "issue_origin": "inference",
        "affected_labels": ["table-main"],
        "why_it_matters": "Finite-sample reliability cannot be assessed.",
        "evidence_refs": ["E1"],
        "recommended_action": "Add the realised cluster count.",
        "sources": [{"kind": "reviewer-role", "source_id": "inference"}],
    }


class ReviewSchemaContractsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.schemas = {
            key: load_json(REFERENCES / filename)
            for key, filename in SCHEMA_FILES.items()
        }
        cls.validators = {
            key: Draft202012Validator(schema)
            for key, schema in cls.schemas.items()
        }
        cls.valid_reviewer = load_json(FIXTURES / "valid.json")["raw_output"]

    def test_all_schemas_are_draft_2020_12_with_fixed_versions(self) -> None:
        for key, schema in self.schemas.items():
            with self.subTest(schema=key):
                Draft202012Validator.check_schema(schema)
                self.assertEqual(
                    schema["$schema"],
                    "https://json-schema.org/draft/2020-12/schema",
                )
                self.assertEqual(
                    schema["properties"]["schema_version"]["const"],
                    VERSIONS[key],
                )
                self.assertFalse(schema["additionalProperties"])

    def test_representative_objects_validate_against_all_four_schemas(self) -> None:
        samples = {
            "request": valid_request(),
            "reviewer": self.valid_reviewer,
            "domain": valid_domain_assessment(),
            "report": valid_report(),
        }
        for key, sample in samples.items():
            with self.subTest(schema=key):
                self.validators[key].validate(sample)

    def test_unknown_missing_and_extra_fields_are_rejected(self) -> None:
        samples = {
            "request": valid_request(),
            "reviewer": self.valid_reviewer,
            "domain": valid_domain_assessment(),
            "report": valid_report(),
        }
        for key, sample in samples.items():
            validator = self.validators[key]
            with self.subTest(schema=key, defect="unknown-version"):
                broken = copy.deepcopy(sample)
                broken["schema_version"] = VERSIONS[key] + "-unknown"
                self.assertTrue(list(validator.iter_errors(broken)))
            with self.subTest(schema=key, defect="missing-required"):
                broken = copy.deepcopy(sample)
                broken.pop("run_id", None)
                if key == "domain":
                    broken.pop("assessment_id")
                self.assertTrue(list(validator.iter_errors(broken)))
            with self.subTest(schema=key, defect="extra-field"):
                broken = copy.deepcopy(sample)
                broken["unexpected"] = True
                self.assertTrue(list(validator.iter_errors(broken)))

    def test_direct_and_nested_invocations_use_the_same_request_envelope(self) -> None:
        direct = valid_request()
        nested = copy.deepcopy(direct)
        nested["invocation"] = "nested"
        nested["caller"] = "econ-lfg/v1"
        self.validators["request"].validate(direct)
        self.validators["request"].validate(nested)
        self.assertEqual(set(direct), set(nested))
        self.assertEqual(
            set(direct["scope"]),
            set(nested["scope"]),
        )
        self.assertEqual(
            set(direct["triggers"]),
            set(nested["triggers"]),
        )

    def test_child_schema_excludes_parent_verdict_coverage_and_ids(self) -> None:
        for forbidden in ("verdict", "coverage", "promotion_gate", "finding_id"):
            with self.subTest(field=forbidden):
                broken = copy.deepcopy(self.valid_reviewer)
                broken[forbidden] = "forbidden"
                self.assertTrue(
                    list(self.validators["reviewer"].iter_errors(broken))
                )


    def test_initial_and_targeted_nested_requests_share_the_public_contract(self) -> None:
        initial = valid_request()
        initial["invocation"] = "nested"
        initial["caller"] = "econ-lfg/v1"
        self.validators["request"].validate(initial)
        self.assertIsNone(initial["resolution_context"])

        rereview = copy.deepcopy(initial)
        rereview["run_id"] = "fixture-rereview"
        rereview["resolution_context"] = {
            "prior_run_id": "fixture-run",
            "finding_outcomes": {
                "F1": {
                    "outcome": "fixed",
                    "changed_paths": ["analysis/model.py"],
                    "affected_labels": ["table-main"],
                    "prior_evidence_refs": ["E1"],
                },
                "F2": {
                    "outcome": "researcher-rejected",
                    "changed_paths": [],
                    "affected_labels": ["baseline"],
                    "prior_evidence_refs": ["E1"],
                },
                "F3": {
                    "outcome": "deferred",
                    "changed_paths": [],
                    "affected_labels": ["appendix-robustness"],
                    "prior_evidence_refs": ["E1"],
                },
            },
            "gap_outcomes": {},
        }
        self.validators["request"].validate(rereview)

        missing_context = copy.deepcopy(initial)
        missing_context.pop("resolution_context")
        self.assertTrue(
            list(self.validators["request"].iter_errors(missing_context))
        )

        malformed_context = copy.deepcopy(rereview)
        malformed_context["resolution_context"]["finding_outcomes"]["F1"][
            "outcome"
        ] = "silently-ignore"
        self.assertTrue(
            list(self.validators["request"].iter_errors(malformed_context))
        )

        fixed_without_path = copy.deepcopy(rereview)
        fixed_without_path["resolution_context"]["finding_outcomes"]["F1"][
            "changed_paths"
        ] = []
        self.assertTrue(
            list(self.validators["request"].iter_errors(fixed_without_path))
        )

        outcome_without_evidence = copy.deepcopy(rereview)
        outcome_without_evidence["resolution_context"]["finding_outcomes"]["F2"][
            "prior_evidence_refs"
        ] = []
        self.assertTrue(
            list(self.validators["request"].iter_errors(outcome_without_evidence))
        )

        invalid_finding_key = copy.deepcopy(rereview)
        invalid_finding_key["resolution_context"]["finding_outcomes"]["F1-copy"] = (
            invalid_finding_key["resolution_context"]["finding_outcomes"].pop("F1")
        )
        self.assertTrue(
            list(self.validators["request"].iter_errors(invalid_finding_key))
        )

        direct_with_history = copy.deepcopy(rereview)
        direct_with_history["invocation"] = "direct"
        direct_with_history["caller"] = None
        self.assertTrue(
            list(self.validators["request"].iter_errors(direct_with_history))
        )

        nested_without_caller = copy.deepcopy(initial)
        nested_without_caller["caller"] = None
        self.assertTrue(
            list(self.validators["request"].iter_errors(nested_without_caller))
        )


    def test_report_cross_field_safety_coverage_and_promotion_invariants(self) -> None:
        validator = self.validators["report"]

        unavailable = valid_report()
        unavailable["safety"] = {
            "mode": "unavailable",
        }
        unavailable["coverage"] = "not-run"
        unavailable["verdict"] = "blocked"
        unavailable["selected_roles"][0].update(
            state="unavailable",
            reason="review-unavailable",
            review_method="unreviewed",
        )
        unavailable["state_canary"]["status"] = "not-run"
        validator.validate(unavailable)

        no_completed_reviewer = valid_report()
        no_completed_reviewer["coverage"] = "not-run"
        no_completed_reviewer["verdict"] = "blocked"
        no_completed_reviewer["selected_roles"][0].update(
            state="failed",
            reason="child-error",
        )
        validator.validate(no_completed_reviewer)

        obsolete_safety_metadata = valid_report()
        obsolete_safety_metadata["safety"]["attestation"] = "legacy-proof"
        self.assertTrue(list(validator.iter_errors(obsolete_safety_metadata)))

        not_run_with_completed_role = copy.deepcopy(no_completed_reviewer)
        not_run_with_completed_role["selected_roles"][0].update(
            state="completed",
            reason=None,
        )
        self.assertTrue(list(validator.iter_errors(not_run_with_completed_role)))

        degraded_without_completed_role = copy.deepcopy(no_completed_reviewer)
        degraded_without_completed_role["coverage"] = "degraded"
        degraded_without_completed_role["verdict"] = "indeterminate"
        self.assertTrue(list(validator.iter_errors(degraded_without_completed_role)))

        degraded_without_cause = valid_report()
        degraded_without_cause["coverage"] = "degraded"
        degraded_without_cause["verdict"] = "indeterminate"
        self.assertTrue(list(validator.iter_errors(degraded_without_cause)))

        prompt_canary_not_run = copy.deepcopy(no_completed_reviewer)
        prompt_canary_not_run["state_canary"]["status"] = "not-run"
        self.assertTrue(list(validator.iter_errors(prompt_canary_not_run)))

        unavailable_with_wrong_reason = copy.deepcopy(unavailable)
        unavailable_with_wrong_reason["selected_roles"][0]["reason"] = "host-proof-missing"
        self.assertTrue(list(validator.iter_errors(unavailable_with_wrong_reason)))

        for path, value in (
            (("coverage",), "degraded"),
            (("verdict",), "indeterminate"),
            (("selected_roles", 0, "state"), "completed"),
            (("state_canary", "status"), "unchanged"),
        ):
            with self.subTest(unavailable_defect=path):
                broken = copy.deepcopy(unavailable)
                target: Any = broken
                for key in path[:-1]:
                    target = target[key]
                target[path[-1]] = value
                self.assertTrue(list(validator.iter_errors(broken)))

        full = valid_report()
        full["supplemental_assessments"] = [
            {
                "assessment_id": "optional-1",
                "assessment_type": "auxiliary-check",
                "required": False,
                "state": "failed",
                "reason": "Optional evidence was unavailable.",
            }
        ]
        validator.validate(full)

        full_with_failed_required = copy.deepcopy(full)
        full_with_failed_required["supplemental_assessments"][0][
            "required"
        ] = True
        self.assertTrue(
            list(validator.iter_errors(full_with_failed_required))
        )

        for path, value in (
            (("safety", "mode"), "unavailable"),
            (("selected_roles", 0, "state"), "failed"),
            (("state_canary", "status"), "drift-detected"),
            (("parent_status",), "failed"),
            (("verdict",), "blocked"),
        ):
            with self.subTest(full_defect=path):
                broken = copy.deepcopy(valid_report())
                target = broken
                for key in path[:-1]:
                    target = target[key]
                target[path[-1]] = value
                self.assertTrue(list(validator.iter_errors(broken)))

        full_with_process_failure = copy.deepcopy(valid_report())
        full_with_process_failure["process_failures"] = [
            {
                "stage": "dispatch",
                "code": "unexpected-retry",
                "message": "A review child required an undeclared retry.",
                "affected_roles": ["inference"],
            }
        ]
        self.assertTrue(
            list(validator.iter_errors(full_with_process_failure))
        )

        clean_with_finding = copy.deepcopy(valid_report())
        clean_with_finding["findings"] = [canonical_finding()]
        self.assertTrue(list(validator.iter_errors(clean_with_finding)))

        issues_without_finding = copy.deepcopy(valid_report())
        issues_without_finding["verdict"] = "issues-found"
        self.assertTrue(list(validator.iter_errors(issues_without_finding)))

        unrequested_but_blocked = copy.deepcopy(valid_report())
        unrequested_but_blocked["promotion_gate"]["status"] = "blocked"
        self.assertTrue(list(validator.iter_errors(unrequested_but_blocked)))

        passed = valid_report()
        passed["request_summary"]["promotion"] = True
        passed["promotion_gate"] = {
            "requested": True,
            "status": "passed",
            "reasons": [],
        }
        validator.validate(passed)

        for path, value in (
            (("coverage",), "degraded"),
            (("verdict",), "issues-found"),
            (("safety", "mode"), "unavailable"),
            (("selected_roles", 0, "state"), "failed"),
            (("state_canary", "status"), "drift-detected"),
        ):
            with self.subTest(promotion_defect=path):
                broken = copy.deepcopy(passed)
                target = broken
                for key in path[:-1]:
                    target = target[key]
                target[path[-1]] = value
                self.assertTrue(list(validator.iter_errors(broken)))

        passed_with_gap = copy.deepcopy(passed)
        passed_with_gap["diagnostic_gaps"] = [canonical_gap()]
        self.assertTrue(list(validator.iter_errors(passed_with_gap)))

    def test_nested_report_preserves_resolution_fields_and_diagnostic_gaps(self) -> None:
        report = valid_report()
        report["verdict"] = "issues-found"
        report["findings"] = [canonical_finding()]
        report["diagnostic_gaps"] = [canonical_gap()]
        self.validators["report"].validate(report)

        round_tripped = json.loads(json.dumps(report))
        finding = round_tripped["findings"][0]
        for field in (
            "fix_class",
            "affected_labels",
            "issue_followup_type",
            "evidence_locations",
            "user_judgement_required",
            "confidence",
        ):
            with self.subTest(field=field):
                self.assertEqual(finding[field], report["findings"][0][field])
                missing = copy.deepcopy(report)
                missing["findings"][0].pop(field)
                self.assertTrue(
                    list(self.validators["report"].iter_errors(missing))
                )
        self.assertEqual(
            round_tripped["diagnostic_gaps"],
            report["diagnostic_gaps"],
        )
        missing_gaps = copy.deepcopy(report)
        missing_gaps.pop("diagnostic_gaps")
        self.assertTrue(
            list(self.validators["report"].iter_errors(missing_gaps))
        )

    def test_gap_only_report_has_a_bounded_resolution_and_rereview_path(self) -> None:
        report = valid_report()
        report["verdict"] = "issues-found"
        report["diagnostic_gaps"] = [canonical_gap()]
        self.validators["report"].validate(report)

        request = valid_request()
        request["run_id"] = "fixture-gap-rereview"
        request["invocation"] = "nested"
        request["caller"] = "econ-lfg/v1"
        request["resolution_context"] = {
            "prior_run_id": report["run_id"],
            "finding_outcomes": {},
            "gap_outcomes": {
                "G1": {
                    "outcome": "fixed",
                    "changed_paths": ["analysis/diagnostics.py"],
                    "affected_labels": ["table-main"],
                    "prior_evidence_refs": ["E1"],
                }
            },
        }
        self.validators["request"].validate(request)

        broken = copy.deepcopy(request)
        broken["resolution_context"]["gap_outcomes"]["G1"][
            "changed_paths"
        ] = []
        self.assertTrue(list(self.validators["request"].iter_errors(broken)))

        no_outcomes = copy.deepcopy(request)
        no_outcomes["resolution_context"]["gap_outcomes"] = {}
        self.assertTrue(
            list(self.validators["request"].iter_errors(no_outcomes))
        )


if __name__ == "__main__":
    unittest.main()
