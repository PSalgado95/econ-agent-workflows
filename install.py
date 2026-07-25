#!/usr/bin/env python3
"""Install econ-agent-workflows into a local Codex configuration."""

from __future__ import annotations

import argparse
import filecmp
import os
import shutil
from pathlib import Path


# The public package is seven core workflows plus one explicitly invoked
# auxiliary handoff. build_claude.py imports these tuples so both runtimes stay
# in lockstep.
CORE_SKILLS = (
    ("econ-brainstorm", "econ-brainstorm"),
    ("econ-plan", "econ-plan"),
    ("econ-work", "econ-work"),
    ("econ-review", "econ-review"),
    ("econ-debug", "econ-debug"),
    ("econ-lfg", "econ-lfg"),
    ("econ-compound", "econ-compound"),
)

AUXILIARY_SKILLS = (("auxiliary/gpt-pro-handoff", "gpt-pro-handoff"),)
SKILLS = CORE_SKILLS + AUXILIARY_SKILLS

# Exact package-owned reviewer registrations retired by the persona-runtime
# migration. Never replace this inventory with a glob, prefix, declared-name
# scan, or other inferred ownership rule.
STALE_AGENT_FILES = (
    "econ-bundle-reviewer.toml",
    "econ-claim-discipline-reviewer.toml",
    "econ-code-quality-reviewer.toml",
    "econ-cross-language-validation-reviewer.toml",
    "econ-design-reviewer.toml",
    "econ-dynamics-reviewer.toml",
    "econ-estimation-practice-reviewer.toml",
    "econ-hybrid-implementation-reviewer.toml",
    "econ-inference-reviewer.toml",
    "econ-output-consistency-reviewer.toml",
    "econ-output-perception-reviewer.toml",
    "econ-provenance-reviewer.toml",
    "econ-reproducibility-reviewer.toml",
    "econ-robustness-reviewer.toml",
    "econ-software-equivalence-reviewer.toml",
    "econ-specification-reviewer.toml",
    "econ-transformation-sample-reviewer.toml",
    "econ-reviewer.toml",
)

# Separate exact inventories for other package-owned surfaces retired by prior
# releases. In particular, ssj-code-taste.md and every unknown file are not
# stale and must survive a forced upgrade.
STALE_SKILL_DIRS = ("econ-reviewer",)
STALE_REFERENCE_FILES = (
    "code-taste.md",
    "code-taste-preference-log.md",
    "r-research-code.md",
    "reviewer-protocol.md",
    "research-code-quality.md",
    "r-defaults.md",
)


def is_within(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False


def copy_tree(
    source: Path,
    destination: Path,
    *,
    force: bool,
    root: Path,
    home_label: str = "Codex",
) -> str:
    if destination.exists():
        if not force:
            return f"skipped existing {destination}"
        if not is_within(destination, root):
            raise RuntimeError(
                f"Refusing to replace path outside {home_label} home: {destination}"
            )
        shutil.rmtree(destination)
    shutil.copytree(
        source,
        destination,
        ignore=shutil.ignore_patterns("__pycache__", "*.pyc"),
    )
    return f"installed {destination}"


def copy_file(
    source: Path,
    destination: Path,
    *,
    force: bool,
    root: Path,
    home_label: str = "Codex",
) -> str:
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists():
        if filecmp.cmp(source, destination, shallow=False):
            return f"already current {destination}"
        if not force:
            return f"skipped existing {destination}"
        if not is_within(destination, root):
            raise RuntimeError(
                f"Refusing to replace path outside {home_label} home: {destination}"
            )
    shutil.copy2(source, destination)
    return f"installed {destination}"


def remove_stale_file(
    path: Path,
    *,
    root: Path,
    label: str = "stale",
    home_label: str = "Codex",
) -> str | None:
    """Remove one exact package-owned stale file under the install root."""
    if not path.exists():
        return None
    if not path.is_file():
        return f"skipped {label} non-file {path}"
    if not is_within(path, root):
        raise RuntimeError(
            f"Refusing to remove path outside {home_label} home: {path}"
        )
    path.unlink()
    return f"removed {label} {path}"


def remove_stale_tree(path: Path, *, root: Path) -> str | None:
    """Remove one exact package-owned stale directory under the install root."""
    if not is_within(path, root):
        raise RuntimeError(f"Refusing to remove path outside install root: {path}")
    try:
        shutil.rmtree(path)
    except FileNotFoundError:
        return None
    except NotADirectoryError:
        return f"skipped stale non-directory {path}"
    return f"removed stale {path}"


def remove_empty_directory(path: Path, *, root: Path) -> None:
    """Remove an empty package directory without touching retained contents."""
    if not path.is_dir() or any(path.iterdir()):
        return
    if not is_within(path, root):
        raise RuntimeError(f"Refusing to remove path outside install root: {path}")
    path.rmdir()


def source_agents(repo: Path) -> tuple[Path, ...]:
    """Return current non-retired source agents, failing on stale source."""
    agents_dir = repo / ".codex" / "agents"
    agents = tuple(sorted(agents_dir.glob("*.toml"))) if agents_dir.is_dir() else ()
    stale = [path.name for path in agents if path.name in STALE_AGENT_FILES]
    if stale:
        raise RuntimeError(
            "Retired reviewer registrations remain in repository source: "
            + ", ".join(stale)
        )
    return agents


def source_references(repo: Path) -> tuple[Path, ...]:
    """Return current non-retired root references, failing on stale source."""
    references_dir = repo / "references"
    references = (
        tuple(sorted(references_dir.glob("*.md"))) if references_dir.is_dir() else ()
    )
    stale = [path.name for path in references if path.name in STALE_REFERENCE_FILES]
    if stale:
        raise RuntimeError(
            "Moved review contracts remain in repository root references: "
            + ", ".join(stale)
        )
    return references


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Install econ-agent-workflows skills and current package assets."
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
        help=(
            "Replace current package trees and remove only exact package-owned "
            "stale files and directories."
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


def main() -> int:
    args = parse_args()
    repo = Path(__file__).resolve().parent
    codex_home = args.codex_home.expanduser().resolve()

    skills_dir = codex_home / "skills"
    agents_dir = codex_home / "agents"
    references_dir = codex_home / "references" / "econ-agent-workflows"

    if args.check:
        from check_install import run_check

        return run_check(
            runtime="Codex",
            home=codex_home,
            skills_dir=skills_dir,
            agents_dir=agents_dir,
            references_dir=references_dir,
            check_generated=False,
            repo=repo,
        )

    # Validate repository ownership boundaries before mutating the target.
    current_agents = source_agents(repo)
    current_references = source_references(repo)

    skills_dir.mkdir(parents=True, exist_ok=True)
    messages: list[str] = []
    skills = CORE_SKILLS if args.skip_auxiliary else SKILLS
    for source_name, installed_name in skills:
        messages.append(
            copy_tree(
                repo / "skills" / source_name,
                skills_dir / installed_name,
                force=args.force,
                root=codex_home,
            )
        )

    for agent in current_agents:
        messages.append(
            copy_file(
                agent,
                agents_dir / agent.name,
                force=args.force,
                root=codex_home,
            )
        )

    for reference in current_references:
        messages.append(
            copy_file(
                reference,
                references_dir / reference.name,
                force=args.force,
                root=codex_home,
            )
        )

    if args.force:
        if args.skip_auxiliary:
            message = remove_stale_tree(
                skills_dir / AUXILIARY_SKILLS[0][1],
                root=codex_home,
            )
            if message:
                messages.append(message)
        for stale in STALE_SKILL_DIRS:
            message = remove_stale_tree(skills_dir / stale, root=codex_home)
            if message:
                messages.append(message)
        for stale in STALE_AGENT_FILES:
            message = remove_stale_file(agents_dir / stale, root=codex_home)
            if message:
                messages.append(message)
        for stale in STALE_REFERENCE_FILES:
            message = remove_stale_file(references_dir / stale, root=codex_home)
            if message:
                messages.append(message)
        remove_empty_directory(references_dir, root=codex_home)

    print("econ-agent-workflows install")
    print(f"Codex home: {codex_home}")
    for message in messages:
        print(f"- {message}")
    print("\nRestart Codex to load the installed skills.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
