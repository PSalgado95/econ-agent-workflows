from __future__ import annotations

import re
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
SKILL_DIR = REPO / "skills" / "create-project"


def read(relative: str) -> str:
    return (SKILL_DIR / relative).read_text(encoding="utf-8")


def frontmatter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    match = re.match(r"---\n(.*?)\n---", text, re.S)
    if not match:
        raise AssertionError(f"missing frontmatter: {path}")
    data: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            data[key.strip()] = value.strip().strip('"')
    return data


class CreateProjectSkillTest(unittest.TestCase):
    def test_skill_metadata_and_interface(self) -> None:
        meta = frontmatter(SKILL_DIR / "SKILL.md")
        self.assertEqual("create-project", meta["name"])
        self.assertIn("economics research project", meta["description"])

        interface = read("agents/openai.yaml")
        self.assertIn('display_name: "Create Project"', interface)
        self.assertIn("short_description:", interface)
        self.assertIn("default_prompt:", interface)
        self.assertIn("$create-project", interface)

    def test_skill_declares_required_scaffold_and_scratch_contract(self) -> None:
        text = read("SKILL.md")
        for expected in (
            "code/",
            "data/raw/",
            "data/processed/",
            "output/logs/",
            "output/figures/",
            "output/tables/",
            "output/results/",
            "paper/",
            "reference/",
            "scratch/docs/plans/",
            "scratch/docs/brainstorms/",
            "scratch/docs/memos/",
            "scratch/docs/notes/",
            "scratch/agents/",
        ):
            self.assertIn(expected, text)

        self.assertIn("Do not create a tracked `docs/` folder", text)
        self.assertIn("Do not add placeholder files", text)
        self.assertIn("If the folder is not empty, stop", text)
        self.assertIn("Use GitHub CLI", text)

    def test_templates_are_minimal_and_non_authoritative(self) -> None:
        readme = read("assets/README.md")
        agents = read("assets/AGENTS.md")

        self.assertIn("minimal project index", readme)
        self.assertIn("not a live status memo", readme)
        self.assertIn("scratch/docs/", readme)
        self.assertIn("scratch/agents/", readme)
        self.assertNotIn("current results", readme.lower())
        self.assertNotIn("current workflow", readme.lower())

        self.assertIn("Write for an economist", agents)
        self.assertIn("Treat `data/raw/` as read-only", agents)
        self.assertIn("scratch/docs/", agents)
        self.assertIn("scratch/agents/", agents)
        self.assertIn("Ask before changing", agents)

    def test_gitignore_variants_encode_data_policy(self) -> None:
        all_data = read("assets/gitignore-all-data.txt")
        raw_only = read("assets/gitignore-raw-only.txt")

        self.assertIn("data/raw/", all_data)
        self.assertIn("data/processed/", all_data)
        self.assertIn("scratch/", all_data)
        self.assertIn("output/logs/", all_data)

        self.assertIn("data/raw/", raw_only)
        self.assertNotIn("data/processed/", raw_only)
        self.assertIn("scratch/", raw_only)
        self.assertIn("output/logs/", raw_only)

    def test_no_default_tracked_docs_instruction(self) -> None:
        combined = "\n".join(
            path.read_text(encoding="utf-8")
            for path in [
                SKILL_DIR / "SKILL.md",
                SKILL_DIR / "assets" / "README.md",
                SKILL_DIR / "assets" / "AGENTS.md",
            ]
        )
        self.assertNotIn("`docs/plans/`", combined)
        self.assertNotIn("`docs/brainstorms/`", combined)
        self.assertIn("scratch/docs/plans/", combined)
        self.assertIn("scratch/docs/brainstorms/", combined)


if __name__ == "__main__":
    unittest.main()
