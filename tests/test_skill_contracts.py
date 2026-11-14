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

    def test_brainstorm_is_optional_and_plan_preserves_scope_memo(self) -> None:
        brainstorm = read(REPO / "skills" / "econ-brainstorm" / "SKILL.md")
        scope_template = read(
            REPO / "skills" / "econ-brainstorm" / "references" / "scope_memo_template.md"
        )
        plan = read(REPO / "skills" / "econ-plan" / "SKILL.md")

        self.assertIn("Do not create a scope memo merely because brainstorming occurred", brainstorm)
        self.assertIn("writes a fresh `-econ-plan.md`", brainstorm)
        self.assertIn("the scope memo remains unchanged", scope_template)
        self.assertIn("leave it unchanged", plan)
        self.assertIn("Never relabel, rename, or overwrite the scope memo", plan)

        combined = "\n".join((brainstorm, scope_template, plan)).lower()
        self.assertNotIn("upgrade that same document in place", combined)
        self.assertNotIn("upgrades the same document in place", combined)

    def test_econ_debug_is_retired_from_the_package(self) -> None:
        import sys

        sys.path.insert(0, str(REPO))
        import install

        self.assertNotIn("econ-debug", {name for _source, name in install.CORE_SKILLS})
        self.assertIn("econ-debug", install.STALE_SKILL_DIRS)
        self.assertFalse((REPO / "skills" / "econ-debug").exists())
        self.assertFalse((REPO / "claude" / "skills" / "econ-debug").exists())
        for root in ALL_SKILL_SOURCES:
            for path in root.rglob("*.md"):
                with self.subTest(path=path.relative_to(REPO)):
                    self.assertNotIn("econ-debug", read(path))

    def test_git_and_issue_actions_follow_repository_instructions(self) -> None:
        rule = "Follow the repository's own instructions for Git and issues"
        for name in ("econ-work", "econ-lfg"):
            text = read(REPO / "skills" / name / "SKILL.md")
            with self.subTest(skill=name):
                self.assertIn(rule, text)
                self.assertNotIn("Do not stage, commit, or push unless", text)
        plan = read(REPO / "skills" / "econ-plan" / "SKILL.md")
        self.assertNotIn("never create or update issues without approval", plan)

    def test_judgment_work_runs_on_the_coordinator_model(self) -> None:
        reference = read(
            REPO / "skills" / "econ-work" / "references" / "delegation_reference.md"
        )
        self.assertNotIn("do not require the parent's settings", reference)
        self.assertIn("runs on the coordinator's own", reference)
        self.assertIn("Never use a Haiku-class model", reference)

    def test_econ_lfg_reviews_with_one_fresh_context_reviewer(self) -> None:
        lfg = read(REPO / "skills" / "econ-lfg" / "SKILL.md")
        resolution = read(
            REPO / "skills" / "econ-lfg" / "references" / "review_resolution_reference.md"
        )
        review = read(REVIEW / "SKILL.md")
        self.assertIn("## Reviewer subagent", lfg)
        self.assertIn("## Reviewer brief", resolution)
        self.assertIn("mode: single-reviewer", resolution)
        self.assertIn("## Single-reviewer mode", review)
        for retired in ("econ-review-request/v1", "econ-review-report/v3", "panel remains degraded"):
            with self.subTest(retired=retired):
                self.assertNotIn(retired, lfg)
                self.assertNotIn(retired, resolution)

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
