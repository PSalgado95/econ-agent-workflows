#!/usr/bin/env python3
"""Install econ-agent-workflows into a local Codex configuration."""

from __future__ import annotations

import argparse
import filecmp
import os
import shutil
from pathlib import Path


SKILLS = (
    ("econ-plan", "econ-plan"),
    ("econ-work", "econ-work"),
    ("econ-review", "econ-review"),
    ("econ-compound", "econ-compound"),
    ("auxiliary/gpt-pro-handoff", "gpt-pro-handoff"),
)


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
            raise RuntimeError(f"Refusing to replace path outside Codex home: {destination}")
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
            raise RuntimeError(f"Refusing to replace path outside Codex home: {destination}")
    shutil.copy2(source, destination)
    return f"installed {destination}"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Install econ-agent-workflows skills, reviewer agents, and shared references."
    )
    parser.add_argument(
        "--codex-home",
        type=Path,
        default=Path(os.environ.get("CODEX_HOME", Path.home() / ".codex")),
        help="Codex configuration directory. Defaults to CODEX_HOME or ~/.codex.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Replace existing installed copies of these skills, agents, and shared references.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo = Path(__file__).resolve().parent
    codex_home = args.codex_home.expanduser().resolve()

    skills_dir = codex_home / "skills"
    agents_dir = codex_home / "agents"
    references_dir = codex_home / "references" / "econ-agent-workflows"

    for directory in (skills_dir, agents_dir, references_dir):
        directory.mkdir(parents=True, exist_ok=True)

    messages: list[str] = []

    for source_name, installed_name in SKILLS:
        messages.append(
            copy_tree(
                repo / "skills" / source_name,
                skills_dir / installed_name,
                force=args.force,
                root=codex_home,
            )
        )

    for agent in sorted((repo / ".codex" / "agents").glob("*.toml")):
        messages.append(
            copy_file(
                agent,
                agents_dir / agent.name,
                force=args.force,
                root=codex_home,
            )
        )

    for reference in sorted((repo / "references").glob("*.md")):
        messages.append(
            copy_file(
                reference,
                references_dir / reference.name,
                force=args.force,
                root=codex_home,
            )
        )

    print("econ-agent-workflows install")
    print(f"Codex home: {codex_home}")
    for message in messages:
        print(f"- {message}")
    print("\nRestart Codex to load the skills and reviewer agents.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
