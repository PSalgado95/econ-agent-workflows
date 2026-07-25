#!/usr/bin/env python3
"""Generate the committed Claude Code package from canonical Codex sources.

The generated package contains directly invocable skills, current non-retired
agent policy files when present, and current non-retired root references. It
never creates slash-command wrappers.
"""

from __future__ import annotations

import argparse
import re
import shutil
import tempfile
import tomllib
from pathlib import Path

from install import (
    AUXILIARY_SKILLS,
    CORE_SKILLS,
    source_agents,
    source_references,
)

SKILLS = CORE_SKILLS + AUXILIARY_SKILLS

BANNER = (
    "<!-- GENERATED FROM CODEX SOURCE - DO NOT EDIT. "
    "Edit the Codex sources and run build_claude.py. -->"
)
REVIEWER_MODEL = "inherit"
READ_ONLY_TOOLS = "Read, Grep, Glob"
DISABLE_MODEL_INVOCATION = frozenset({"econ-lfg", "gpt-pro-handoff"})

OVERRIDES: dict[tuple[str, str], str] = {
    ("econ-lfg", "## Goal-backed run"): (
        "## Goal-backed run\n"
        "\n"
        "Claude Code has no goal primitive. Persist the loop with the built-in "
        "task list: one task per stage (plan, work, review, revise, re-review, "
        "deliver), with statuses kept current as the run advances. The session "
        "is the persistence boundary—if it ends, the loop does not survive on "
        "its own. State in the closeout that persistence was session-local "
        "rather than goal-backed. Do not claim a goal was created.\n"
        "\n"
        "Treat the run as complete only when the final deliverable is produced "
        "and review-resolution is handled. Treat it as blocked only when the "
        "same user-level economics decision or external-access blocker prevents "
        "meaningful progress after repeated attempts.\n"
    ),
}

DENY_PATTERNS = (
    r"\bCodex\b",
    r"request_user_input",
    r"update_plan",
    r"\bAGENTS\.md\b",
    r"\.codex[\\/]",
    r"(?i)\bpedro\b",
    r"(?i)c:\\users",
)
SCANNED_SUFFIXES = (
    ".md",
    ".html",
    ".htm",
    ".py",
    ".cjs",
    ".js",
    ".yaml",
    ".yml",
    ".toml",
    ".txt",
)


def substitute(text: str) -> str:
    """Rewrite runtime-specific text for Claude Code."""
    names = "|".join(re.escape(name) for _source, name in SKILLS)
    text = re.sub(rf"\$({names})", r"/\1", text)
    text = text.replace("request_user_input", "AskUserQuestion")
    text = text.replace("`update_plan`", "the built-in task list")
    text = re.sub(r"\bAGENTS\.md\b", "CLAUDE.md", text)
    text = text.replace("~/.codex/", "~/.claude/")
    text = text.replace(".codex/agents/", "~/.claude/agents/")
    text = text.replace(".codex/", ".claude/")
    return re.sub(r"\bCodex\b", "Claude Code", text)


def deny_scan(out: Path) -> list[str]:
    violations: list[str] = []
    for path in sorted(out.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in SCANNED_SUFFIXES:
            continue
        if "__pycache__" in path.parts:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for lineno, line in enumerate(text.splitlines(), 1):
            if line.strip().startswith("<!-- GENERATED FROM CODEX SOURCE"):
                continue
            for pattern in DENY_PATTERNS:
                if re.search(pattern, line):
                    violations.append(
                        f"{path.relative_to(out)}:{lineno}: {pattern} :: "
                        f"{line.strip()[:100]}"
                    )
    return violations


def with_banner(text: str) -> str:
    lines = text.splitlines()
    if lines and lines[0].strip() == "---":
        for index in range(1, len(lines)):
            if lines[index].strip() == "---":
                lines[index + 1:index + 1] = ["", BANNER]
                return "\n".join(lines) + "\n"
    return BANNER + "\n\n" + text


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def apply_section_override(text: str, replacement: str) -> str:
    heading = replacement.splitlines()[0].strip()
    lines = text.splitlines()
    start = next(
        (index for index, line in enumerate(lines) if line.strip() == heading),
        None,
    )
    if start is None:
        raise ValueError(f"override heading not found: {heading!r}")
    end = next(
        (
            index
            for index in range(start + 1, len(lines))
            if lines[index].startswith("## ")
        ),
        len(lines),
    )
    body = replacement.rstrip("\n").splitlines()
    if end < len(lines) and lines[end].strip():
        body.append("")
    result = lines[:start] + body + lines[end:]
    return "\n".join(result) + ("\n" if text.endswith("\n") else "")


def inject_frontmatter(text: str, additions: dict[str, str]) -> str:
    lines = text.splitlines()
    if not (lines and lines[0].strip() == "---"):
        raise ValueError("expected YAML frontmatter")
    close = next(
        (index for index in range(1, len(lines)) if lines[index].strip() == "---"),
        None,
    )
    if close is None:
        raise ValueError("unterminated YAML frontmatter")
    description = next(
        (
            index
            for index in range(1, close)
            if lines[index].startswith("description:")
        ),
        None,
    )
    at = description + 1 if description is not None else close
    lines[at:at] = [f"{key}: {value}" for key, value in additions.items()]
    return "\n".join(lines) + ("\n" if text.endswith("\n") else "")


def copy_skill(source: Path, destination: Path, installed_name: str) -> None:
    for item in sorted(source.rglob("*")):
        if item.is_dir():
            continue
        relative = item.relative_to(source)
        if relative.parts and relative.parts[0] == "agents":
            continue
        if "__pycache__" in relative.parts or item.suffix == ".pyc":
            continue
        target = destination / relative
        if item.suffix == ".md":
            text = substitute(item.read_text(encoding="utf-8"))
            if relative.as_posix() == "SKILL.md":
                for (skill, _heading), replacement in OVERRIDES.items():
                    if skill == installed_name:
                        text = apply_section_override(text, replacement)
                if installed_name in DISABLE_MODEL_INVOCATION:
                    text = inject_frontmatter(
                        text, {"disable-model-invocation": "true"}
                    )
            write(target, with_banner(text))
        elif item.suffix.lower() in SCANNED_SUFFIXES:
            write(target, substitute(item.read_text(encoding="utf-8")))
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(item, target)


def build_agent(source: Path, destination: Path) -> str:
    """Convert a current non-retired Codex agent policy to Claude format."""
    data = tomllib.loads(source.read_text(encoding="utf-8"))
    name = data["name"]
    description = data["description"].replace('"', "'")
    instructions = substitute(data["developer_instructions"].strip())
    lines = [
        "---",
        f"name: {name}",
        f'description: "{description}"',
        f"model: {REVIEWER_MODEL}",
    ]
    if data.get("sandbox_mode") == "read-only":
        lines.append(f"tools: {READ_ONLY_TOOLS}")
    lines.extend(["---", "", BANNER, "", instructions, ""])
    write(destination / f"{name}.md", "\n".join(lines))
    return name


def build_tree(repo: Path, out: Path) -> tuple[list[str], list[str], list[str]]:
    if out.exists():
        shutil.rmtree(out)
    skills_out = out / "skills"
    skill_names: list[str] = []
    for source_name, installed_name in SKILLS:
        copy_skill(
            repo / "skills" / source_name,
            skills_out / installed_name,
            installed_name,
        )
        skill_names.append(installed_name)

    agent_names: list[str] = []
    for agent in source_agents(repo):
        agent_names.append(build_agent(agent, out / "agents"))

    reference_names: list[str] = []
    for reference in source_references(repo):
        write(
            out / "references" / "econ-agent-workflows" / reference.name,
            with_banner(substitute(reference.read_text(encoding="utf-8"))),
        )
        reference_names.append(reference.name)
    return skill_names, agent_names, reference_names


def tree_digest(root: Path) -> dict[str, bytes]:
    digest: dict[str, bytes] = {}
    if not root.is_dir():
        return digest
    for path in sorted(item for item in root.rglob("*") if item.is_file()):
        if "__pycache__" in path.parts or path.suffix == ".pyc":
            continue
        raw = path.read_bytes().replace(b"\r\n", b"\n")
        digest[path.relative_to(root).as_posix()] = raw
    return digest


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate or verify the Claude Code package."
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Fail if committed claude/ differs from a fresh generated tree.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo = Path(__file__).resolve().parent
    committed = repo / "claude"

    if args.check:
        with tempfile.TemporaryDirectory() as temporary:
            fresh = Path(temporary) / "claude"
            build_tree(repo, fresh)
            violations = deny_scan(fresh)
            if violations:
                print("build_claude --check: deny-list violations:")
                for violation in violations:
                    print(f"  {violation}")
                return 1
            fresh_digest = tree_digest(fresh)
            committed_digest = tree_digest(committed)
            stale = sorted(
                set(fresh_digest) ^ set(committed_digest)
                | {
                    path
                    for path in set(fresh_digest) & set(committed_digest)
                    if fresh_digest[path] != committed_digest[path]
                }
            )
            if stale:
                print(
                    "build_claude --check: claude/ is STALE. "
                    "Run `python build_claude.py`:"
                )
                for path in stale:
                    print(f"  {path}")
                return 1
        print("build_claude --check: claude/ is current and deny-list clean.")
        return 0

    skill_names, agent_names, reference_names = build_tree(repo, committed)
    violations = deny_scan(committed)
    if violations:
        print("build_claude: FAILED deny-list scan:")
        for violation in violations:
            print(f"  {violation}")
        return 1

    print("build_claude: generated claude/ (deny-list clean)")
    print(f"- skills: {', '.join(skill_names)}")
    print(f"- current policy agents: {len(agent_names)}")
    print(f"- current root references: {len(reference_names)}")
    print("- command wrappers: 0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
