from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

import build_claude  # noqa: E402


class BuildClaudeDenyScanTest(unittest.TestCase):
    def test_reference_override_does_not_change_other_skill_files(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / "source"
            (source / "references").mkdir(parents=True)
            original = "## Host settings\n\nOriginal.\n\n## Next\n\nKeep.\n"
            (source / "SKILL.md").write_text(original, encoding="utf-8")
            (source / "references/dispatch.md").write_text(original, encoding="utf-8")
            overrides = {
                ("test-skill", "references/dispatch.md", "## Host settings"):
                    "## Host settings\n\nReplacement.\n"
            }
            with patch.object(build_claude, "OVERRIDES", overrides):
                build_claude.copy_skill(source, root / "out", "test-skill")
            reference = (root / "out/references/dispatch.md").read_text(encoding="utf-8")
            self.assertIn("Replacement.", reference)
            self.assertIn("## Next\n\nKeep.", reference)
            self.assertNotIn("Original.", reference)
            self.assertIn("Original.", (root / "out/SKILL.md").read_text(encoding="utf-8"))

    def test_invalid_utf8_is_a_deterministic_violation(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "broken.md").write_bytes(b"\xff")

            self.assertEqual(
                build_claude.deny_scan(root),
                ["broken.md:0: unreadable-text :: invalid UTF-8"],
            )

    def test_read_error_is_a_deterministic_violation(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            path = root / "blocked.md"
            path.write_text("safe\n", encoding="utf-8")
            original = Path.read_text

            def fail_selected(
                candidate: Path, *args: object, **kwargs: object
            ) -> str:
                if candidate == path:
                    raise PermissionError("host-specific details")
                return original(candidate, *args, **kwargs)

            with patch.object(Path, "read_text", fail_selected):
                self.assertEqual(
                    build_claude.deny_scan(root),
                    ["blocked.md:0: unreadable-text :: PermissionError"],
                )


if __name__ == "__main__":
    unittest.main()
