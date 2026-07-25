#!/usr/bin/env python3
"""Install econ-agent-workflows into a local Codex configuration."""

from __future__ import annotations

import argparse
import filecmp
import hashlib
import json
import os
import re
import shutil
import subprocess
from pathlib import Path
from typing import Any

from release_gate import (
    AGENT_NATIVE_PROOF_VERSION,
    RELEASE_GATE_VERSION,
    RELEASE_SCENARIOS,
    SSJ_ACCEPTANCE_VERSION,
    TRUSTED_SMOKE_ADAPTER_SHA256,
)


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

HEX_40_OR_64 = re.compile(r"^[0-9a-f]{40}(?:[0-9a-f]{24})?$")
HEX_64 = re.compile(r"^[0-9a-f]{64}$")

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


def default_runtime_homes(runtime: str) -> frozenset[Path]:
    """Return configured and conventional live homes for one runtime."""
    if runtime == "Claude Code":
        configured = Path(
            os.environ.get("CLAUDE_CONFIG_DIR", Path.home() / ".claude")
        )
        conventional = Path.home() / ".claude"
    else:
        configured = Path(os.environ.get("CODEX_HOME", Path.home() / ".codex"))
        conventional = Path.home() / ".codex"
    return frozenset(
        path.expanduser().resolve() for path in (configured, conventional)
    )


def is_default_runtime_home(home: Path, runtime: str) -> bool:
    return home.expanduser().resolve() in default_runtime_homes(runtime)


def _git(
    repo: Path, *arguments: str, text: bool = True
) -> subprocess.CompletedProcess[Any]:
    safe_repo = repo.resolve().as_posix()
    return subprocess.run(
        [
            "git",
            "-c",
            f"safe.directory={safe_repo}",
            "-C",
            str(repo.resolve()),
            *arguments,
        ],
        capture_output=True,
        check=False,
        text=text,
    )


def checkout_head(repo: Path) -> str:
    process = _git(repo, "rev-parse", "HEAD")
    head = process.stdout.strip()
    if process.returncode or not HEX_40_OR_64.fullmatch(head):
        raise RuntimeError("Cannot identify the checkout HEAD for release gating.")
    return head


def checkout_source_sha256(repo: Path) -> str:
    """Hash the deterministic tracked tree used by the smoke release proof."""
    process = _git(repo, "archive", "--format=tar", "HEAD", text=False)
    if process.returncode:
        raise RuntimeError(
            "Cannot archive the checkout HEAD for release gating."
        )
    return hashlib.sha256(process.stdout).hexdigest()


def package_source_changes(repo: Path) -> tuple[str, ...]:
    """Return tracked/untracked changes that can alter installed package bytes."""
    paths = (
        "skills",
        ".codex/agents",
        "references",
        "claude",
        "install.py",
        "install_claude.py",
        "check_install.py",
        "build_claude.py",
        "release_gate.py",
    )
    process = _git(
        repo,
        "status",
        "--porcelain=v1",
        "--untracked-files=all",
        "--",
        *paths,
    )
    if process.returncode:
        raise RuntimeError(
            "Cannot verify that package-owned checkout sources are clean."
        )
    return tuple(line for line in process.stdout.splitlines() if line.strip())


def _object(
    value: object, *, label: str, keys: frozenset[str]
) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise RuntimeError(f"Release gate {label} must be an object.")
    actual = frozenset(value)
    if actual != keys:
        missing = ", ".join(sorted(keys - actual)) or "none"
        extra = ", ".join(sorted(actual - keys)) or "none"
        raise RuntimeError(
            f"Release gate {label} has invalid keys "
            f"(missing: {missing}; extra: {extra})."
        )
    return value


def _sha256(value: object, *, label: str) -> str:
    if not isinstance(value, str) or not HEX_64.fullmatch(value):
        raise RuntimeError(f"Release gate {label} must be a lowercase SHA-256.")
    return value


def _validate_integrity_map(value: object, *, label: str) -> None:
    if not isinstance(value, dict) or not value:
        raise RuntimeError(f"Release gate {label} must be a non-empty object.")
    for name, digest in value.items():
        if not isinstance(name, str) or not name:
            raise RuntimeError(f"Release gate {label} has an invalid path.")
        _sha256(digest, label=f"{label}.{name}")


def validate_release_gate(path: Path, repo: Path) -> dict[str, Any]:
    """Validate release evidence against the exact checkout being installed."""
    try:
        payload = json.loads(path.expanduser().read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
        raise RuntimeError(
            f"Cannot read release-gate receipt {path}: {type(error).__name__}."
        ) from error

    gate = _object(
        payload,
        label="receipt",
        keys=frozenset(
            {
                "schema_version",
                "checkout_head",
                "checkout_source_sha256",
                "agent_native",
                "ssj_adapter",
            }
        ),
    )
    if gate["schema_version"] != RELEASE_GATE_VERSION:
        raise RuntimeError("Release gate has an unsupported schema version.")

    expected_head = checkout_head(repo)
    expected_source = checkout_source_sha256(repo)
    if gate["checkout_head"] != expected_head:
        raise RuntimeError("Release gate is bound to a different checkout HEAD.")
    if gate["checkout_source_sha256"] != expected_source:
        raise RuntimeError("Release gate is bound to different checkout sources.")

    agent_native = _object(
        gate["agent_native"],
        label="agent_native",
        keys=frozenset(
            {
                "schema_version",
                "status",
                "host",
                "request_id",
                "checkout_head",
                "checkout_source_sha256",
                "trusted_adapter_sha256",
                "request_sha256",
                "runtime_integrity",
                "receipt_sha256",
                "scenarios",
                "workspace_unchanged",
                "created_at_utc",
            }
        ),
    )
    if (
        agent_native["schema_version"] != AGENT_NATIVE_PROOF_VERSION
        or agent_native["status"] != "passed"
        or agent_native["host"] != "codex"
        or agent_native["workspace_unchanged"] is not True
    ):
        raise RuntimeError("Agent-native release proof is not a passing Codex proof.")
    if not isinstance(agent_native["request_id"], str) or not agent_native["request_id"]:
        raise RuntimeError("Agent-native release proof has no request id.")
    if agent_native["checkout_head"] != expected_head:
        raise RuntimeError("Agent-native proof is bound to a different checkout HEAD.")
    if agent_native["checkout_source_sha256"] != expected_source:
        raise RuntimeError("Agent-native proof is bound to different checkout sources.")
    adapter = _sha256(
        agent_native["trusted_adapter_sha256"],
        label="agent_native.trusted_adapter_sha256",
    )
    if adapter not in TRUSTED_SMOKE_ADAPTER_SHA256["codex"]:
        raise RuntimeError(
            "Agent-native proof names an adapter digest that is not approved."
        )
    _sha256(agent_native["request_sha256"], label="agent_native.request_sha256")
    _sha256(agent_native["receipt_sha256"], label="agent_native.receipt_sha256")
    if (
        not isinstance(agent_native["scenarios"], list)
        or tuple(agent_native["scenarios"]) != RELEASE_SCENARIOS
    ):
        raise RuntimeError("Agent-native proof does not cover the canonical scenarios.")
    if (
        not isinstance(agent_native["created_at_utc"], str)
        or not agent_native["created_at_utc"].endswith("Z")
    ):
        raise RuntimeError("Agent-native proof has an invalid creation timestamp.")
    integrity = _object(
        agent_native["runtime_integrity"],
        label="agent_native.runtime_integrity",
        keys=frozenset({"protocols", "personas", "schemas"}),
    )
    for group in ("protocols", "personas", "schemas"):
        _validate_integrity_map(
            integrity[group],
            label=f"agent_native.runtime_integrity.{group}",
        )

    ssj = _object(
        gate["ssj_adapter"],
        label="ssj_adapter",
        keys=frozenset(
            {
                "schema_version",
                "status",
                "checkout_head",
                "checkout_source_sha256",
                "assessment_schema_version",
                "assessment_type",
                "retired_reviewer_requested",
                "integration_tests_passed",
                "evidence_sha256",
                "accepted_at_utc",
            }
        ),
    )
    if (
        ssj["schema_version"] != SSJ_ACCEPTANCE_VERSION
        or ssj["status"] != "accepted"
        or ssj["assessment_schema_version"] != "econ-domain-assessment/v1"
        or ssj["assessment_type"] != "ssj-model-validity"
        or ssj["retired_reviewer_requested"] is not False
        or ssj["integration_tests_passed"] is not True
    ):
        raise RuntimeError("SSJ adapter evidence is not accepted and contract-current.")
    if ssj["checkout_head"] != expected_head:
        raise RuntimeError("SSJ acceptance is bound to a different checkout HEAD.")
    if ssj["checkout_source_sha256"] != expected_source:
        raise RuntimeError("SSJ acceptance is bound to different checkout sources.")
    _sha256(ssj["evidence_sha256"], label="ssj_adapter.evidence_sha256")
    if (
        not isinstance(ssj["accepted_at_utc"], str)
        or not ssj["accepted_at_utc"].endswith("Z")
    ):
        raise RuntimeError("SSJ acceptance has an invalid timestamp.")
    return gate


def enforce_live_release_gate(
    *, runtime: str, home: Path, force: bool, release_gate: Path | None, repo: Path
) -> None:
    """Block destructive live upgrades without checkout-bound release proof."""
    if not force or not is_default_runtime_home(home, runtime):
        return
    if release_gate is None:
        raise RuntimeError(
            f"Refusing a forced install into the default {runtime} home: "
            "pass --release-gate with genuine agent-native and accepted SSJ evidence."
        )
    validate_release_gate(release_gate, repo)
    changes = package_source_changes(repo)
    if changes:
        preview = ", ".join(changes[:3])
        raise RuntimeError(
            "Refusing a live install from package sources that differ from "
            f"the gated checkout ({preview})."
        )


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
    parser.add_argument(
        "--release-gate",
        type=Path,
        help=(
            "Checkout-bound econ-agent-workflows-release-gate/v1 receipt. "
            "Required for --force into a default live runtime home."
        ),
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
            release_gate=args.release_gate,
        )

    try:
        enforce_live_release_gate(
            runtime="Codex",
            home=codex_home,
            force=args.force,
            release_gate=args.release_gate,
            repo=repo,
        )
    except RuntimeError as error:
        raise SystemExit(str(error)) from error

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
