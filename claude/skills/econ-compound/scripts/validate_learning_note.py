#!/usr/bin/env python3
"""Validator for econ-compound learning notes."""

from __future__ import annotations

import re
import sys
from pathlib import Path


REQUIRED = {
    "title",
    "date",
    "status",
    "scope",
    "scope_basis",
    "category",
    "evidence_paths",
    "applies_when",
    "do_not_apply_when",
    "last_checked",
    "supersedes",
    "superseded_by",
    "refresh_reason",
}

STATUSES = {"active", "provisional", "stale", "superseded"}
SCOPES = {"project", "repo", "general"}
CATEGORIES = {
    "source-provenance",
    "data-measurement",
    "sample-linkage",
    "specification-estimation",
    "theory-models",
    "interpretation-claims",
    "writing-figures",
    "reproducibility-handoff",
    "workflow-practice",
}
SECTIONS = (
    "## Situation",
    "## Durable Lesson",
    "## Evidence",
    "## Reuse Boundary",
    "## Future Workflow Use",
)
PLACEHOLDERS = (
    "short descriptive title",
    "yyyy-mm-dd",
    "path/to/",
    "path\\to\\",
    "condition where",
    "what happened",
    "state the reusable",
    "name the plan",
    "state when to apply",
    "state how future",
)
FILE_LIKE_SUFFIXES = {
    ".csv",
    ".docx",
    ".do",
    ".html",
    ".ipynb",
    ".json",
    ".log",
    ".md",
    ".pdf",
    ".py",
    ".r",
    ".rds",
    ".tex",
    ".txt",
    ".xlsx",
    ".yaml",
    ".yml",
}
SOURCE_ID_PREFIXES = (
    "source_id:",
    "archive_id:",
    "register_id:",
    "dataset_id:",
    "doi:",
)


def parse_frontmatter(text: str) -> tuple[dict[str, object], str]:
    if not text.startswith("---\n"):
        raise ValueError("missing opening frontmatter delimiter")
    end = text.find("\n---", 4)
    if end == -1:
        raise ValueError("missing closing frontmatter delimiter")
    raw = text[4:end].splitlines()
    body = text[end + 4 :]
    data: dict[str, object] = {}
    current_key: str | None = None
    for line in raw:
        if not line.strip():
            continue
        if re.match(r"^[A-Za-z_][A-Za-z0-9_-]*:", line):
            key, value = line.split(":", 1)
            key = key.strip()
            value = value.strip()
            if value == "":
                data[key] = []
                current_key = key
            else:
                data[key] = value.strip('"')
                current_key = None
            continue
        if line.startswith("  - ") and current_key:
            item = line[4:].strip().strip('"')
            if not isinstance(data[current_key], list):
                data[current_key] = []
            data[current_key].append(item)
            continue
        raise ValueError(f"cannot parse frontmatter line: {line}")
    return data, body


def as_scalar(data: dict[str, object], key: str) -> str:
    value = data.get(key, "")
    if isinstance(value, list):
        return ""
    return str(value).strip()


def as_list(data: dict[str, object], key: str) -> list[str]:
    value = data.get(key)
    if not isinstance(value, list):
        return []
    return [str(item).strip() for item in value]


def is_noneish(value: str) -> bool:
    return value.strip().lower() in {"", "none", "n/a", "na", "not applicable"}


def has_placeholder(value: str) -> bool:
    lowered = value.lower()
    return any(token in lowered for token in PLACEHOLDERS)


def is_url(value: str) -> bool:
    return bool(re.match(r"^[a-z][a-z0-9+.-]*://", value, flags=re.IGNORECASE))


def is_source_id(value: str) -> bool:
    lowered = value.lower()
    return any(lowered.startswith(prefix) and len(value) > len(prefix) for prefix in SOURCE_ID_PREFIXES)


def is_absolute_local_path(value: str) -> bool:
    return bool(
        re.match(r"^[A-Za-z]:[\\/]", value)
        or value.startswith("\\\\")
        or value.startswith("/")
    )


def strip_fragment(value: str) -> str:
    return value.split("#", 1)[0].strip()


def looks_file_like(value: str) -> bool:
    clean = strip_fragment(value)
    if not clean or is_url(clean) or is_source_id(clean):
        return False
    if any(ch in clean for ch in ("*", "?")):
        return False
    suffix = Path(clean.replace("\\", "/")).suffix.lower()
    return "/" in clean or "\\" in clean or suffix in FILE_LIKE_SUFFIXES


def infer_root(note_path: Path) -> Path:
    parts = list(note_path.resolve().parts)
    lowered = [part.lower() for part in parts]
    for marker in (["docs", "research-learnings"], [".codex", "research-learnings"]):
        for i in range(0, len(lowered) - len(marker) + 1):
            if lowered[i : i + len(marker)] == marker:
                return Path(*parts[:i]) if i else Path(parts[0])
    return note_path.resolve().parent


def reference_values(data: dict[str, object], key: str) -> list[str]:
    value = data.get(key)
    if isinstance(value, list):
        return [str(item).strip() for item in value if not is_noneish(str(item))]
    scalar = str(value or "").strip()
    if is_noneish(scalar):
        return []
    return [item.strip() for item in scalar.split(";") if item.strip()]


def validate_reference(value: str, root: Path, field_name: str, errors: list[str], warnings: list[str]) -> None:
    clean = strip_fragment(value)
    if has_placeholder(value):
        errors.append(f"{field_name} still contains placeholder text: {value}")
        return
    if is_url(clean):
        warnings.append(f"{field_name} is a URL and was not file-checked: {value}")
        return
    if is_source_id(clean):
        warnings.append(f"{field_name} treated as a source ID and was not file-checked: {value}")
        return
    if is_absolute_local_path(clean):
        errors.append(f"{field_name} must be repo-relative or an explicit source ID, not absolute: {value}")
        return
    if looks_file_like(clean):
        target = (root / clean).resolve()
        if not target.exists():
            errors.append(f"checkable local {field_name} does not exist relative to {root}: {value}")
    else:
        warnings.append(f"{field_name} treated as a non-file source ID and was not file-checked: {value}")


def parse_body_sections(body: str) -> dict[str, str]:
    starts = [(match.group(0).strip(), match.start()) for match in re.finditer(r"^## .+$", body, flags=re.MULTILINE)]
    sections: dict[str, str] = {}
    for idx, (heading, start) in enumerate(starts):
        end = starts[idx + 1][1] if idx + 1 < len(starts) else len(body)
        content_start = start + len(heading)
        sections[heading] = body[content_start:end].strip()
    return sections


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: validate_learning_note.py <note.md>", file=sys.stderr)
        return 2

    path = Path(sys.argv[1])
    text = path.read_text(encoding="utf-8")
    try:
        data, body = parse_frontmatter(text)
    except ValueError as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1

    errors: list[str] = []
    warnings: list[str] = []

    missing = sorted(REQUIRED - set(data))
    if missing:
        errors.append("missing frontmatter fields: " + ", ".join(missing))

    status = as_scalar(data, "status")
    scope = as_scalar(data, "scope")
    category = as_scalar(data, "category")
    scope_basis = as_scalar(data, "scope_basis")
    supersedes = as_scalar(data, "supersedes")
    superseded_by = as_scalar(data, "superseded_by")
    refresh_reason = as_scalar(data, "refresh_reason")

    if status not in STATUSES:
        errors.append("status must be active, provisional, stale, or superseded")
    if scope not in SCOPES:
        errors.append("scope must be project, repo, or general")
    if category not in CATEGORIES:
        errors.append("category is not in the allowed list")

    for key in ("title", "scope_basis", "refresh_reason", "supersedes", "superseded_by"):
        value = as_scalar(data, key)
        if value and has_placeholder(value):
            errors.append(f"{key} still contains placeholder text")

    for key in ("date", "last_checked"):
        value = as_scalar(data, key)
        if not re.match(r"^\d{4}-\d{2}-\d{2}$", value):
            errors.append(f"{key} must use YYYY-MM-DD")

    for key in ("evidence_paths", "applies_when", "do_not_apply_when"):
        values = as_list(data, key)
        if not values:
            errors.append(f"{key} must be a non-empty YAML list")
            continue
        for item in values:
            if is_noneish(item):
                errors.append(f"{key} contains an empty or none-like item")
            if has_placeholder(item):
                errors.append(f"{key} still contains placeholder text")

    if scope == "general":
        basis = scope_basis.lower()
        if "user-confirmed" not in basis and "multiple project" not in basis:
            errors.append("scope: general requires scope_basis to mention user-confirmed general use or multiple projects")
    elif is_noneish(scope_basis):
        errors.append("scope_basis must explain why the selected scope is justified")

    if status == "stale":
        if is_noneish(refresh_reason):
            errors.append("status: stale requires refresh_reason")
        if not is_noneish(superseded_by):
            errors.append("stale notes should not set superseded_by; use status: superseded when a successor exists")
    elif status == "superseded":
        if is_noneish(superseded_by):
            errors.append("status: superseded requires superseded_by")
        if not is_noneish(refresh_reason):
            warnings.append("superseded notes usually do not need refresh_reason")
    else:
        if not is_noneish(superseded_by):
            errors.append("superseded_by should be none unless status is superseded")
        if not is_noneish(refresh_reason):
            errors.append("refresh_reason should be none unless status is stale")

    root = infer_root(path)
    for evidence in as_list(data, "evidence_paths"):
        validate_reference(evidence, root, "evidence path", errors, warnings)
    for predecessor in reference_values(data, "supersedes"):
        validate_reference(predecessor, root, "supersedes reference", errors, warnings)
    if not is_noneish(superseded_by):
        validate_reference(superseded_by, root, "superseded_by reference", errors, warnings)

    sections = parse_body_sections(body)
    missing_sections = [section for section in SECTIONS if section not in sections]
    if missing_sections:
        errors.append("missing body sections: " + ", ".join(missing_sections))

    for section in SECTIONS:
        content = sections.get(section, "")
        if not content:
            errors.append(f"{section} is empty")
        elif has_placeholder(content):
            errors.append(f"{section} still contains placeholder text")
        elif len(content.split()) < 5:
            errors.append(f"{section} is too thin to be a useful learning note")

    if errors:
        print("FAIL: " + "; ".join(errors), file=sys.stderr)
        if warnings:
            print("WARN: " + "; ".join(warnings), file=sys.stderr)
        return 1

    if warnings:
        print("PASS with warnings: " + "; ".join(warnings))
    else:
        print("PASS: learning note is valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
