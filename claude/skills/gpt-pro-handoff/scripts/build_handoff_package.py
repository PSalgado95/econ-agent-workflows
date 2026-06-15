#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import textwrap
import zipfile
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


DEFAULT_MAX_FILES = 12
DEFAULT_STAGED_MAX_FILES = 24
DEFAULT_SOFT_MAX_MB = 25.0
DEFAULT_HARD_FILE_MB = 50.0
MAX_RECORDED_OMISSIONS = 40
DEFAULT_EXPECTED_OUTPUT = textwrap.dedent(
    """\
    Return a structured memo or note appropriate to the task, with:
    1. Bottom-line answer
    2. Main reasoning or evidence
    3. Main objections, alternative interpretations, or decision-relevant tradeoffs
    4. Uncertainty, missing evidence, or fragile assumptions
    5. Recommended next checks or follow-up analysis
    """
).strip()
DEFAULT_DOWNLOADS_DIR = Path.home() / "Downloads" / "GPT Pro Packages"
SKIP_DIR_NAMES = {
    ".git",
    ".hg",
    ".svn",
    ".idea",
    ".vscode",
    ".venv",
    "__pycache__",
    "node_modules",
    "tmp",
    "temp",
    "dist",
    "build",
    "coverage",
}
STAGED_ROLE_DIR_NAMES = {
    "package",
    "evidence",
    "code",
    "shared",
    "discussion",
    "drafts",
    "examples",
}
STAGED_CONTROL_FILE_PRIORITY = {
    "governing_direction.md": 0,
    "reading_order.md": 1,
    "return_contract.md": 2,
    "return_contract.yaml": 2,
    "return_contract.yml": 2,
    "return_spec.md": 2,
    "return_spec.yaml": 2,
    "return_spec.yml": 2,
    "repo_scan.md": 3,
    "scope_notes.md": 4,
}
SKIP_SUFFIXES = {
    ".7z",
    ".bin",
    ".dll",
    ".dylib",
    ".exe",
    ".gz",
    ".iso",
    ".log",
    ".msi",
    ".o",
    ".obj",
    ".pkl",
    ".pyc",
    ".so",
    ".tar",
    ".tmp",
    ".zip",
}
AUTO_EXTENSIONS = {
    ".csv",
    ".docx",
    ".ipynb",
    ".jl",
    ".json",
    ".md",
    ".pdf",
    ".png",
    ".pptx",
    ".py",
    ".r",
    ".tex",
    ".tsv",
    ".txt",
    ".xlsx",
    ".xls",
    ".yaml",
    ".yml",
}
EXTENSION_WEIGHTS = {
    ".md": 70,
    ".txt": 65,
    ".pdf": 62,
    ".csv": 58,
    ".xlsx": 55,
    ".xls": 53,
    ".docx": 52,
    ".json": 48,
    ".yaml": 46,
    ".yml": 46,
    ".tex": 42,
    ".tsv": 40,
    ".pptx": 38,
    ".png": 28,
    ".ipynb": 24,
    ".py": 20,
    ".r": 20,
    ".jl": 20,
}
KEYWORD_WEIGHTS = {
    "analysis": 18,
    "brief": 24,
    "caption": 8,
    "check": 16,
    "comparison": 22,
    "config": 14,
    "context": 16,
    "dashboard": 12,
    "doc": 10,
    "draft": 6,
    "evidence": 18,
    "figure": 14,
    "finding": 20,
    "handoff": 16,
    "irf": 18,
    "lp": 14,
    "manifest": 10,
    "memo": 22,
    "note": 20,
    "output": 14,
    "overview": 16,
    "prompt": 8,
    "readme": 24,
    "report": 24,
    "result": 24,
    "robustness": 16,
    "spec": 16,
    "summary": 30,
    "table": 22,
    "workflow": 18,
}
SLUG_STOPWORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "by",
    "for",
    "from",
    "help",
    "how",
    "i",
    "if",
    "in",
    "into",
    "is",
    "it",
    "me",
    "my",
    "of",
    "on",
    "or",
    "our",
    "please",
    "review",
    "that",
    "the",
    "this",
    "to",
    "use",
    "using",
    "we",
    "with",
    "you",
    "your",
}


@dataclass(frozen=True)
class Candidate:
    source_path: Path
    relative_path: Path
    size_bytes: int
    explicit_rank: int
    score: int


@dataclass(frozen=True)
class Omission:
    path: str
    reason: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create a GPT Pro handoff package in Downloads/GPT Pro Packages.",
    )
    parser.add_argument("--task", required=True, help="Task to give GPT Pro.")
    parser.add_argument("--workspace", default=".", help="Workspace root for relative paths.")
    parser.add_argument(
        "--include",
        action="append",
        default=[],
        help="File or folder to prioritize. Repeatable.",
    )
    parser.add_argument("--title", default="", help="Optional label for the handoff brief.")
    parser.add_argument(
        "--instruction",
        action="append",
        default=[],
        help="Instruction to preserve verbatim in the GPT Pro prompt. Repeatable.",
    )
    parser.add_argument(
        "--expected-output",
        default="",
        help="Override the default expected output section in the GPT Pro prompt.",
    )
    parser.add_argument(
        "--max-files",
        type=int,
        default=DEFAULT_MAX_FILES,
        help=(
            f"Soft limit for source files to include. Default: {DEFAULT_MAX_FILES}; "
            f"staged role-folder packages auto-expand to at least {DEFAULT_STAGED_MAX_FILES} unless you set a higher value."
        ),
    )
    parser.add_argument(
        "--soft-max-mb",
        type=float,
        default=DEFAULT_SOFT_MAX_MB,
        help=f"Soft cap for included source-file size before compression. Default: {DEFAULT_SOFT_MAX_MB}.",
    )
    parser.add_argument(
        "--hard-file-mb",
        type=float,
        default=DEFAULT_HARD_FILE_MB,
        help=f"Per-file guardrail. Files larger than this are omitted. Default: {DEFAULT_HARD_FILE_MB}.",
    )
    parser.add_argument(
        "--downloads-dir",
        default=str(DEFAULT_DOWNLOADS_DIR),
        help="Output directory for the zip and standalone prompt file.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Print machine-readable JSON instead of a human summary.",
    )
    return parser.parse_args()


def slugify_label(text: str, max_words: int = 4, max_length: int = 24) -> str:
    tokens = re.findall(r"[a-z0-9]+", text.lower())
    filtered = [
        token
        for token in tokens
        if token not in SLUG_STOPWORDS and (len(token) > 2 or token.isdigit() or token == "lp")
    ]
    chosen = filtered or tokens
    if not chosen:
        return "package"

    words: list[str] = []
    current_length = 0
    for token in chosen:
        projected = current_length + len(token) + (1 if words else 0)
        if words and (len(words) >= max_words or projected > max_length):
            break
        words.append(token)
        current_length = projected

    return "-".join(words) or "package"


def unique_output_stem(downloads_dir: Path, title: str, task: str) -> str:
    month_day = datetime.now().strftime("%m-%d")
    label = slugify_label(title.strip() or task.strip())
    base = f"gptpro_{month_day}_{label}"
    stem = base
    counter = 2
    while (downloads_dir / f"{stem}.zip").exists():
        stem = f"{base}-{counter}"
        counter += 1
    return stem


def resolve_input_path(raw_path: str, workspace: Path) -> Path:
    candidate = Path(raw_path)
    if candidate.is_absolute():
        return candidate.resolve()
    return (workspace / candidate).resolve()


def should_skip_file(path: Path, explicit_rank: int) -> bool:
    suffix = path.suffix.lower()
    if suffix in SKIP_SUFFIXES:
        return True
    if explicit_rank == 0 and suffix not in AUTO_EXTENSIONS:
        return True
    return False


def iter_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for current_root, dirnames, filenames in os.walk(root):
        dirnames[:] = [
            name
            for name in dirnames
            if name.lower() not in SKIP_DIR_NAMES and not name.startswith(".")
        ]
        current_dir = Path(current_root)
        for filename in filenames:
            files.append(current_dir / filename)
    return files


def score_candidate(relative_path: Path, size_bytes: int, explicit_rank: int) -> int:
    score = 0
    score += 300 if explicit_rank == 2 else 150 if explicit_rank == 1 else 0
    score += EXTENSION_WEIGHTS.get(relative_path.suffix.lower(), 8)
    pieces = re.split(r"[^a-z0-9]+", relative_path.as_posix().lower())
    for piece in pieces:
        score += KEYWORD_WEIGHTS.get(piece, 0)
    if relative_path.name.lower().startswith("readme"):
        score += 15
    if size_bytes <= 250_000:
        score += 20
    elif size_bytes <= 1_000_000:
        score += 12
    elif size_bytes <= 5_000_000:
        score += 4
    else:
        score -= 8
    depth = len(relative_path.parts)
    score += max(0, 8 - depth)
    return score


def format_bytes(num_bytes: int) -> str:
    units = ["B", "KB", "MB", "GB"]
    size = float(num_bytes)
    for unit in units:
        if size < 1024 or unit == units[-1]:
            if unit == "B":
                return f"{int(size)} {unit}"
            return f"{size:.1f} {unit}"
        size /= 1024
    return f"{num_bytes} B"


def explicit_label(explicit_rank: int) -> str:
    if explicit_rank == 2:
        return "explicit include"
    if explicit_rank == 1:
        return "inside explicit folder"
    return "auto-selected"


def compress_omissions(
    omissions: list[Omission],
    limit: int = MAX_RECORDED_OMISSIONS,
) -> tuple[list[Omission], int]:
    if len(omissions) <= limit:
        return omissions, 0
    return omissions[:limit], len(omissions) - limit


def collect_candidates(
    workspace: Path,
    include_paths: list[str],
    hard_file_limit_bytes: int,
) -> tuple[list[Candidate], list[Omission]]:
    candidate_map: dict[Path, Candidate] = {}
    omissions: list[Omission] = []

    def add_candidate(path: Path, explicit_rank: int) -> None:
        if not path.exists():
            omissions.append(Omission(path=str(path), reason="missing requested path"))
            return
        if path.is_dir():
            child_rank = 1 if explicit_rank > 0 else 0
            for child in iter_files(path):
                add_candidate(child, child_rank)
            return
        if should_skip_file(path, explicit_rank):
            return
        try:
            size_bytes = path.stat().st_size
        except OSError:
            omissions.append(Omission(path=str(path), reason="could not read file metadata"))
            return
        if size_bytes > hard_file_limit_bytes:
            omissions.append(
                Omission(
                    path=str(path),
                    reason=f"omitted because it exceeded the per-file guardrail ({format_bytes(hard_file_limit_bytes)})",
                )
            )
            return
        try:
            relative_path = path.resolve().relative_to(workspace)
        except ValueError:
            relative_path = Path(path.name)
        score = score_candidate(relative_path, size_bytes, explicit_rank)
        existing = candidate_map.get(path.resolve())
        new_candidate = Candidate(
            source_path=path.resolve(),
            relative_path=relative_path,
            size_bytes=size_bytes,
            explicit_rank=explicit_rank,
            score=score,
        )
        if existing is None or (
            new_candidate.explicit_rank,
            new_candidate.score,
        ) > (
            existing.explicit_rank,
            existing.score,
        ):
            candidate_map[path.resolve()] = new_candidate

    if include_paths:
        for raw_path in include_paths:
            add_candidate(resolve_input_path(raw_path, workspace), explicit_rank=2)
    else:
        add_candidate(workspace, explicit_rank=0)

    return list(candidate_map.values()), omissions


def choose_candidates(
    candidates: list[Candidate],
    max_files: int,
    soft_max_bytes: int,
    staged_mode: bool,
) -> tuple[list[Candidate], list[Omission]]:
    selected: list[Candidate] = []
    omitted: list[Omission] = []
    running_bytes = 0
    ordered = sorted(
        candidates,
        key=lambda item: (
            *candidate_priority_key(item.relative_path, staged_mode),
            -item.explicit_rank,
            -item.score,
            item.size_bytes,
            item.relative_path.as_posix(),
        ),
    )

    for candidate in ordered:
        if len(selected) >= max_files:
            omitted.append(
                Omission(
                    path=candidate.relative_path.as_posix(),
                    reason="omitted to keep the package lean within the file-count budget",
                )
            )
            continue
        projected_bytes = running_bytes + candidate.size_bytes
        if selected and projected_bytes > soft_max_bytes and candidate.explicit_rank == 0:
            omitted.append(
                Omission(
                    path=candidate.relative_path.as_posix(),
                    reason="omitted to keep the package lean within the size budget",
                )
            )
            continue
        selected.append(candidate)
        running_bytes = projected_bytes

    return selected, omitted


def top_paths(candidates: list[Candidate], count: int = 5) -> list[str]:
    return [candidate.relative_path.as_posix() for candidate in candidates[:count]]


def top_level_dir(relative_path: Path) -> str:
    return relative_path.parts[0] if relative_path.parts else ""


def package_control_file_priority(relative_path: Path) -> int | None:
    if top_level_dir(relative_path) != "package":
        return None
    return STAGED_CONTROL_FILE_PRIORITY.get(relative_path.name.lower())


def is_package_control_file(relative_path: Path) -> bool:
    return package_control_file_priority(relative_path) is not None


def looks_like_staged_package(candidates: list[Candidate]) -> bool:
    top_level_dirs = {top_level_dir(candidate.relative_path) for candidate in candidates if candidate.relative_path.parts}
    return "package" in top_level_dirs and bool(top_level_dirs & (STAGED_ROLE_DIR_NAMES - {"package"}))


def candidate_priority_key(relative_path: Path, staged_mode: bool) -> tuple[int, int]:
    if not staged_mode:
        return (2, 999)
    control_priority = package_control_file_priority(relative_path)
    if control_priority is not None:
        return (0, control_priority)
    if top_level_dir(relative_path) == "package":
        return (1, 999)
    return (2, 999)


def find_binding_contract_path(selected_paths: list[str]) -> str:
    preferred_names = [
        "package/return_contract.md",
        "package/return_contract.yaml",
        "package/return_contract.yml",
        "package/return_spec.md",
        "package/return_spec.yaml",
        "package/return_spec.yml",
    ]
    for path in preferred_names:
        if path in selected_paths:
            return path
    return ""


def build_brief(
    task: str,
    title: str,
    workspace: Path,
    selected: list[Candidate],
    instructions: list[str],
    omitted: list[Omission],
) -> str:
    header = title.strip() or "GPT Pro Handoff Brief"
    included_lines = "\n".join(
        f"- `{candidate.relative_path.as_posix()}` ({format_bytes(candidate.size_bytes)})"
        for candidate in selected[:8]
    )
    if not included_lines:
        included_lines = "- No source files were selected. Use the manifest to inspect warnings."

    omitted_lines = "\n".join(
        f"- `{omission.path}`: {omission.reason}"
        for omission in omitted[:6]
    )
    if not omitted_lines:
        omitted_lines = "- No notable omissions were recorded."

    instruction_lines = "\n".join(f"- {line}" for line in instructions) if instructions else "- No extra instructions were supplied."

    reading_order = "\n".join(
        f"{index}. `{path}`" for index, path in enumerate(top_paths(selected, 4), start=1)
    )
    if not reading_order:
        reading_order = "1. `package_manifest.md`"
    return "\n".join(
        [
            f"# {header}",
            "",
            "## Task",
            "",
            task.strip(),
            "",
            "## Workspace",
            "",
            f"- `{workspace}`",
            "",
            "## Included source artifacts",
            "",
            included_lines,
            "",
            "## User instructions preserved in the prompt",
            "",
            instruction_lines,
            "",
            "## Curation notes",
            "",
            "- This package was curated to stay legible and agent-ready.",
            "- Preference went to governing context, key evidence, and direct supporting surfaces.",
            "- Redundant, oversized, or lower-priority files were left out and documented in the manifest.",
            "",
            "## Notable omissions or warnings",
            "",
            omitted_lines,
            "",
            "## Suggested reading order",
            "",
            reading_order,
            "",
        ]
    )


def build_prompt(
    task: str,
    selected: list[Candidate],
    instructions: list[str],
    expected_output: str,
) -> str:
    role_dirs = STAGED_ROLE_DIR_NAMES
    selected_paths = [candidate.relative_path.as_posix() for candidate in selected]
    top_level_dirs = {
        candidate.relative_path.parts[0]
        for candidate in selected
        if candidate.relative_path.parts
    }
    has_staged_roles = bool(top_level_dirs & role_dirs)
    has_governing_direction = "package/governing_direction.md" in selected_paths
    has_reading_order = "package/reading_order.md" in selected_paths
    return_contract_path = find_binding_contract_path(selected_paths)
    package_lines = "\n".join(
        f"- `source/{candidate.relative_path.as_posix()}`"
        for candidate in selected[:8]
    )
    if not package_lines:
        package_lines = "- See `package_manifest.md` for the packaged contents and warnings."

    instruction_block = "\n".join(f"- {item}" for item in instructions)
    if not instruction_block:
        instruction_block = "- No additional user instructions were supplied."

    how_to_use_lines = [
        "1. Read `handoff_brief.md` first.",
        "2. Read `package_manifest.md` second.",
    ]
    step_number = 3
    if has_governing_direction:
        how_to_use_lines.append(f"{step_number}. Read `source/package/governing_direction.md`.")
        step_number += 1
    if has_reading_order:
        how_to_use_lines.append(f"{step_number}. Read `source/package/reading_order.md`.")
        step_number += 1
    if return_contract_path:
        how_to_use_lines.append(
            f"{step_number}. Treat `source/{return_contract_path}` as binding for filenames and bundle structure."
        )
        step_number += 1
    if {"evidence", "code"}.issubset(top_level_dirs):
        how_to_use_lines.append(
            f"{step_number}. Use `source/evidence/` for prior analysis and `source/code/` for the live implementation surface."
        )
        step_number += 1
    elif has_staged_roles:
        how_to_use_lines.append(
            f"{step_number}. Use the role folders under `source/` in the intended order; do not treat them as one flat file pool."
        )
        step_number += 1
    else:
        how_to_use_lines.append(f"{step_number}. Use the files in `source/` as the primary evidence.")

    deliverables_block = expected_output.strip()
    if not deliverables_block:
        if return_contract_path:
            deliverables_block = f"Follow the binding contract in `source/{return_contract_path}`."
        else:
            deliverables_block = DEFAULT_EXPECTED_OUTPUT

    success_criteria_lines = [
        "- The final answer directly addresses the goal.",
        "- Claims are grounded in the packaged evidence or clearly labeled as inference or assumptions.",
    ]
    if return_contract_path:
        success_criteria_lines.append("- The binding return contract is followed for filenames and bundle structure.")
    else:
        success_criteria_lines.append("- The deliverables match the requested output shape.")

    evidence_rules = [
        "- Distinguish source-backed claims from inference or assumptions.",
        "- Call out missing evidence or ambiguities before relying on them.",
    ]
    if {"evidence", "code"}.issubset(top_level_dirs):
        evidence_rules.insert(
            0,
            "- Use `source/evidence/` for prior analysis and `source/code/` for the live implementation surface.",
        )
    elif has_staged_roles:
        evidence_rules.insert(
            0,
            "- Use the role folders under `source/` according to their purpose rather than as one flat file pool.",
        )
    else:
        evidence_rules.insert(0, "- Use the files in `source/` as the primary evidence.")

    stop_rules = [
        "- Stop once the success criteria can be met from the package and any allowed external research.",
        "- If a blocking input is missing, name the smallest missing input rather than broadening the task.",
        "- If the requested output cannot be supported by the package, return the closest useful bounded answer and list the blocker.",
    ]

    return "\n".join(
        [
            "You are reviewing a curated handoff package prepared by Codex.",
            "",
            "## Goal",
            "",
            task.strip(),
            "",
            "## Success criteria",
            "",
            *success_criteria_lines,
            "",
            "## How to use the package",
            "",
            *how_to_use_lines,
            "",
            "## Key packaged sources",
            "",
            package_lines,
            "",
            "## Deliverables",
            "",
            deliverables_block,
            "",
            "## Evidence rules",
            "",
            *evidence_rules,
            "",
            "## Working rules",
            "",
            instruction_block,
            "",
            "## Stop rules",
            "",
            *stop_rules,
            "",
        ]
    )


def build_manifest(
    task: str,
    title: str,
    workspace: Path,
    selected: list[Candidate],
    omitted: list[Omission],
    max_files: int,
    soft_max_bytes: int,
) -> str:
    visible_omissions, remaining_omissions = compress_omissions(omitted)
    included_lines = "\n".join(
        f"- `{candidate.relative_path.as_posix()}` | {format_bytes(candidate.size_bytes)} | score {candidate.score} | "
        f"{explicit_label(candidate.explicit_rank)}"
        for candidate in selected
    )
    if not included_lines:
        included_lines = "- No source files were packaged."

    omitted_lines = "\n".join(
        f"- `{omission.path}`: {omission.reason}"
        for omission in visible_omissions
    )
    if not omitted_lines:
        omitted_lines = "- No omissions recorded."
    elif remaining_omissions:
        omitted_lines += f"\n- ... plus {remaining_omissions} more omitted items not listed individually."
    return "\n".join(
        [
            "# Package Manifest",
            "",
            "## Package settings",
            "",
            f"- Title: {title.strip() or 'GPT Pro handoff'}",
            f"- Task: {task.strip()}",
            f"- Workspace: `{workspace}`",
            f"- Source file budget: {max_files}",
            f"- Soft size budget: {format_bytes(soft_max_bytes)}",
            f"- Created: {datetime.now().isoformat(timespec='seconds')}",
            "",
            "## Included source files",
            "",
            included_lines,
            "",
            "## Omitted or skipped items",
            "",
            omitted_lines,
            "",
            "## Default exclusions",
            "",
            "- Cache and build directories such as `.git`, `.venv`, `node_modules`, `dist`, `build`, and `coverage`",
            "- Archive and transient file types such as `.zip`, `.tar`, `.gz`, `.log`, `.tmp`, and compiled binaries",
            "",
        ]
    )


def write_text_file(path: Path, contents: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(contents, encoding="utf-8")


def copy_sources(staging_source_dir: Path, selected: list[Candidate]) -> None:
    for candidate in selected:
        destination = staging_source_dir / candidate.relative_path
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(candidate.source_path, destination)


def zip_directory(staging_dir: Path, zip_path: Path) -> None:
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for file_path in staging_dir.rglob("*"):
            if file_path.is_file():
                archive.write(file_path, file_path.relative_to(staging_dir.parent).as_posix())


def package_workspace(args: argparse.Namespace) -> dict[str, object]:
    workspace = Path(args.workspace).resolve()
    downloads_dir = Path(args.downloads_dir).resolve()
    downloads_dir.mkdir(parents=True, exist_ok=True)

    hard_file_limit_bytes = int(args.hard_file_mb * 1024 * 1024)
    soft_max_bytes = int(args.soft_max_mb * 1024 * 1024)

    candidates, initial_omissions = collect_candidates(
        workspace=workspace,
        include_paths=args.include,
        hard_file_limit_bytes=hard_file_limit_bytes,
    )
    staged_mode = looks_like_staged_package(candidates)
    effective_max_files = args.max_files
    if staged_mode and args.max_files == DEFAULT_MAX_FILES:
        effective_max_files = max(args.max_files, DEFAULT_STAGED_MAX_FILES)

    selected, selection_omissions = choose_candidates(
        candidates=candidates,
        max_files=effective_max_files,
        soft_max_bytes=soft_max_bytes,
        staged_mode=staged_mode,
    )
    omissions = initial_omissions + selection_omissions
    visible_omissions, remaining_omissions = compress_omissions(omissions)

    title = args.title.strip()
    expected_output = args.expected_output.strip()
    prompt_text = build_prompt(
        task=args.task,
        selected=selected,
        instructions=args.instruction,
        expected_output=expected_output,
    )
    brief_text = build_brief(
        task=args.task,
        title=title,
        workspace=workspace,
        selected=selected,
        instructions=args.instruction,
        omitted=omissions,
    )
    manifest_text = build_manifest(
        task=args.task,
        title=title,
        workspace=workspace,
        selected=selected,
        omitted=omissions,
        max_files=effective_max_files,
        soft_max_bytes=soft_max_bytes,
    )

    output_stem = unique_output_stem(downloads_dir, title=title, task=args.task)
    staging_dir = downloads_dir / output_stem
    staging_source_dir = staging_dir / "source"
    zip_path = downloads_dir / f"{output_stem}.zip"
    prompt_path = downloads_dir / f"{output_stem}_prompt.txt"

    write_text_file(staging_dir / "handoff_brief.md", brief_text)
    write_text_file(staging_dir / "handoff_prompt.txt", prompt_text)
    write_text_file(staging_dir / "package_manifest.md", manifest_text)
    write_text_file(prompt_path, prompt_text)
    copy_sources(staging_source_dir, selected)
    zip_directory(staging_dir, zip_path)

    return {
        "title": title or "GPT Pro handoff",
        "task": args.task,
        "workspace": str(workspace),
        "zip_path": str(zip_path),
        "prompt_path": str(prompt_path),
        "staging_dir": str(staging_dir),
        "selected_files": [candidate.relative_path.as_posix() for candidate in selected],
        "selected_file_count": len(selected),
        "selected_total_bytes": sum(candidate.size_bytes for candidate in selected),
        "omissions": [{"path": omission.path, "reason": omission.reason} for omission in visible_omissions],
        "omitted_item_count": len(omissions),
        "additional_omitted_item_count": remaining_omissions,
        "warnings": [omission.reason for omission in visible_omissions[:8]],
        "prompt_text": prompt_text,
    }


def print_human_summary(summary: dict[str, object]) -> None:
    selected_files = summary["selected_files"]
    omissions = summary["omissions"]
    print(f"Created zip: {summary['zip_path']}")
    print(f"Prompt file: {summary['prompt_path']}")
    print(
        f"Included {summary['selected_file_count']} source files "
        f"({format_bytes(int(summary['selected_total_bytes']))})."
    )
    if selected_files:
        print("Included sources:")
        for relative_path in selected_files:
            print(f"- {relative_path}")
    if omissions:
        print("Warnings:")
        for omission in omissions[:6]:
            print(f"- {omission['path']}: {omission['reason']}")
    print("\nGPT Pro prompt:\n")
    print(summary["prompt_text"].rstrip())


def main() -> int:
    args = parse_args()
    summary = package_workspace(args)
    if args.json:
        print(json.dumps(summary, indent=2))
    else:
        print_human_summary(summary)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
