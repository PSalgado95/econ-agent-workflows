from __future__ import annotations

import hashlib
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

import install  # noqa: E402
import install_claude  # noqa: E402
import check_install  # noqa: E402


EXPECTED_STALE_AGENTS = (
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
EXPECTED_STALE_REFERENCES = (
    "code-taste.md",
    "code-taste-preference-log.md",
    "r-research-code.md",
    "reviewer-protocol.md",
    "research-code-quality.md",
    "r-defaults.md",
)
EXPECTED_STALE_COMMANDS = (
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


def file_digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def tree_digest(root: Path) -> dict[str, str]:
    if not root.is_dir():
        return {}
    return {
        path.relative_to(root).as_posix(): file_digest(path)
        for path in sorted(item for item in root.rglob("*") if item.is_file())
    }


class InstallContractsTest(unittest.TestCase):
    maxDiff = None

    @classmethod
    def setUpClass(cls) -> None:
        cls.environment = os.environ.copy()
        cls.environment["PYTHONDONTWRITEBYTECODE"] = "1"

    def run_script(
        self, script: str, *arguments: object, expected: int = 0
    ) -> subprocess.CompletedProcess[str]:
        process = subprocess.run(
            [sys.executable, str(REPO / script), *(str(arg) for arg in arguments)],
            cwd=REPO,
            env=self.environment,
            capture_output=True,
            text=True,
        )
        self.assertEqual(
            process.returncode,
            expected,
            msg=process.stdout + process.stderr,
        )
        return process

    def seed_home(self, root: Path, runtime: str) -> dict[str, str]:
        agents = root / "agents"
        references = root / "references" / "econ-agent-workflows"
        retired_skill = root / "skills" / "econ-reviewer"
        agents.mkdir(parents=True)
        references.mkdir(parents=True)
        retired_skill.mkdir(parents=True)
        (retired_skill / "legacy.txt").write_text("legacy", encoding="utf-8")

        if runtime == "codex":
            stale_agents = EXPECTED_STALE_AGENTS
            sentinels = {
                agents / "econ-review-readonly-transport.toml": "TRANSPORT",
                agents / "separately-owned-agent.toml": "EXTERNAL-AGENT",
                agents / "unrelated-agent.toml": "UNKNOWN-AGENT",
            }
        else:
            stale_agents = tuple(
                Path(name).stem.replace("-", "_") + ".md"
                for name in EXPECTED_STALE_AGENTS
            )
            sentinels = {
                agents / "econ_review_readonly_transport.md": "TRANSPORT",
                agents / "separately_owned_agent.md": "EXTERNAL-AGENT",
                agents / "unrelated_agent.md": "UNKNOWN-AGENT",
            }
        for name in stale_agents:
            (agents / name).write_text(f"stale:{name}", encoding="utf-8")
        for name in EXPECTED_STALE_REFERENCES:
            (references / name).write_text(f"stale:{name}", encoding="utf-8")

        sentinels.update(
            {
                references / "separately-owned-reference.md": "EXTERNAL-REFERENCE",
                references / "unknown-reference.md": "UNKNOWN-REFERENCE",
                root / "skills" / "unrelated-skill" / "sentinel.txt": "UNKNOWN-SKILL",
            }
        )
        if runtime == "claude":
            commands = root / "commands"
            commands.mkdir(parents=True)
            for name in EXPECTED_STALE_COMMANDS:
                (commands / name).write_text(
                    f"stale:{name}", encoding="utf-8"
                )
            sentinels[commands / "unrelated-command.md"] = "UNKNOWN-COMMAND"

        for path, contents in sentinels.items():
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(contents, encoding="utf-8")
        return {str(path): file_digest(path) for path in sentinels}

    def assert_sentinels_unchanged(self, expected: dict[str, str]) -> None:
        for raw_path, digest in expected.items():
            path = Path(raw_path)
            with self.subTest(path=path):
                self.assertTrue(path.is_file())
                self.assertEqual(file_digest(path), digest)

    def assert_stale_present(self, root: Path, runtime: str) -> None:
        names = (
            EXPECTED_STALE_AGENTS
            if runtime == "codex"
            else tuple(
                Path(name).stem.replace("-", "_") + ".md"
                for name in EXPECTED_STALE_AGENTS
            )
        )
        self.assertTrue(all((root / "agents" / name).is_file() for name in names))
        self.assertTrue(
            all(
                (root / "references" / "econ-agent-workflows" / name).is_file()
                for name in EXPECTED_STALE_REFERENCES
            )
        )
        self.assertTrue((root / "skills" / "econ-reviewer").is_dir())
        if runtime == "claude":
            self.assertTrue(
                all((root / "commands" / name).is_file() for name in EXPECTED_STALE_COMMANDS)
            )

    def assert_stale_absent(self, root: Path, runtime: str) -> None:
        names = (
            EXPECTED_STALE_AGENTS
            if runtime == "codex"
            else tuple(
                Path(name).stem.replace("-", "_") + ".md"
                for name in EXPECTED_STALE_AGENTS
            )
        )
        self.assertTrue(all(not (root / "agents" / name).exists() for name in names))
        self.assertTrue(
            all(
                not (
                    root / "references" / "econ-agent-workflows" / name
                ).exists()
                for name in EXPECTED_STALE_REFERENCES
            )
        )
        self.assertFalse((root / "skills" / "econ-reviewer").exists())
        if runtime == "claude":
            self.assertTrue(
                all(
                    not (root / "commands" / name).exists()
                    for name in EXPECTED_STALE_COMMANDS
                )
            )

    def test_exact_literal_stale_inventories_and_claude_mapping(self) -> None:
        self.assertEqual(install.STALE_AGENT_FILES, EXPECTED_STALE_AGENTS)
        self.assertEqual(len(set(install.STALE_AGENT_FILES)), 18)
        self.assertEqual(
            install_claude.STALE_CLAUDE_AGENT_FILES,
            tuple(
                Path(name).stem.replace("-", "_") + ".md"
                for name in EXPECTED_STALE_AGENTS
            ),
        )
        self.assertEqual(
            install.STALE_REFERENCE_FILES,
            EXPECTED_STALE_REFERENCES,
        )
        self.assertEqual(
            install_claude.STALE_COMMAND_FILES,
            EXPECTED_STALE_COMMANDS,
        )
        self.assertEqual(install.STALE_SKILL_DIRS, ("econ-reviewer",))

        explicitly_preserved = {
            "econ-review-readonly-transport.toml",
            "econ_review_readonly_transport.md",
            "separately-owned-agent.toml",
            "separately_owned_agent.md",
            "unrelated-agent.toml",
            "unrelated_agent.md",
        }
        self.assertTrue(
            explicitly_preserved.isdisjoint(install.STALE_AGENT_FILES)
        )
        self.assertTrue(
            explicitly_preserved.isdisjoint(
                install_claude.STALE_CLAUDE_AGENT_FILES
            )
        )

    def test_generated_tree_is_current_and_contains_only_direct_skills(self) -> None:
        self.run_script("build_claude.py", "--check")
        generated = REPO / "claude"
        expected_skills = {
            installed
            for _source, installed in install.CORE_SKILLS
            + install.AUXILIARY_SKILLS
        }
        self.assertEqual(
            {
                path.name
                for path in (generated / "skills").iterdir()
                if path.is_dir()
            },
            expected_skills,
        )
        self.assertFalse(any((generated / "agents").glob("*.md")))
        self.assertFalse(any((generated / "commands").glob("*.md")))
        self.assertFalse(
            any(
                (generated / "references" / "econ-agent-workflows").glob(
                    "*.md"
                )
            )
        )

    def test_fresh_codex_and_claude_installs_pass_full_tree_checks(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            codex = base / "codex"
            claude = base / "claude"
            self.run_script("install.py", "--codex-home", codex)
            self.run_script("install_claude.py", "--claude-home", claude)
            self.run_script("install.py", "--codex-home", codex, "--check")
            self.run_script(
                "install_claude.py", "--claude-home", claude, "--check"
            )

            expected = {
                installed
                for _source, installed in install.CORE_SKILLS
                + install.AUXILIARY_SKILLS
            }
            self.assertEqual(
                {path.name for path in (codex / "skills").iterdir()},
                expected,
            )
            self.assertEqual(
                {path.name for path in (claude / "skills").iterdir()},
                expected,
            )
            self.assertFalse(any((codex / "agents").glob("*")))
            self.assertFalse(any((claude / "agents").glob("*")))
            self.assertFalse(
                (codex / "references" / "econ-agent-workflows").exists()
            )
            self.assertFalse(
                (claude / "references" / "econ-agent-workflows").exists()
            )

    def test_full_tree_check_detects_and_repairs_a_missing_persona(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            cases = (
                ("install.py", "--codex-home", base / "codex"),
                ("install_claude.py", "--claude-home", base / "claude"),
            )
            for script, option, root in cases:
                with self.subTest(runtime=script):
                    self.run_script(script, option, root)
                    persona = (
                        root
                        / "skills"
                        / "econ-review"
                        / "references"
                        / "personas"
                        / "inference.md"
                    )
                    persona.unlink()
                    failure = self.run_script(
                        script, option, root, "--check", expected=1
                    )
                    self.assertIn("missing 1 [references/personas/inference.md]", failure.stdout)
                    self.assertIn("--force", failure.stdout)
                    self.run_script(script, option, root, "--force")
                    self.run_script(script, option, root, "--check")
                    self.assertTrue(persona.is_file())

    def run_seeded_migration(
        self, runtime: str, script: str, option: str
    ) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / runtime
            sentinel_hashes = self.seed_home(root, runtime)

            self.run_script(script, option, root)
            self.assert_stale_present(root, runtime)
            self.assert_sentinels_unchanged(sentinel_hashes)
            failed_check = self.run_script(
                script, option, root, "--check", expected=1
            )
            exact_repair = f'python {script} {option} "{root.resolve()}" --force'
            self.assertIn(exact_repair, failed_check.stdout)

            self.run_script(script, option, root, "--force")
            self.assert_stale_absent(root, runtime)
            self.assert_sentinels_unchanged(sentinel_hashes)
            first_force_digest = tree_digest(root)

            self.run_script(script, option, root, "--force")
            self.assertEqual(tree_digest(root), first_force_digest)
            self.assert_sentinels_unchanged(sentinel_hashes)
            self.run_script(script, option, root, "--check")

    def test_seeded_codex_migration_is_exact_and_idempotent(self) -> None:
        self.run_seeded_migration("codex", "install.py", "--codex-home")

    def test_seeded_claude_migration_is_exact_and_idempotent(self) -> None:
        self.run_seeded_migration(
            "claude", "install_claude.py", "--claude-home"
        )

    def test_auxiliary_skill_is_optional_but_checked_when_present(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            cases = (
                ("install.py", "--codex-home", base / "codex"),
                ("install_claude.py", "--claude-home", base / "claude"),
            )
            for script, option, root in cases:
                with self.subTest(runtime=script):
                    self.run_script(
                        script, option, root, "--skip-auxiliary"
                    )
                    self.assertFalse(
                        (root / "skills" / "gpt-pro-handoff").exists()
                    )
                    self.run_script(script, option, root, "--check")

    def test_force_skip_auxiliary_removes_only_exact_owned_tree(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            cases = (
                ("install.py", "--codex-home", base / "codex"),
                ("install_claude.py", "--claude-home", base / "claude"),
            )
            for script, option, root in cases:
                with self.subTest(runtime=script):
                    self.run_script(script, option, root)
                    auxiliary = root / "skills" / "gpt-pro-handoff"
                    self.assertTrue(auxiliary.is_dir())
                    unrelated = root / "skills" / "gpt-pro-handoff-local"
                    unrelated.mkdir(parents=True)
                    sentinel = unrelated / "sentinel.txt"
                    sentinel.write_text("preserve\n", encoding="utf-8")

                    self.run_script(
                        script, option, root, "--skip-auxiliary"
                    )
                    self.assertTrue(auxiliary.is_dir())
                    self.assertEqual(
                        sentinel.read_text(encoding="utf-8"), "preserve\n"
                    )

                    self.run_script(
                        script,
                        option,
                        root,
                        "--force",
                        "--skip-auxiliary",
                    )
                    self.assertFalse(auxiliary.exists())
                    self.assertEqual(
                        sentinel.read_text(encoding="utf-8"), "preserve\n"
                    )

    def test_force_skip_auxiliary_removes_seeded_legacy_tree(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            cases = (
                ("install.py", "--codex-home", base / "codex"),
                ("install_claude.py", "--claude-home", base / "claude"),
            )
            for script, option, root in cases:
                with self.subTest(runtime=script):
                    auxiliary = root / "skills" / "gpt-pro-handoff"
                    auxiliary.mkdir(parents=True)
                    (auxiliary / "legacy.txt").write_text(
                        "legacy\n", encoding="utf-8"
                    )

                    self.run_script(
                        script, option, root, "--skip-auxiliary"
                    )
                    self.assertTrue(auxiliary.is_dir())

                    self.run_script(
                        script,
                        option,
                        root,
                        "--force",
                        "--skip-auxiliary",
                    )
                    self.assertFalse(auxiliary.exists())

    def test_default_home_force_installs_without_release_receipt(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            home = Path(temporary) / "default-codex"
            environment = self.environment.copy()
            environment["CODEX_HOME"] = str(home)
            process = subprocess.run(
                [sys.executable, str(REPO / "install.py"), "--force"],
                cwd=REPO,
                env=environment,
                capture_output=True,
                text=True,
            )
            self.assertEqual(
                process.returncode,
                0,
                msg=process.stdout + process.stderr,
            )
            self.assertTrue((home / "skills" / "econ-review" / "SKILL.md").is_file())
            self.assertNotIn("--release-gate", process.stdout + process.stderr)

    def test_default_home_check_reports_direct_force_repair(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            home = Path(temporary) / "default-codex"
            process = self.run_script(
                "check_install.py",
                "--home",
                home,
                expected=1,
            )
            self.assertIn("Exact repair command", process.stdout)
            self.assertIn("install.py", process.stdout)
            self.assertIn("--force", process.stdout)
            self.assertNotIn("--release-gate", process.stdout)


if __name__ == "__main__":
    unittest.main()
