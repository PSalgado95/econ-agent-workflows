"""Validate the package's deliberately small YAML subset without dependencies.

Metadata uses unquoted identifier keys, JSON-quoted strings, and YAML booleans.
Reject other syntax rather than pretending to parse arbitrary YAML.
"""
from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]


def metadata(text: str) -> dict:
    result: dict = {}
    stack = [(-2, result)]
    for line in text.splitlines():
        if not line.strip():
            continue
        match = re.fullmatch(r"( *)([a-z][a-z0-9_-]*):(?: (.+))?", line)
        if not match:
            raise ValueError(f"Unsupported metadata syntax: {line!r}")
        spaces, key, raw = match.groups()
        indent = len(spaces)
        while indent <= stack[-1][0]:
            stack.pop()
        if indent != stack[-1][0] + 2:
            raise ValueError("Invalid metadata indentation")
        parent = stack[-1][1]
        if key in parent:
            raise ValueError(f"Duplicate metadata key: {key}")
        if raw is None:
            parent[key] = {}
            stack.append((indent, parent[key]))
        elif raw in {"true", "false"}:
            parent[key] = raw == "true"
        elif key == "name" and re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", raw):
            parent[key] = raw
        else:
            parent[key] = json.loads(raw)
            if not isinstance(parent[key], str):
                raise ValueError("Expected a quoted string")
    return result


class SkillMetadataTest(unittest.TestCase):
    def test_verification_does_not_implicitly_launch_formal_review(self) -> None:
        work = (REPO / "skills/econ-work/SKILL.md").read_text(encoding="utf-8")
        debug = (REPO / "skills/econ-debug/SKILL.md").read_text(encoding="utf-8")
        lfg = (REPO / "skills/econ-lfg/SKILL.md").read_text(encoding="utf-8")
        self.assertNotIn("Default review target:", work)
        self.assertNotIn("hand the changed surface to a targeted", debug)
        self.assertIn("Do not automatically invoke `econ-review`", work)
        self.assertIn("Do not automatically invoke `econ-review`", debug)
        self.assertIn("Invoke `econ-review`", lfg)

    def test_discovery_and_ui_contracts(self) -> None:
        names = set()
        for path in sorted((REPO / "skills").rglob("SKILL.md")):
            with self.subTest(skill=path.parent.name):
                header = metadata(path.read_text(encoding="utf-8").split("---", 2)[1])
                name = header["name"]
                self.assertEqual(name, path.parent.name)
                self.assertNotIn(name, names)
                names.add(name)
                self.assertLessEqual(len(name), 64)
                self.assertTrue(1 <= len(header["description"]) <= 1024)
                ui = metadata((path.parent / "agents/openai.yaml").read_text(encoding="utf-8"))
                interface = ui["interface"]
                self.assertTrue(interface["display_name"].strip())
                self.assertTrue(25 <= len(interface["short_description"]) <= 64)
                self.assertIn(f"${name}", interface["default_prompt"])
                explicit_only = name in {"gpt-pro-handoff", "econ-review"}
                self.assertEqual(ui.get("policy", {}).get("allow_implicit_invocation", True), not explicit_only)
                generated = REPO / "claude/skills" / name / "SKILL.md"
                claude = metadata(generated.read_text(encoding="utf-8").split("---", 2)[1])
                self.assertEqual(claude.get("disable-model-invocation", False), explicit_only)
                self.assertEqual(claude["description"], header["description"])

    def test_rejects_duplicate_keys_and_invalid_indentation(self) -> None:
        for text in ('name: one\nname: two', 'interface:\n   display_name: "Bad"', 'description: [broken'):
            with self.subTest(text=text), self.assertRaises(ValueError):
                metadata(text)


if __name__ == "__main__":
    unittest.main()
