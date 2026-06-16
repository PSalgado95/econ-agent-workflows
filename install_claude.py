#!/usr/bin/env python3
"""Install the generated Claude Code package into a local Claude configuration.

Run build_claude.py first (Codex is the source of truth). This script copies the
committed claude/ tree into ~/.claude: skills, slash commands, reviewer
subagents, and shared references.
"""

from __future__ import annotations

import argparse
import filecmp
import os
import shutil
from pathlib import Path


def is_within(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False


def copy_tree(source: Path, destination: Path, *, force: bool, root: Path) -> str:
    if destination.exists():
        if not force:
            return f"skipped existing {destination}"
        if not is_within(destination, root):
            raise RuntimeError(f"Refusing to replace path outside Claude home: {destination}")
        shutil.rmtree(destination)
    shutil.copytree(source, destination)
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


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Install the generated Claude Code skills, commands, reviewer agents, and protocol."
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
        help="Replace existing installed copies of these skills, commands, agents, and protocol.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo = Path(__file__).resolve().parent
    package = repo / "claude"
    if not package.exists():
        raise SystemExit("claude/ not found. Run `python build_claude.py` first.")

    claude_home = args.claude_home.expanduser().resolve()
    skills_dir = claude_home / "skills"
    commands_dir = claude_home / "commands"
    agents_dir = claude_home / "agents"
    references_dir = claude_home / "references" / "econ-agent-workflows"

    for directory in (skills_dir, commands_dir, agents_dir, references_dir):
        directory.mkdir(parents=True, exist_ok=True)

    messages: list[str] = []

    for skill in sorted(p for p in (package / "skills").iterdir() if p.is_dir()):
        messages.append(
            copy_tree(skill, skills_dir / skill.name, force=args.force, root=claude_home)
        )

    for command in sorted((package / "commands").glob("*.md")):
        messages.append(
            copy_file(command, commands_dir / command.name, force=args.force, root=claude_home)
        )

    for agent in sorted((package / "agents").glob("*.md")):
        messages.append(
            copy_file(agent, agents_dir / agent.name, force=args.force, root=claude_home)
        )

    for reference in sorted((package / "references" / "econ-agent-workflows").glob("*.md")):
        messages.append(
            copy_file(
                reference,
                references_dir / reference.name,
                force=args.force,
                root=claude_home,
            )
        )

    print("econ-agent-workflows install (Claude Code)")
    print(f"Claude home: {claude_home}")
    for message in messages:
        print(f"- {message}")
    print("\nRestart Claude Code to load the skills, commands, and reviewer agents.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
