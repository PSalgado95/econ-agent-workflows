---
name: econ-plan
description: "Turn an economics research task into a staged, saved execution plan scoped by reader and deliverable, handed off to econ-work. Use when the user asks to plan, scope, or sequence empirical or computational research: cleaning or constructing data, panel/DiD/event-study/IV/structural estimation, tables and figures, robustness rounds, replication packages, or a results note — or names a plan file, project brief, or GitHub issue to plan against. Not for pure software planning with no research object."
---

# Economist Planning Workflow

Plan only. Do not execute code, run empirical work, build outputs, or draft the note in the same turn unless the user later gives a separate instruction. This file is the contract; read `references/plan_template.md` only when writing or refreshing the saved plan, and `references/project_brief_template.md` only when the user approves a project-backbone document.

## Direct invocation contract

Every direct invocation ends in exactly one of two states:
- **an alignment conversation in progress**, asking one decision per blocking question until the material task context is shared; or
- **a saved plan file plus a short receipt.**

An inline-only plan is not a valid completion. Write the saved markdown plan unless file creation is genuinely blocked (missing write access, no workspace location, or a failed file operation), in which case state the blocker and the exact no-save reason. The saved file is the artifact; the chat receipt is only the summary and handoff. Always plan; never abandon the workflow as "not a planning task".

## Receipt — mandatory visible output

Unless the turn ends while alignment questions are still in progress, the visible response carries these fields in order:

1. **Task restatement** — one plain paragraph: what is in scope, out of scope, and which assumption would change the plan. Example: *I understand this as: rerun the main figure under the current sample rule, inspect whether the headline changes, and prepare a coauthor-facing note only if the result is stable. I will not change the identification strategy unless you ask.*
2. **Classification** — `domain_mode`, `task_family`, `code_role`, `reporting: yes|no`, and secondary lanes if any. Surface only the classifications that change behaviour.
3. **Decision frame** — final human reader, desired output, project backbone used or proposed, GitHub issue action if any.
4. **Central bottleneck** — the one constraint the plan is organised around.
5. **Execution path** — the four `econ-work` stages with their expected stop conditions.
6. **Review and handoff** — saved plan path or no-save reason, the `econ-work` route, the later `econ-review` surface, an optional plan-review trigger, and the recommended next command.

## Questions

Asking good blocking questions is how the plan recovers the research context that is not yet in the prompt. Use the platform's blocking-question tool (`request_user_input`; the Claude build translates it), not plain chat text. Ask one decision per question, with the context that makes it answerable: what the decision affects for the plan, the plausible options with their tradeoffs, and a recommended conservative default. Continue until the objective, research object, scope, assumptions, methods, outputs, audience, and relevant constraints are sufficiently understood. Do not guess missing context merely to avoid asking, and never bury a material question in the `Open questions` list.

Ask, after a first repo read, whenever the answer could materially change the plan:
- the objective or decision problem, and the intended reader;
- whether reporting (a reader-facing note or figures) is in scope;
- the baseline or main comparison; whether a benchmark is a diagnostic comparison or the target to match;
- whether an expensive rerun or destructive overwrite is acceptable.

Clarify reporting scope without compressing separate decisions into one overloaded question. Establish whether a reader-facing output is wanted, then its type, reader, and figure needs as separate follow-ups when those answers are not already shared.

**Scope call-out gate.** After reading evidence (Stage 2) and before writing the plan, present the task restatement plus the material stated, inferred, and out-of-scope call-outs the researcher should confirm ("I am assuming X is the baseline; Y is out of scope"), each answerable without opening the repo. In an autonomous parent run, any surviving inference goes into an explicit `Assumptions` section of the saved plan; researcher-level choices still return to the parent as questions.

## What a ready plan locks

- a plain-language restatement (receipt item 1) and the decision problem, not just the topic;
- the final human reader and the desired output;
- the project backbone used, or that none was found;
- `domain_mode`, `task_family`, `code_role`, and `reporting: yes|no`;
- one central bottleneck;
- sparse stable labels for important decisions, outputs, and work units (`F1`, `F2`, … reserved for `econ-review` findings);
- the live research object separate from any benchmark or comparison block, and audit outputs separate from report inputs;
- a four-stage execution path handed to `econ-work`: code and run checks → output inspection → interpretation and headline triage → note and figures.

**Smallest correct round.** When the validated evidence already exists, plan the smallest correct next round; do not reopen adjacent branches unless the central bottleneck requires it.

When reporting is in scope, lock the reader-facing note contract before execution. Do not draft it from raw diagnostics:
- note type (free text), and the question the note must answer;
- the one-sentence headline it may make if the evidence holds;
- what the reader should know by the end;
- the definitions and sample distinctions that must appear before findings;
- the finished human-facing surface (`html` by default, or explicitly requested `tex-plus-pdf`) and render target;
- the likely headline figure, and what belongs in the appendix rather than the main text.

Default format: standalone researcher-facing notes and memos are HTML. Produce `.tex` plus rendered `.pdf` only when the user explicitly requests those formats or explicitly asks for integration into a paper. Markdown is an agent-facing planning or drafting surface, not the default finished note.

## Domain routing

Classify `domain_mode` before writing the plan (this is its single home):
- `empirical` — economics research where sources, data, models, outputs, interpretation, reporting, benchmark comparison, or reproducibility matter;
- `hybrid` — research-object integrity and software-implementation integrity both matter (data pipelines, reproducibility, custom interfaces, model computation, simulation, calibration, estimation machinery, reusable research tooling);
- `software-handoff` — pure app, API, UI, infrastructure, tooling, refactor, or debugging with no research-object, output, interpretation, or reporting stakes. Mark it and route to the software-engineering workflow rather than `econ-work`.

## Proportionality

**Compact plan.** When the task is a single bounded stage with no new definitions, samples, or benchmark treatment, collapse the receipt to four fields — task restatement, one-line classification, execution path with skipped stages named, and review and handoff — and save a short plan using only the template sections that apply. The saved file always exists.

## Workflow

Saved plans use repo-relative paths for files, outputs, and evidence (`analysis/build_sample.do`, not `/path/to/repo/...`); use absolute paths only in the final chat link. When the user names a specific file, issue, plan, output, register, dataset, or document, inspect it before substituting a generic alternative; if it cannot be found, say so.

### Stage 0 — Locate the planning surface
- If an existing plan is referenced or obviously matches, read it; ask update-in-place vs new when ambiguous; revise only still-relevant sections (plans carry no execution progress log).
- When the planning surface is a scope memo with `readiness: scoping-only` (from `econ-brainstorm`), upgrade that same document in place to a full plan rather than creating a new file.
- Discover the project backbone in order: a brief named in `README.md`/docs index → `PROJECT_BRIEF.md` → `RESEARCH_BRIEF.md` → paper outline, coauthor memo, or methods note → a dated plan only when it is clearly acting as the backbone.
- Use `AGENTS.md`/`README.md` for orientation only, never as the research plan. If no backbone exists and future sessions will need the context, ask whether to create a compact `PROJECT_BRIEF.md` (not for narrow one-offs). A new project's `DEFINITIONS.md` can be seeded from the backbone's definitions section or a graduated scope memo.
- If a GitHub issue is named (`#123`, `repo#123`, or a URL), read it as coordination context, summarise only the decision-relevant parts, add an `Issue coordination` section, and never create or update issues without approval.

### Stage 1 — Decision frame
Lock the objective; project backbone; issue coordination when issue-linked; reader contract; `reporting: yes|no` (and the note contract when yes); `task_family`; `code_role` when code is in scope; secondary lanes; and the central bottleneck.

Classify `task_family` by the primary research object, not the output format, keeping it orthogonal to `domain_mode` and reporting: an `analysis` or `data_construction` plan may still carry a note, and `writing` is only for when the note or memo is the primary object, built from already-defended or inspection-ready evidence — never drafted from raw diagnostics or uncatalogued sources.

### Stage 2 — Gather evidence, then call out scope
- Read the object-defining code, current outputs and checks, active workflow notes, and the prior plans, notes, or benchmark material that matter.
- Read the project's `DEFINITIONS.md` when present and treat its terms as canonical; the plan's definition registry cites its entries rather than restating them.
- For broad, repeated, risky, or unclear tasks, search repo-local research-learning notes (`docs/research-learnings/`, `.codex/research-learnings/`, legacy `docs/solutions/`), narrowed by task family: `source_collection` → source-provenance, interpretation-claims; `data_construction` → data-measurement, sample-linkage; `model_computation` → theory-models, specification-estimation; `analysis` → specification-estimation, interpretation-claims; `writing` → interpretation-claims, writing-figures.
- Treat any note as precedent, not authority; flag a conflict with live files and mark the note stale rather than following it silently.
- Build a compact evidence map (live and checked / live but unchecked / missing vs the requested target / ambiguous), and call out missing evidence before leaning on it.
- Then run the scope call-out gate above.

### Stage 3 — Lock definitions and deliverables
Make explicit the research question and estimand (or descriptive object), a definition registry for terms that can drift, current authority files vs supporting or benchmark files, interpretation scope, audit outputs, and report inputs. When reporting is in scope, lock the note contract above. The task-family implementation-surface specifics (source/register fields, data-construction registries and audits, model-computation entrypoints and checks, analysis baseline and robustness grid, writing claim-budget) live in `references/plan_template.md` as guidance under the matching sections — read them at template-writing time.

### Stage 4 — Sequence the four econ-work stages and verification
Hand off the same four stages `econ-work` runs; the per-stage fields are in `references/plan_template.md`:
- **Stage 1 code and run checks** — likely entrypoints, expected objects, feasible run boundary, code role and the research-code-quality floor, stop conditions;
- **Stage 2 output inspection** — realised outputs to inspect before interpretation, sample/grouping/denominator/missingness/overlap audits, audit vs report outputs;
- **Stage 3 interpretation and headline triage** — where to stop and decide the main finding, and whether the interpretation and note briefs are required;
- **Stage 4 note writing and figures** — structure, definitions before findings, figure order, text-figure consistency, and portability, or an explicit skip naming any non-note handoff artifact when reporting is out of scope.

Specify verification: input, transformation, realised-sample, grouping, and denominator integrity; object comparability before any benchmark claim; which audit outputs and report inputs must exist; text-figure consistency when reporting; and which findings trigger a stop-and-ask or GPT Pro escalation — if the user accepts escalation, prepare the package with `$gpt-pro-handoff` (lean mode: surprise memo plus the decisive outputs).

### Save
Write or refresh the saved plan with `references/plan_template.md`; it is ready only when it passes the template's minimum quality check. Preferred location: a repo convention if one exists, otherwise `docs/plans/YYYY-MM-DD-<slug>-econ-plan.md`. The ordinary next step is `econ-work` on the saved plan; name the outputs, checks, briefs, and bundles `econ-work` should leave ready for later `econ-review`. Use `econ-review surface:plan` only when the plan is unusually large, risky, ambiguous, or intended for multi-agent execution. If a material question remains, ask it (blocking) and wait before saving — never finalise with it buried in `Open questions`.

## Hard stops

- Do not execute the plan inside the planning turn.
- Do not leave the objective, reader, reporting scope, or desired output implicit when they materially affect the work.
- Do not use `AGENTS.md` or `README.md` as the home for long research-state content, or create or update GitHub issues without approval.
- Do not hide missing evidence or ambiguities.
- Do not let a benchmark silently redefine the live research object.
- Do not plan to draft the note from raw diagnostics, manifests, or execution logs, or treat the execution note as the reader-facing note.
