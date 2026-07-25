#!/usr/bin/env python3
"""Read-only health check for Codex and Claude Code installations."""

from __future__ import annotations

import argparse
import hashlib
import os
import subprocess
import sys
from pathlib import Path

from install import (
    AUXILIARY_SKILLS,
    CORE_SKILLS,
    STALE_AGENT_FILES,
    STALE_REFERENCE_FILES,
    STALE_SKILL_DIRS,
    enforce_live_release_gate,
    is_default_runtime_home,
    source_agents,
    source_references,
)


def tree_manifest(root: Path) -> dict[str, str]:
    """Return exact relative-file hashes for a package-owned tree."""
    manifest: dict[str, str] = {}
    if not root.is_dir():
        return manifest
    for path in sorted(item for item in root.rglob("*") if item.is_file()):
        relative = path.relative_to(root)
        if "__pycache__" in relative.parts or path.suffix == ".pyc":
            continue
        manifest[relative.as_posix()] = hashlib.sha256(path.read_bytes()).hexdigest()
    return manifest


def tree_status(source: Path, installed: Path) -> tuple[bool, str]:
    """Compare complete trees, including schemas and nested persona assets."""
    if not source.is_dir():
        return False, f"source tree missing ({source})"
    if not installed.is_dir():
        return False, f"installed tree missing ({installed})"
    expected = tree_manifest(source)
    actual = tree_manifest(installed)
    missing = sorted(set(expected) - set(actual))
    extra = sorted(set(actual) - set(expected))
    changed = sorted(
        path
        for path in set(expected) & set(actual)
        if expected[path] != actual[path]
    )
    if not (missing or extra or changed):
        return True, f"complete tree current ({len(expected)} files; {installed})"
    parts: list[str] = []
    if missing:
        parts.append(f"missing {len(missing)} [{', '.join(missing[:3])}]")
    if changed:
        parts.append(f"changed {len(changed)} [{', '.join(changed[:3])}]")
    if extra:
        parts.append(f"extra {len(extra)} [{', '.join(extra[:3])}]")
    return False, f"tree differs ({'; '.join(parts)}; {installed})"


def files_status(source: Path, installed: Path) -> tuple[bool, str]:
    if not source.is_file():
        return False, f"source file missing ({source})"
    if not installed.is_file():
        return False, f"installed file missing ({installed})"
    if source.read_bytes() != installed.read_bytes():
        return False, f"installed file differs ({installed})"
    return True, f"current ({installed})"


def _current_package_files(
    runtime: str, repo: Path
) -> tuple[tuple[Path, ...], tuple[Path, ...]]:
    if runtime == "Claude Code":
        package = repo / "claude"
        agents_dir = package / "agents"
        references_dir = package / "references" / "econ-agent-workflows"
        agents = (
            tuple(sorted(agents_dir.glob("*.md"))) if agents_dir.is_dir() else ()
        )
        references = (
            tuple(sorted(references_dir.glob("*.md")))
            if references_dir.is_dir()
            else ()
        )
        return agents, references
    return source_agents(repo), source_references(repo)


def _stale_agent_names(runtime: str) -> tuple[str, ...]:
    if runtime != "Claude Code":
        return STALE_AGENT_FILES
    from install_claude import stale_claude_agent_name

    return tuple(stale_claude_agent_name(filename) for filename in STALE_AGENT_FILES)


def run_check(
    *,
    runtime: str,
    home: Path,
    skills_dir: Path,
    agents_dir: Path,
    references_dir: Path,
    check_generated: bool,
    repo: Path,
    release_gate: Path | None = None,
) -> int:
    """Check a runtime install without creating, deleting, or replacing files."""
    is_claude = runtime == "Claude Code"
    source_skills = repo / "claude" / "skills" if is_claude else repo / "skills"
    results: list[tuple[bool, str]] = []

    for source_name, installed_name in CORE_SKILLS:
        source = (
            source_skills / installed_name
            if is_claude
            else source_skills / source_name
        )
        ok, detail = tree_status(source, skills_dir / installed_name)
        results.append((ok, f"core skill '{installed_name}': {detail}"))

    for source_name, installed_name in AUXILIARY_SKILLS:
        installed = skills_dir / installed_name
        if not installed.exists():
            continue
        source = (
            source_skills / installed_name
            if is_claude
            else source_skills / source_name
        )
        ok, detail = tree_status(source, installed)
        results.append((ok, f"installed auxiliary skill '{installed_name}': {detail}"))

    for stale in STALE_SKILL_DIRS:
        path = skills_dir / stale
        results.append(
            (not path.exists(), f"retired skill directory absent ({path})")
        )

    current_agents, current_references = _current_package_files(runtime, repo)
    for source in current_agents:
        ok, detail = files_status(source, agents_dir / source.name)
        results.append((ok, f"current policy agent '{source.name}': {detail}"))
    for stale in _stale_agent_names(runtime):
        path = agents_dir / stale
        results.append(
            (not path.exists(), f"retired reviewer registration absent ({path})")
        )

    for source in current_references:
        ok, detail = files_status(source, references_dir / source.name)
        results.append((ok, f"current root reference '{source.name}': {detail}"))
    for stale in STALE_REFERENCE_FILES:
        path = references_dir / stale
        results.append((not path.exists(), f"moved root contract absent ({path})"))

    if is_claude:
        from install_claude import STALE_COMMAND_FILES

        commands_dir = home / "commands"
        for stale in STALE_COMMAND_FILES:
            path = commands_dir / stale
            results.append(
                (not path.exists(), f"retired command wrapper absent ({path})")
            )

    if check_generated:
        process = subprocess.run(
            [sys.executable, str(repo / "build_claude.py"), "--check"],
            capture_output=True,
            text=True,
        )
        ok = process.returncode == 0
        detail = "generated claude/ tree current and deny-list clean"
        if not ok:
            output = (process.stdout + process.stderr).strip().splitlines()
            tail = output[-1] if output else "no build output"
            detail = (
                "generated claude/ tree stale or deny-list dirty; "
                f"run `python build_claude.py` ({tail})"
            )
        results.append((ok, detail))

    print(f"econ-agent-workflows install health check ({runtime})")
    for ok, message in results:
        print(f"  [{'PASS' if ok else 'FAIL'}] {message}")

    failures = [message for ok, message in results if not ok]
    if failures:
        if is_default_runtime_home(home, runtime):
            try:
                enforce_live_release_gate(
                    runtime=runtime,
                    home=home,
                    force=True,
                    release_gate=release_gate,
                    repo=repo,
                )
            except RuntimeError as error:
                print(
                    f"\n{len(failures)} check(s) failed. Live repair is "
                    f"release-gated and remains blocked:\n  {error}"
                )
                print(
                    "Run the trusted agent-native smoke with a durable result, "
                    "accept the SSJ adapter, and assemble an "
                    "econ-agent-workflows-release-gate/v1 receipt bound to this HEAD."
                )
                return 1
        repair = (
            f"python install_claude.py --claude-home \"{home}\" --force"
            if is_claude
            else f"python install.py --codex-home \"{home}\" --force"
        )
        if release_gate is not None:
            repair += f' --release-gate "{release_gate.expanduser().resolve()}"'
        print(f"\n{len(failures)} check(s) failed. Exact repair command:")
        print(f"  {repair}")
        return 1
    print("\nAll checks passed.")
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Check an installed workflow package.")
    parser.add_argument(
        "--runtime",
        choices=("codex", "claude"),
        default="codex",
        help="Runtime to check; defaults to Codex.",
    )
    parser.add_argument(
        "--home",
        type=Path,
        help="Runtime home. Defaults to CODEX_HOME/CLAUDE_CONFIG_DIR or the user home.",
    )
    parser.add_argument(
        "--release-gate",
        type=Path,
        help="Checkout-bound release receipt for an authorized live repair.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo = Path(__file__).resolve().parent
    is_claude = args.runtime == "claude"
    default = (
        Path(os.environ.get("CLAUDE_CONFIG_DIR", Path.home() / ".claude"))
        if is_claude
        else Path(os.environ.get("CODEX_HOME", Path.home() / ".codex"))
    )
    home = (args.home or default).expanduser().resolve()
    return run_check(
        runtime="Claude Code" if is_claude else "Codex",
        home=home,
        skills_dir=home / "skills",
        agents_dir=home / "agents",
        references_dir=home / "references" / "econ-agent-workflows",
        check_generated=is_claude,
        repo=repo,
        release_gate=args.release_gate,
    )


if __name__ == "__main__":
    raise SystemExit(main())
