# Port econ-agent-workflows to Claude Code

- **Date:** 2026-06-14
- **Type:** port / build tooling
- **Status:** implemented 2026-06-14 (build + install scripts written, generated tree verified via temp install)
- **Owner:** Pedro

## 1. Goal

Make the four core skills (`econ-plan`, `econ-work`, `econ-review`, `econ-compound`) plus
the auxiliary `gpt-pro-handoff` skill installable and usable in **Claude Code**, while
**Codex remains the only place the skills are authored and edited**.

The Claude artifacts must be:

1. **Generated, never hand-edited** — so Codex stays the single source of truth.
2. **Committed to the GitHub repo** — so an agent pointed at the repo can install them by copying files.
3. **Re-installable / updatable** — pull the repo, re-run the install script.

## 2. Decisions (confirmed)

- **Distribution:** install script (mirrors the existing Codex `install.py`), **not** a plugin marketplace.
- **Slash commands:** yes — generate `/econ-plan`, `/econ-work`, `/econ-review`, `/gpt-pro-handoff`
  from each skill's `agents/openai.yaml`. (`econ-compound` has no `openai.yaml`, so no command unless we add one.)
- **Process:** plan doc first (this document), then build.

## 3. Source-of-truth & sync model

```
Codex source (canonical, hand-edited)        Generated (committed, never hand-edited)
  skills/<name>/SKILL.md            ─┐
  skills/<name>/references/*         │   build_claude.py        claude/
  skills/<name>/scripts/*           ├──► (deterministic   ──►    .claude/skills/<name>/
  skills/<name>/agents/openai.yaml  │    transforms)             .claude/agents/*.md
  .codex/agents/*.toml              │                            .claude/commands/*.md
  references/reviewer-protocol.md   ─┘                           .claude/references/...
```

Two scripts:

- **`build_claude.py`** — maintainer step. Reads the Codex tree, writes the generated
  `claude/` tree into the repo. Pedro runs this after editing skills in Codex, then commits.
- **`install_claude.py`** — user/agent step. Copies the committed `claude/` tree into the
  user's `~/.claude/` (`skills/`, `agents/`, `commands/`, `references/`). Mirrors `install.py`.

**Sync loop:** edit in Codex → `python build_claude.py` → commit & push → on the Claude side
`git pull` → `python install_claude.py --force`.

Every generated file gets a banner:
`<!-- GENERATED FROM CODEX SOURCE — DO NOT EDIT. Edit skills/ or .codex/agents/ and run build_claude.py. -->`

## 4. Format mapping

| Piece | Codex | Claude Code | Transform |
|---|---|---|---|
| Skill body | `skills/<n>/SKILL.md` | `skills/<n>/SKILL.md` | Copy + substitution table (§5) |
| References | `skills/<n>/references/*` | same | Copy + substitution table |
| Scripts | `skills/<n>/scripts/*` | same | Copy as-is |
| Skill interface | `agents/openai.yaml` | `commands/<n>.md` | Generate slash command from `default_prompt` |
| Reviewer agents | `.codex/agents/*.toml` | `agents/*.md` | TOML → MD frontmatter + body (§6) |
| Shared protocol | `~/.codex/references/econ-agent-workflows/reviewer-protocol.md` | `~/.claude/references/econ-agent-workflows/reviewer-protocol.md` | Copy + path rewrite |
| Install | `install.py` → `~/.codex` | `install_claude.py` → `~/.claude` | New script |

Install destinations (user-level, cross-platform via `pathlib`, matching the Windows/VS Code setup):

- skills → `~/.claude/skills/<name>/`
- agents → `~/.claude/agents/<name>.md`
- commands → `~/.claude/commands/<name>.md`
- protocol → `~/.claude/references/econ-agent-workflows/reviewer-protocol.md`

## 5. Substitution table (Codex → Claude, applied to skill/reference/agent text)

| Find | Replace | Notes |
|---|---|---|
| `$econ-plan` / `$econ-work` / `$econ-review` / `$econ-compound` / `$gpt-pro-handoff` | `/econ-plan` etc. | Invocation syntax |
| `request_user_input` | `AskUserQuestion` | User-prompt tool name |
| `~/.codex/references/econ-agent-workflows/` | `~/.claude/references/econ-agent-workflows/` | Installed protocol path |
| `.codex/agents/` | `~/.claude/agents/` | Repo-relative agent dir → installed agent dir |
| "Codex custom agents" / "Codex" (when naming the runtime) | "Claude Code" | Prose only; do not blind-replace inside file names |

"subagent tools" / "spawn reviewer agents in parallel" stay — Claude dispatches them via the
**Task** tool (`subagent_type` = agent name), multiple Task calls in one message = parallel.

The substitution table lives in `build_claude.py` as an explicit ordered list so it is reviewable
and easy to extend when new Codex-isms appear.

## 6. Reviewer agent transform (TOML → MD)

Codex TOML keys → Claude MD frontmatter:

| Codex TOML | Claude MD |
|---|---|
| `name = "econ_inference_reviewer"` | `name: econ_inference_reviewer` (keep identical — see §7) |
| `description = "..."` | `description: "..."` |
| `model_reasoning_effort = "high"` | `model: sonnet` (baseline for all reviewers; see §11.3) |
| `sandbox_mode = "read-only"` | `tools: Read, Grep, Glob` (read-only auditor set) |
| `developer_instructions = """..."""` | Markdown body below frontmatter |

The 16 reviewer TOMLs under `.codex/agents/` each become one `agents/<name>.md`.

## 7. Agent-name / role mapping (must be preserved)

`econ-review` selects reviewers by **role alias** (`provenance-auditor`, `inference-auditor`, …)
and maps them to **agent names** (`econ_provenance_reviewer`, `econ_inference_reviewer`, …) via the
table in `skills/econ-review/references/review_reference.md`.

Decision: **keep the Codex agent names unchanged** so that mapping table stays valid with no edits.
Claude's Task `subagent_type` will be the agent `name` (e.g. `econ_inference_reviewer`). Underscores
in agent names are acceptable.

## 8. Command generation

For each skill with `agents/openai.yaml`, generate `commands/<skill>.md`:

```markdown
<!-- GENERATED ... -->
---
description: "<short_description from openai.yaml>"
---

<default_prompt, with $econ-x → /econ-x substitution> $ARGUMENTS
```

`econ-compound` has no `openai.yaml`. Options: (a) leave it command-less (skill still
auto-triggers and is callable via the Skill tool), or (b) add an `openai.yaml` to the Codex source
so both runtimes get a command. **Open question — see §11.**

## 9. Repo layout after this change

```text
.codex/agents/*.toml            # Codex source (unchanged)
references/reviewer-protocol.md  # Codex source (unchanged)
skills/                          # Codex source (unchanged)
  econ-plan/ econ-work/ econ-review/ econ-compound/
  auxiliary/gpt-pro-handoff/
install.py                       # Codex installer (unchanged)
build_claude.py                  # NEW — generator (Codex → claude/)
install_claude.py                # NEW — installer (claude/ → ~/.claude)
claude/                          # NEW — GENERATED, committed
  skills/  agents/  commands/  references/
docs/plans/2026-06-14-port-econ-skills-to-claude-code-plan.md
README.md
```

## 10. Implementation steps

1. Write `build_claude.py`: substitution table, TOML→MD agent transform, command generation,
   protocol copy, banner injection; emits `claude/`.
2. Run it; review the generated `claude/` tree by hand for any leaked Codex-isms.
3. Write `install_claude.py` (pathlib, `--force`, `--claude-home` override, refuses to write
   outside the target home — mirror `install.py` safety).
4. Test in this Claude Code session: install locally, then exercise
   `/econ-plan`, `/econ-work`, `/econ-compound`, and an `econ-review` panel; confirm reviewer
   subagents dispatch via Task and the protocol path resolves.
5. Update `README.md` with a "Claude Code" section: the sync loop, install command, and the
   "edit in Codex only" rule.
6. Commit (only when Pedro asks).

## 11. Decisions resolved & remaining risks

1. **`econ-compound` command** — RESOLVED: add `agents/openai.yaml` to the Codex source so both
   runtimes get `/econ-compound`. Delegated to Codex (message drafted 2026-06-14). The Claude build
   should tolerate the file being absent until Codex adds it (skip the command, don't error).
2. **Read-only reviewer tools** — RESOLVED: all 16 reviewer TOMLs are `sandbox_mode = "read-only"`
   and explicitly forbid mutation/scripts, so they map to `tools: Read, Grep, Glob`.

7. **`gpt-pro-handoff` script string** — OPEN (cosmetic): `skills/auxiliary/gpt-pro-handoff/scripts/
   build_handoff_package.py:711` embeds a GPT Pro prompt line "...prepared by Codex." Scripts are
   copied byte-for-byte (substituting Python is risky), so this label stays "Codex" in the Claude
   build. Best fixed by making the string runtime-neutral in the Codex source. Flagged for Codex.
3. **Reviewer model** — RESOLVED: map all reviewer agents to `model: sonnet` as the baseline.
   Pedro can manually promote a specific reviewer (or a whole run) to Opus when the task is
   critical. Do not force Opus by default.
4. **`gpt-pro-handoff`** — RESOLVED: port as-is.
5. **Commit of generated `claude/`** — RESOLVED: commit the generated tree, so an agent can install
   by dumb-copying from GitHub (no Python required at install time beyond running `install_claude.py`).
6. **`econ-review` degraded-mode wording** — OPEN (verify during testing): the skill already handles
   "subagents unavailable" gracefully; confirm the wording still reads correctly under Claude's Task
   model after substitution.
```

