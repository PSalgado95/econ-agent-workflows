from __future__ import annotations

import copy
import importlib.util
import unittest
from pathlib import Path

from jsonschema import ValidationError
from test_review_contracts import valid_report, valid_request

REPO = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "validate_review_report",
    REPO / "skills/econ-review/scripts/validate_review_report.py",
)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)
validate_report = MODULE.validate_report


def worker(wid: str, roles: list[str], state: str = "completed") -> dict:
    return {
        "worker_id": wid, "roles": roles, "model": "gpt-5.6-sol",
        "effort": "low", "reason": "Trace a bounded code path.", "state": state,
    }


class ReviewExecutionTest(unittest.TestCase):
    def test_parent_only_full_coverage_needs_no_agents(self) -> None:
        validate_report(valid_report(), valid_request())

    def test_twelve_lenses_can_be_covered_by_two_workers(self) -> None:
        report = valid_report()
        names = [
            "provenance", "specification", "transformation-and-sample",
            "estimation-practice", "inference", "output-consistency",
            "claim-discipline", "code-quality", "design", "dynamics",
            "robustness", "software-equivalence",
        ]
        exemplar = report["selected_roles"][0]
        report["selected_roles"] = [
            dict(copy.deepcopy(exemplar), role=name, review_method="independent",
                 worker_ids=["W1" if i < 6 else "W2"])
            for i, name in enumerate(names)
        ]
        report["delegation"].update(
            max_starts=2, max_concurrent=2,
            workers=[worker("W1", names[:6]), worker("W2", names[6:])],
        )
        validate_report(report, valid_request())

    def test_luna_high_is_accepted_without_downgrading_coverage(self) -> None:
        report = valid_report()
        report["delegation"].update(max_starts=1, max_concurrent=1,
                                    workers=[worker("W1", ["inference"])])
        report["delegation"]["workers"][0].update(model="gpt-5.6-luna", effort="high")
        report["selected_roles"][0].update(review_method="independent", worker_ids=["W1"])
        validate_report(report)

    def test_failed_worker_can_be_replaced_by_honest_parent_check(self) -> None:
        report = valid_report()
        report["delegation"].update(max_starts=1, max_concurrent=1,
                                    workers=[worker("W1", ["inference"], "failed")])
        report["selected_roles"][0]["worker_ids"] = ["W1"]
        validate_report(report)
        report["selected_roles"][0]["review_method"] = "independent"
        with self.assertRaisesRegex(ValueError, "completed worker"):
            validate_report(report)

    def test_budget_and_fabricated_independence_fail(self) -> None:
        report = valid_report()
        report["delegation"].update(max_concurrent=1,
                                    workers=[worker("W1", ["inference"])])
        with self.assertRaisesRegex(ValueError, "exceed"):
            validate_report(report)
        report = valid_report()
        report["selected_roles"][0].update(review_method="independent", worker_ids=["invented"])
        with self.assertRaisesRegex(ValueError, "unknown"):
            validate_report(report)

    def test_unknown_evidence_and_legacy_report_fail(self) -> None:
        report = valid_report()
        report["selected_roles"][0]["evidence_reviewed"] = ["E9"]
        with self.assertRaisesRegex(ValueError, "outside"):
            validate_report(report, valid_request())
        report = valid_report()
        report["schema_version"] = "econ-review-report/v2"
        with self.assertRaises(ValidationError):
            validate_report(report)


if __name__ == "__main__":
    unittest.main()
