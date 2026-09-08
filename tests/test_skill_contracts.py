from __future__ import annotations

import re
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
REVIEW = REPO / "skills" / "econ-review"
REFERENCES = REVIEW / "references"

ACTIVE_SKILLS = (
    "econ-brainstorm",
    "econ-plan",
    "econ-work",
    "econ-review",
    "econ-debug",
    "econ-lfg",
    "econ-compound",
)
ALL_SKILL_SOURCES = tuple(REPO / "skills" / name for name in ACTIVE_SKILLS) + (
    REPO / "skills" / "auxiliary" / "gpt-pro-handoff",
)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


class PackagePortabilityTest(unittest.TestCase):


    def test_active_source_and_generated_skills_are_person_neutral(self) -> None:
        forbidden_source = (
            re.compile(r"(?i)\bpedro\b"),
            re.compile(r"(?i)c:\\users\\"),
            re.compile(r"(?i)pedro[_-]escritorio"),
        )
        roots = ALL_SKILL_SOURCES + (REPO / "claude" / "skills",)
        suffixes = {".md", ".json", ".yaml", ".yml", ".py", ".txt", ".html"}
        for root in roots:
            for path in root.rglob("*"):
                if not path.is_file() or path.suffix.lower() not in suffixes:
                    continue
                text = read(path)
                for pattern in forbidden_source:
                    with self.subTest(path=path.relative_to(REPO), pattern=pattern.pattern):
                        self.assertIsNone(pattern.search(text))

        claude_forbidden = (
            re.compile(r"\bCodex\b"),
            re.compile(r"request_user_input"),
            re.compile(r"update_plan"),
            re.compile(r"\bAGENTS\.md\b"),
            re.compile(r"\.codex[\\/]"),
        )
        for path in (REPO / "claude" / "skills").rglob("*"):
            if not path.is_file() or path.suffix.lower() not in suffixes:
                continue
            text_without_banner = "\n".join(
                line
                for line in read(path).splitlines()
                if not line.strip().startswith(
                    "<!-- GENERATED FROM CODEX SOURCE"
                )
            )
            for pattern in claude_forbidden:
                with self.subTest(path=path.relative_to(REPO), pattern=pattern.pattern):
                    self.assertIsNone(pattern.search(text_without_banner))


class LocalAssetContractsTest(unittest.TestCase):

    def test_every_active_local_reference_resolves_within_its_skill(self) -> None:
        markdown_link = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
        package_path = re.compile(
            r"`((?:references|assets|scripts)/[^`\s,;)]+)`"
        )
        for skill_root in ALL_SKILL_SOURCES:
            resolved_root = skill_root.resolve()
            for markdown in skill_root.rglob("*.md"):
                text = read(markdown)
                for raw_target in markdown_link.findall(text):
                    target = raw_target.strip().strip("<>").split("#", 1)[0]
                    if not target or "://" in target or target.startswith("#"):
                        continue
                    resolved = (markdown.parent / target).resolve()
                    with self.subTest(file=markdown.relative_to(REPO), target=target):
                        self.assertTrue(resolved.exists())
                        self.assertTrue(resolved.is_relative_to(resolved_root))
                for target in package_path.findall(text):
                    resolved = (skill_root / target.rstrip(".")).resolve()
                    with self.subTest(file=markdown.relative_to(REPO), target=target):
                        self.assertTrue(resolved.exists())
                        self.assertTrue(resolved.is_relative_to(resolved_root))

    def test_research_code_quality_guardrails_are_byte_identical(self) -> None:
        work_copy = REPO / "skills" / "econ-work" / "references" / "research-code-quality.md"
        review_copy = REFERENCES / "research-code-quality.md"
        self.assertEqual(work_copy.read_bytes(), review_copy.read_bytes())
        self.assertTrue(
            (REPO / "skills" / "econ-work" / "references" / "r-defaults.md").is_file()
        )
        self.assertFalse(
            (REPO / "references" / "research-code-quality.md").exists()
        )
        self.assertFalse((REPO / "references" / "r-defaults.md").exists())
        self.assertFalse((REPO / "references" / "reviewer-protocol.md").exists())


if __name__ == "__main__":
    unittest.main()
