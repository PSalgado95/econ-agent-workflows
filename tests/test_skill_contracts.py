from __future__ import annotations

import json
import re
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
REVIEW = REPO / "skills" / "econ-review"
REFERENCES = REVIEW / "references"
CATALOG = REFERENCES / "persona-catalog.md"
CROSSWALK = REPO / "tests" / "fixtures" / "reviewer-responsibility-crosswalk.json"

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


def section(text: str, start: str, end: str | None = None) -> str:
    start_at = text.index(start)
    if end is None:
        return text[start_at:]
    return text[start_at : text.index(end, start_at + len(start))]


def parse_catalog() -> tuple[list[str], dict[str, str], dict[str, dict[str, list[str]]]]:
    text = read(CATALOG)
    canonical_text = section(text, "## Canonical role order", "## Base-surface matrix")
    roles = re.findall(r"^\d+\.\s+`([^`]+)`\s*$", canonical_text, re.MULTILINE)
    paths = dict(
        re.findall(
            r"^\| `([^`]+)` \| `([^`]+)` \|\s*$",
            canonical_text,
            re.MULTILINE,
        )
    )

    matrix_text = section(text, "## Base-surface matrix", "## Conditional triggers")
    matrix: dict[str, dict[str, list[str]]] = {}
    for surface, quick, standard in re.findall(
        r"^\| `([^`]+)` \| ([^|]+) \| ([^|]+) \|\s*$",
        matrix_text,
        re.MULTILINE,
    ):
        matrix[surface] = {
            "quick": re.findall(r"`([^`]+)`", quick),
            "standard": re.findall(r"`([^`]+)`", standard),
        }
    return roles, paths, matrix


def role_tokens(text: str, canonical: list[str]) -> set[str]:
    return set(re.findall(r"`([^`]+)`", text)).intersection(canonical)


def ordered_union(canonical: list[str], *groups: list[str] | set[str]) -> list[str]:
    selected: set[str] = set()
    for group in groups:
        selected.update(group)
    return [role for role in canonical if role in selected]


def select_from_catalog(
    canonical: list[str],
    matrix: dict[str, dict[str, list[str]]],
    surfaces: list[str],
    depth: str,
    additions: set[str] | None = None,
) -> list[str]:
    base_depth = "quick" if depth == "quick" else "standard"
    groups: list[list[str] | set[str]] = [
        matrix[surface][base_depth] for surface in matrix if surface in surfaces
    ]
    if additions:
        groups.append(additions)
    return ordered_union(canonical, *groups)


class PersonaCatalogueContractsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.catalog_text = read(CATALOG)
        cls.roles, cls.persona_paths, cls.matrix = parse_catalog()
        cls.crosswalk = json.loads(CROSSWALK.read_text(encoding="utf-8"))

    def test_exactly_fifteen_catalogue_roles_resolve_one_to_one(self) -> None:
        self.assertEqual(len(self.roles), 15)
        self.assertEqual(len(set(self.roles)), 15)
        self.assertEqual(set(self.persona_paths), set(self.roles))
        self.assertEqual(len(set(self.persona_paths.values())), 15)

        actual_files = {
            path.relative_to(REFERENCES).as_posix()
            for path in (REFERENCES / "personas").glob("*.md")
        }
        self.assertEqual(actual_files, set(self.persona_paths.values()))

        required_sections = (
            "## Remit",
            "## Required checks",
            "## Prohibited overreach",
            "## Evidence expectations",
            "## JSON contribution",
        )
        for role, relative_path in self.persona_paths.items():
            persona = read(REFERENCES / relative_path)
            with self.subTest(role=role):
                self.assertIn(f"Role: `{role}`", persona)
                for heading in required_sections:
                    self.assertIn(heading, persona)
                self.assertIn(f'`"role": "{role}"`', persona)
                self.assertIn(f'`"issue_origin": "{role}"`', persona)

        self.assertFalse((REFERENCES / "personas" / "cross-language-validation.md").exists())
        self.assertFalse((REFERENCES / "personas" / "hybrid-implementation.md").exists())

    def test_crosswalk_covers_every_retired_specialist_and_fold(self) -> None:
        crosswalk = self.crosswalk
        self.assertEqual(
            crosswalk["schema_version"],
            "reviewer-responsibility-crosswalk/v1",
        )
        inventory = crosswalk["source_inventory"]
        self.assertEqual(len(inventory), 17)
        self.assertEqual(len(set(inventory)), 17)
        self.assertNotIn("econ-reviewer.toml", inventory)

        obligations = crosswalk["obligations"]
        self.assertEqual(len(obligations), 75)
        obligation_ids = [item["obligation_id"] for item in obligations]
        self.assertEqual(len(obligation_ids), len(set(obligation_ids)))
        source_union = {
            source
            for obligation in obligations
            for source in obligation["source_agents"]
        }
        self.assertEqual(source_union, set(inventory))
        for obligation in obligations:
            with self.subTest(obligation=obligation["obligation_id"]):
                self.assertTrue(obligation["obligation"].strip())
                self.assertTrue(obligation["destinations"])
                self.assertTrue(set(obligation["source_agents"]).issubset(inventory))

        expected_folds = {
            "cross-language-validation": {
                "software-equivalence",
                "transformation-and-sample",
                "reproducibility",
            },
            "hybrid-implementation": {
                "code-quality",
                "estimation-practice",
                "transformation-and-sample",
                "reproducibility",
                "output-consistency",
            },
        }
        source_names = {
            "cross-language-validation": "econ-cross-language-validation-reviewer.toml",
            "hybrid-implementation": "econ-hybrid-implementation-reviewer.toml",
        }
        for folded_role, destinations in expected_folds.items():
            fold = crosswalk["folds"][folded_role]
            with self.subTest(fold=folded_role):
                self.assertFalse(fold["persona_created"])
                self.assertEqual(set(fold["required_destinations"]), destinations)
                owned_destinations = " ".join(
                    destination
                    for obligation in obligations
                    if source_names[folded_role] in obligation["source_agents"]
                    for destination in obligation["destinations"]
                )
                for destination in destinations:
                    self.assertIn(destination, owned_destinations)

    def test_base_matrix_and_folds_produce_deterministic_ordered_unions(self) -> None:
        self.assertEqual(
            set(self.matrix),
            {
                "plan-design",
                "implementation-code",
                "empirical-results",
                "replication-handoff",
            },
        )
        multi_surface = select_from_catalog(
            self.roles,
            self.matrix,
            ["plan-design", "empirical-results"],
            "standard",
        )
        self.assertEqual(
            multi_surface,
            [
                "specification",
                "inference",
                "output-consistency",
                "claim-discipline",
                "design",
                "robustness",
            ],
        )

        cross_language = role_tokens(
            section(
                self.catalog_text,
                "### Cross-language fold",
                "### Hybrid/custom implementation fold",
            ),
            self.roles,
        )
        self.assertEqual(
            select_from_catalog(
                self.roles,
                self.matrix,
                ["implementation-code"],
                "standard",
                cross_language,
            ),
            [
                "transformation-and-sample",
                "code-quality",
                "software-equivalence",
                "reproducibility",
            ],
        )

        hybrid = role_tokens(
            section(
                self.catalog_text,
                "### Hybrid/custom implementation fold",
                "## Promotion modifier",
            ),
            self.roles,
        )
        self.assertEqual(
            select_from_catalog(
                self.roles,
                self.matrix,
                ["implementation-code"],
                "quick",
                hybrid,
            ),
            [
                "transformation-and-sample",
                "estimation-practice",
                "output-consistency",
                "code-quality",
                "reproducibility",
            ],
        )

        promotion = role_tokens(
            section(
                self.catalog_text,
                "## Promotion modifier",
                "## Deterministic selection algorithm",
            ),
            self.roles,
        )
        self.assertEqual(
            select_from_catalog(
                self.roles,
                self.matrix,
                ["empirical-results"],
                "standard",
                promotion,
            ),
            [
                "specification",
                "inference",
                "output-consistency",
                "claim-discipline",
                "output-perception",
                "design",
                "robustness",
                "reproducibility",
                "bundle",
            ],
        )

        trigger_table = section(
            self.catalog_text,
            "## Conditional triggers",
            "### Cross-language fold",
        )
        all_triggers = role_tokens(trigger_table, self.roles)
        all_roles = select_from_catalog(
            self.roles,
            self.matrix,
            list(self.matrix),
            "full",
            all_triggers,
        )
        self.assertEqual(all_roles, self.roles)
        self.assertIn("Six roles are a context-and-cost target, never a cap.", self.catalog_text)

    def test_every_surface_and_depth_has_an_exact_frozen_core(self) -> None:
        expected = {
            ("plan-design", "quick"): ["specification", "design"],
            ("plan-design", "standard"): [
                "specification",
                "claim-discipline",
                "design",
            ],
            ("implementation-code", "quick"): [
                "transformation-and-sample",
                "code-quality",
            ],
            ("implementation-code", "standard"): [
                "transformation-and-sample",
                "code-quality",
                "reproducibility",
            ],
            ("empirical-results", "quick"): [
                "specification",
                "inference",
                "output-consistency",
            ],
            ("empirical-results", "standard"): [
                "specification",
                "inference",
                "output-consistency",
                "claim-discipline",
                "robustness",
            ],
            ("replication-handoff", "quick"): [
                "provenance",
                "reproducibility",
                "bundle",
            ],
            ("replication-handoff", "standard"): [
                "provenance",
                "output-consistency",
                "reproducibility",
                "bundle",
            ],
        }
        for surface in self.matrix:
            for depth in ("quick", "standard", "full"):
                with self.subTest(surface=surface, depth=depth):
                    actual = select_from_catalog(
                        self.roles,
                        self.matrix,
                        [surface],
                        depth,
                    )
                    expected_depth = "quick" if depth == "quick" else "standard"
                    self.assertEqual(actual, expected[(surface, expected_depth)])

    def test_every_conditional_trigger_has_an_exact_composed_roster(self) -> None:
        trigger_table = section(
            self.catalog_text,
            "## Conditional triggers",
            "### Cross-language fold",
        )
        rows = {
            trigger.strip(): role_tokens(additions, self.roles)
            for trigger, additions in re.findall(
                r"^\| ([^|]+) \| ([^|]+) \|\s*$",
                trigger_table,
                re.MULTILINE,
            )
            if role_tokens(additions, self.roles)
        }
        cases = {
            "Source lineage": {"provenance"},
            "Joins": {"transformation-and-sample"},
            "Non-trivial estimator": {"estimation-practice"},
            "P-values": {"inference"},
            "Substantive tables": {
                "output-perception",
                "output-consistency",
            },
            "Code": {"code-quality"},
            "Causal": {"design"},
            "Event time": {"dynamics"},
            "Baseline placement": {"robustness"},
            "Cross-software": {"software-equivalence"},
            "Rerun": {"reproducibility"},
            "The compact review package": {"bundle"},
        }
        self.assertEqual(len(rows), len(cases))
        base = ["specification", "design"]
        for prefix, expected_additions in cases.items():
            matches = [
                additions
                for trigger, additions in rows.items()
                if trigger.startswith(prefix)
            ]
            with self.subTest(trigger=prefix):
                self.assertEqual(matches, [expected_additions])
                self.assertEqual(
                    select_from_catalog(
                        self.roles,
                        self.matrix,
                        ["plan-design"],
                        "quick",
                        matches[0],
                    ),
                    ordered_union(self.roles, base, expected_additions),
                )


class OrchestrationContractsTest(unittest.TestCase):
    def test_review_uses_bounded_prompts_and_a_state_canary_without_attestation_gate(self) -> None:
        skill = read(REVIEW / "SKILL.md")
        protocol = read(REFERENCES / "reviewer-protocol.md")
        schema = read(REFERENCES / "review-report-schema.json")
        openai = read(REVIEW / "agents" / "openai.yaml")
        generated = "\n".join(
            (
                read(REPO / "claude" / "skills" / "econ-review" / "SKILL.md"),
                read(
                    REPO
                    / "claude"
                    / "skills"
                    / "econ-review"
                    / "references"
                    / "reviewer-protocol.md"
                ),
                read(
                    REPO
                    / "claude"
                    / "skills"
                    / "econ-review"
                    / "references"
                    / "review-report-schema.json"
                ),
            )
        )

        combined = "\n".join((skill, protocol, schema, openai, generated))
        normalized_skill = re.sub(r"\s+", " ", skill)
        self.assertIn("prompt-and-canary", combined)
        self.assertIn("generic child dispatch is unavailable", skill)
        self.assertIn("attempts any prohibited action", protocol)
        self.assertIn("Never auto-revert any drift", skill)
        self.assertIn("If the scope is inside a Git repository", normalized_skill)
        self.assertIn("A standalone file outside Git", normalized_skill)

        for obsolete in (
            "host-read-only",
            "transport-read-only",
            "host attestation",
            "host-attested",
            "side_effecting_tools_disabled",
            "safety-preflight",
        ):
            with self.subTest(obsolete=obsolete):
                self.assertNotIn(obsolete, combined)

    def test_queue_backpressure_idle_capacity_and_timeout_semantics_are_explicit(self) -> None:
        skill = read(REVIEW / "SKILL.md")
        normalized = re.sub(r"\s+", " ", skill)
        phrases = (
            "`queued`: selected roles not yet started, in canonical order",
            "Do not hard-code a capacity.",
            "Start roles strictly from the head of `queued`.",
            "refill from the queue without waiting for unrelated running children",
            "Do not use fixed waves or an all-settle barrier before refill.",
            "retry it only after the next owned terminal event",
            "yield to the host once and retry the head role once",
            "mark the head role and every",
            "`capacity-unavailable`",
            "never spin, shrink the roster, skip ahead",
            "`timed_out` is valid only when the host enforces",
            "Every selected role ends in exactly one state",
            "Synthesis begins only after every selected role is terminal.",
        )
        for phrase in phrases:
            with self.subTest(phrase=phrase):
                self.assertIn(re.sub(r"\s+", " ", phrase), normalized)

    def test_child_prompt_is_self_contained_and_parent_owns_verdict_and_ids(self) -> None:
        template_text = read(REFERENCES / "subagent-template.md")
        prompt = re.search(
            r"```text\n(.*?)\n```",
            template_text,
            re.DOTALL,
        )
        self.assertIsNotNone(prompt)
        assembled = prompt.group(1)
        replacements = {
            "{reviewer_protocol}": read(REFERENCES / "reviewer-protocol.md"),
            "{persona}": read(REFERENCES / "personas" / "inference.md"),
            "{method_guardrails}": read(
                REFERENCES / "research-code-quality.md"
            ),
            "{normalized_request}": '{"schema_version":"econ-review-request/v1"}',
            "{bounded_evidence_manifest}": '{"E1":"results/table.tex"}',
            "{reviewer_output_schema}": read(
                REFERENCES / "reviewer-output-schema.json"
            ),
            "{selected_role}": "inference",
        }
        for slot, value in replacements.items():
            assembled = assembled.replace(slot, value)
        self.assertNotRegex(assembled, r"\{[a-z_]+\}")
        self.assertEqual(
            assembled.count(read(REFERENCES / "personas" / "inference.md")),
            1,
        )
        for role, path in parse_catalog()[1].items():
            if role != "inference":
                self.assertNotIn(read(REFERENCES / path), assembled)
        self.assertNotIn("~/.codex/", assembled)
        self.assertNotIn(".codex/agents/", assembled)
        self.assertNotIn("econ_reviewer", assembled)
        self.assertIn("## Parent-only responsibilities", assembled)
        self.assertIn("assign stable `F<n>` identifiers", assembled)
        self.assertIn("assign or recommend the overall verdict", assembled)

    def test_current_user_turn_is_the_only_external_handoff_gate(self) -> None:
        forbidden = re.compile(r"(?i)gpt[\s_-]*pro|gpt-pro-handoff")
        for skill_root in ALL_SKILL_SOURCES[: len(ACTIVE_SKILLS)]:
            for path in skill_root.rglob("*"):
                if path.is_file() and path.suffix.lower() in {".md", ".yaml", ".yml"}:
                    with self.subTest(path=path.relative_to(REPO)):
                        self.assertIsNone(forbidden.search(read(path)))

        auxiliary = ALL_SKILL_SOURCES[-1]
        skill = read(auxiliary / "SKILL.md")
        metadata = read(auxiliary / "agents" / "openai.yaml")
        combined = skill + "\n" + metadata
        self.assertIn("current user", combined.lower())
        self.assertRegex(combined.lower(), r"prior turns|prior user")
        self.assertIn("another skill", combined.lower())
        self.assertIn("current user turn", metadata.lower())
        self.assertIn("explicitly request", metadata.lower())
        self.assertIn("return exactly `not-invoked`", skill)
        self.assertIn("do not suggest or advertise this skill", skill)

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
    def test_econ_work_note_gate_is_local_and_named(self) -> None:
        skill = read(REPO / "skills" / "econ-work" / "SKILL.md")
        reference = read(
            REPO / "skills" / "econ-work" / "references" / "execution_reference.md"
        )
        self.assertIn("local **Reader-facing note gate**", skill)
        self.assertIn("## Reader-facing note gate", reference)
        self.assertIn(
            "passes the local **Reader-facing note gate** above",
            reference,
        )
        self.assertNotIn("`econ-review` Stage 6", skill + reference)

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
