"""Validate report v3, including worker provenance and resource accounting.

Usage: python validate_review_report.py REPORT.json [--request REQUEST.json]
Requires jsonschema. Reads files only; never rewrites evidence or reports.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator


def validate_report(report: dict[str, Any], request: dict[str, Any] | None = None) -> None:
    schema = Path(__file__).resolve().parents[1] / "references/review-report-schema.json"
    Draft202012Validator(json.loads(schema.read_text(encoding="utf-8"))).validate(report)
    delegation = report["delegation"]
    workers = {w["worker_id"]: w for w in delegation["workers"]}
    if len(workers) != len(delegation["workers"]):
        raise ValueError("Duplicate worker IDs")
    if len(workers) > delegation["max_starts"]:
        raise ValueError("Worker starts exceed the declared budget")
    if delegation["max_concurrent"] > delegation["max_starts"]:
        raise ValueError("Concurrency limit exceeds total-start budget")
    if workers and delegation["max_concurrent"] == 0:
        raise ValueError("Workers recorded with a zero concurrency limit")
    roles = {r["role"]: r for r in report["selected_roles"]}
    if len(roles) != len(report["selected_roles"]):
        raise ValueError("Duplicate coverage roles")
    for worker in workers.values():
        if not set(worker["roles"]).issubset(roles):
            raise ValueError("Worker assigned a role outside the coverage inventory")
    for role in roles.values():
        for wid in role["worker_ids"]:
            if wid not in workers or role["role"] not in workers[wid]["roles"]:
                raise ValueError("Coverage references an unknown or unrelated worker")
        if role["review_method"] == "independent" and not any(
            workers[wid]["state"] == "completed" for wid in role["worker_ids"]
        ):
            raise ValueError("Independent coverage requires a completed worker")
    for finding in report["findings"] + report["warnings"] + report["diagnostic_gaps"]:
        for source in finding["sources"]:
            kind, sid = source["kind"], source["source_id"]
            if kind == "parent-review":
                if sid not in roles or roles[sid]["state"] != "completed":
                    raise ValueError("Parent observation requires completed lens coverage")
            elif kind == "reviewer-role":
                if sid not in roles or not any(
                    workers[wid]["state"] == "completed" for wid in roles[sid]["worker_ids"]
                ):
                    raise ValueError("Reviewer observation requires a completed contributing worker")
    if request is not None:
        if report["run_id"] != request["run_id"]:
            raise ValueError("Report/request run mismatch")
        evidence = {e["evidence_id"]: e["path"] for e in request["evidence_manifest"]}
        for role in roles.values():
            if not set(role["evidence_reviewed"]).issubset(evidence):
                raise ValueError("Coverage cites evidence outside the request")
        for finding in report["findings"] + report["warnings"] + report["diagnostic_gaps"]:
            if not set(finding["evidence_refs"]).issubset(evidence):
                raise ValueError("Finding cites evidence outside the request")
            for location in finding.get("evidence_locations", []):
                if evidence.get(location["evidence_id"]) != location["path"]:
                    raise ValueError("Finding location does not match the evidence manifest")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("report", type=Path)
    parser.add_argument("--request", type=Path)
    args = parser.parse_args()
    request = json.loads(args.request.read_text(encoding="utf-8")) if args.request else None
    validate_report(json.loads(args.report.read_text(encoding="utf-8")), request)
    print("Review report valid (schema and cross-record checks).")


if __name__ == "__main__":
    main()
