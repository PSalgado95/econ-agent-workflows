from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]


class InstallTest(unittest.TestCase):
    def test_installs_create_project_skill(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            result = subprocess.run(
                [sys.executable, "install.py", "--codex-home", tmp, "--force"],
                cwd=REPO,
                text=True,
                capture_output=True,
                check=True,
            )
            codex_home = Path(tmp)
            self.assertIn("econ-agent-workflows install", result.stdout)
            self.assertTrue((codex_home / "skills" / "create-project" / "SKILL.md").exists())
            self.assertTrue(
                (
                    codex_home
                    / "skills"
                    / "create-project"
                    / "assets"
                    / "README.md"
                ).exists()
            )
            self.assertTrue(
                (
                    codex_home
                    / "skills"
                    / "create-project"
                    / "assets"
                    / "AGENTS.md"
                ).exists()
            )
            self.assertTrue(
                (
                    codex_home
                    / "skills"
                    / "create-project"
                    / "agents"
                    / "openai.yaml"
                ).exists()
            )


if __name__ == "__main__":
    unittest.main()
