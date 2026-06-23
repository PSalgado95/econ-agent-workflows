from __future__ import annotations

import re
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]


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


class SkillMetadataTest(unittest.TestCase):
    def test_create_project_metadata(self) -> None:
        meta = frontmatter(REPO / "skills" / "create-project" / "SKILL.md")
        self.assertEqual("create-project", meta["name"])
        self.assertIn("economics research project", meta["description"])
        text = (REPO / "skills" / "create-project" / "agents" / "openai.yaml").read_text(
            encoding="utf-8"
        )
        self.assertIn("display_name:", text)
        self.assertIn("short_description:", text)
        self.assertIn("default_prompt:", text)
        self.assertIn("$create-project", text)


if __name__ == "__main__":
    unittest.main()
