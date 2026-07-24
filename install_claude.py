#!/usr/bin/env python3
"""Install the generated, directly invocable Claude Code skill package."""

from __future__ import annotations

import argparse
import filecmp
import os
import shutil
from pathlib import Path

from install import (
    AUXILIARY_SKILLS,
    CORE_SKILLS,
    STALE_AGENT_FILES,
    STALE_REFERENCE_FILES,
    STALE_SKILL_DIRS,
    is_within,
    remove_empty_directory,
    remove_stale_tree,
)

AUXILIARY_NAMES = frozenset(name for _source, name in AUXILIARY_SKILLS)

# Exact historical command-wrapper inventory. Generated Claude skills are now
# directly invocable; no command wrapper is current.
STALE_COMMAND_FILES = (
    "econ-brainstorm.md",
    "econ-plan.md",
    "econ-work.md",
    "econ-review.md",
    "econ-debug.md",
    "econ-lfg.md",
    "econ-compound.md",
    "gpt-pro-handoff.md",
    "econ-html-memo.md",
    "econ-explain.md",
    "econ-svg-fig.md",
)


def stale_claude_agent_name(codex_filename: str) -> str:
    """Deterministically map a retired Codex filename to Claude."""
    return Path(codex_filename).stem.replace("-", "_") + ".md"


STALE_CLAUDE_AGENT_FILES = tuple(
    stale_claude_agent_name(filename) for filename in STALE_AGENT_FILES
)


def copy_tree(source: Path, destination: Path, *, force: bool, root: Path) -> str:
    if destination.exists():
        if not force:
            return f"skipped existing {destination}"
        if not is_within(destination, root):
            raise RuntimeError(f"Refusing to replace path outside Claude home: {destination}")
        shutil.rmtree(destination)
    shutil.copytree(
        source,
        destination,
        ignore=shutil.ignore_patterns("__pycache__", "*.pyc"),
    )
    return f"installed {destination}"


def copy_file(source: Path, destination: Path, *, force: bool, root: Path) -> str:
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists():
        if filecmp.cmp(source, destination, shallow=False):
            return f"already current {destination}"
        if not force:
            return f"skipped existing {destination}"
        if not is_within(destination, root):
            raise RuntimeError(f"Refusing to replace path outside Claude home: {destination}")
    shutil.copy2(source, destination)
    return f"installed {destination}"


def remove_stale_file(path: Path, *, root: Path, label: str = "stale") -> str | None:
    if not path.exists():
        return None
    if not path.is_file():
        return f"skipped {label} non-file {path}"
    if not is_within(path, root):
        raise RuntimeError(f"Refusing to remove path outside Claude home: {path}")
    path.unlink()
    return f"removed {label} {path}"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Install generated econ-agent-workflows skills for Claude Code."
    )
    parser.add_argument(
        "--claude-home",
        type=Path,
        default=Path(os.environ.get("CLAUDE_CONFIG_DIR", Path.home() / ".claude")),
        help="Claude configuration directory. Defaults to CLAUDE_CONFIG_DIR or ~/.claude.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help=(
            "Replace current package trees and remove only exact package-owned "
            "stale files, wrappers, and directories."
        ),
    )
    parser.add_argument(
        "--skip-auxiliary",
        action="store_true",
        help="Install only the seven core skills; skip gpt-pro-handoff.",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Report-only health check; mutate nothing and exit 1 on failure.",
    )
    return parser.parse_args()


def package_files(
    package: Path,
) -> tuple[tuple[Path, ...], tuple[Path, ...]]:
    """Preflight generated policy agents and root references."""
    agents_dir = package / "agents"
    agents = tuple(sorted(agents_dir.glob("*.md"))) if agents_dir.is_dir() else ()
    stale_agents = [
        path.name for path in agents if path.name in STALE_CLAUDE_AGENT_FILES
    ]
    if stale_agents:
        raise RuntimeError(
            "Retired reviewer registrations remain in generated package: "
            + ", ".join(stale_agents)
        )

    references_dir = package / "references" / "econ-agent-workflows"
    references = (
        tuple(sorted(references_dir.glob("*.md")))
        if references_dir.is_dir()
        else ()
    )
    stale_references = [
        path.name for path in references if path.name in STALE_REFERENCE_FILES
    ]
    if stale_references:
        raise RuntimeError(
            "Moved review contracts remain in generated root references: "
            + ", ".join(stale_references)
        )
    return agents, references


def main() -> int:
    args = parse_args()
    repo = Path(__file__).resolve().parent
    package = repo / "claude"
    claude_home = args.claude_home.expanduser().resolve()

    skills_dir = claude_home / "skills"
    commands_dir = claude_home / "commands"
    agents_dir = claude_home / "agents"
    references_dir = claude_home / "references" / "econ-agent-workflows"

    if args.check:
        from check_install import run_check

        return run_check(
            runtime="Claude Code",
            home=claude_home,
            skills_dir=skills_dir,
            agents_dir=agents_dir,
            references_dir=references_dir,
            check_generated=True,
            repo=repo,
        )

    if not package.is_dir():
        raise SystemExit("claude/ not found. Run `python build_claude.py` first.")

    current_agents, current_references = package_files(package)
    selected_skills = CORE_SKILLS if args.skip_auxiliary else CORE_SKILLS + AUXILIARY_SKILLS
    skill_sources: list[tuple[Path, str]] = []
    for _source_name, installed_name in selected_skills:
        source = package / "skills" / installed_name
        if not source.is_dir():
            raise RuntimeError(
                f"Generated skill is missing: {source}. Run `python build_claude.py`."
            )
        skill_sources.append((source, installed_name))

    skills_dir.mkdir(parents=True, exist_ok=True)
    messages: list[str] = []
    for source, installed_name in skill_sources:
        messages.append(
            copy_tree(
                source,
                skills_dir / installed_name,
                force=args.force,
                root=claude_home,
            )
        )

    for agent in current_agents:
        messages.append(
            copy_file(
                agent,
                agents_dir / agent.name,
                force=args.force,
                root=claude_home,
            )
        )
    for reference in current_references:
        messages.append(
            copy_file(
                reference,
                references_dir / reference.name,
                force=args.force,
                root=claude_home,
            )
        )

    if args.force:
        for stale in STALE_SKILL_DIRS:
            message = remove_stale_tree(skills_dir / stale, root=claude_home)
            if message:
                messages.append(message)
        for stale in STALE_COMMAND_FILES:
            message = remove_stale_file(
                commands_dir / stale,
                root=claude_home,
                label="stale command wrapper",
            )
            if message:
                messages.append(message)
        for stale in STALE_CLAUDE_AGENT_FILES:
            message = remove_stale_file(agents_dir / stale, root=claude_home)
            if message:
                messages.append(message)
        for stale in STALE_REFERENCE_FILES:
            message = remove_stale_file(references_dir / stale, root=claude_home)
            if message:
                messages.append(message)
        remove_empty_directory(commands_dir, root=claude_home)
        remove_empty_directory(references_dir, root=claude_home)

    print("econ-agent-workflows install (Claude Code)")
    print(f"Claude home: {claude_home}")
    for message in messages:
        print(f"- {message}")
    if args.skip_auxiliary:
        print("- skipped auxiliary skill gpt-pro-handoff")
    print("\nRestart Claude Code to load the installed skills.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
