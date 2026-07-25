---
name: econ-work
description: "Execute empirical or computational economics work from a plan or a clear request, keeping the research object, realised sample, and audit trail intact. Use when the task is to run or rerun code, inspect and audit realised outputs, interpret results, draft an economist-facing note or figures from defended outputs, prepare a review bundle, or carry out issue-linked research work. Not for pure software engineering with no research object, not for planning (use econ-plan) or reviewing (use econ-review)."
---

<!-- GENERATED FROM CODEX SOURCE - DO NOT EDIT. Edit the Codex sources and run build_claude.py. -->

# Economist Execution Workflow

Execute the work without losing the research object, realised sample, audit trail, benchmark boundary, or reader-facing deliverable. This file is the contract; read `references/execution_reference.md` at the stage that needs a template or checklist (each pointer below says when).

## Intake

Treat the arguments passed with this invocation, or the user's current request, as the work object. If it is empty, ask (blocking) what to execute — the plan, issue, output, note, or concrete task. Classify before touching anything:

- **Trivial one-off** — a narrow check, inspection, or mechanical edit with low empirical stakes. Proceed compactly: no task list, no review bundle, a compact closeout. This is the expected path for small work; do not force the full workflow onto it.
- **Saved plan** — read it as the decision artifact (not a progress log) and execute its stages; record divergence in the task tracker or closeout rather than rewriting the plan body.
- **Bare empirical request** — clear task, no plan. Scan the work surface, then write a short execution outline before any non-trivial edit or rerun.
- **Issue-linked work** — read the issue as coordination context only (objective, done-when, linked branches). Record whether issue updates are requested, approved, or out of scope.
- **Unclear work object** — inspect the available surface, then ask one decision per question and continue until the work object is shared clearly enough to execute.

Route pure software work to the current Compound Engineering work skill (`compound-engineering:ce-work` when available). If the user asked for advice rather than execution, label the response advice-only. Do not start code changes, reruns, output promotion, or note drafting until the task, research object, scope, and rerun authority are sufficiently understood.

## Core invariants

Keep these distinctions explicit for the whole run; collapsing any of them is how research trust is lost:

- project backbone vs dated execution plan; plan labels vs incidental task names;
- the live research object vs any benchmark or comparison object;
- rerun outputs vs pre-existing outputs being inspected;
- audit outputs vs report inputs; the execution note vs the reader-facing note;
- observed facts vs diagnostic explanations vs limitations;
- research-code role and the maturity expected now.

Default order of work: (1) code and run checks; (2) output inspection; (3) economic interpretation and headline triage; (4) note brief when reporting is in scope; (5) only then the note and figures.

When code changes the main output family, update its specification, manifest, and checks in the same unit. When it changes sample, missingness, grouping, denominator, weighting, or timing rules, refresh the corresponding audit before closing. Keep one writer per mutable output family (derived datasets, tables, figures, logs, ledgers, note drafts, bundles, manifests, specs) unless isolated roots or worktrees are explicit; use sub-agents for evidence collection, not parallel writes.

## Run boundary and provenance

Before major edits or reruns, establish what can actually be executed. A directory such as `raw/` is never proof that the required inputs are present. Check the actual files and access conditions; the authorised scope; which outputs or model objects are stale, inherited, or expected to be regenerated now; whether the active specification or computational object matches the intended run; and the stable entrypoint that regenerates the surface.

When required raw, restricted, model, simulation, calibration, or numerical inputs are unavailable or intentionally outside scope, code, manifests, checks, specifications, static validation, and interpretation of defended existing outputs may still proceed. State plainly that the main outputs were not regenerated, name the missing input or scope reason, and never present inherited outputs as fresh. When inputs and authority are present, run the appropriate empirical or computational path and report exactly what was regenerated.

## Choice classes and questions

Asking good blocking questions is part of building the task with the researcher, not an interruption. Use the platform's blocking-question tool (`AskUserQuestion`; the Claude build translates it), not plain chat text. Ask one decision per question, with the context that makes it answerable: what the decision affects, the plausible options with their tradeoffs, and a recommended conservative default. Continue until the objective, research object, scope, assumptions, methods, outputs, audience, and relevant constraints are sufficiently understood. Do not guess missing context merely to avoid asking, and never bury a material question in a closeout or "open questions" list.

- **Class A** — estimand, identification, sample boundary, baseline, main output, benchmark treatment, or note scope when reporting is live. Ask before resolving any Class A choice, any destructive overwrite, or any new empirical branch. In an autonomous parent run, return an unresolved Class A choice to the parent; do not mark it provisional and continue silently.
- **Class B** — a specification or inference choice within the allowed hierarchy. Choose from the plan or repo conventions, log it, and note credible alternatives worth stress-testing.
- **Class C** — a low-stakes implementation detail. Choose directly; log only when the audit trail benefits.

Log Class A/B choices as rows in `choice_register.md` using the template in `references/execution_reference.md`.

## Workflow

For non-trivial work, keep a task list (the platform's task tool) derived from the actual work surface — plan stages, required inputs, output families, verification needs, and any interpretation, note, bundle, or issue obligations — not a fixed universal checklist.

### Stage 0 — Ingest the work surface

Read the plan when present (as a decision artifact, not a progress log), the current workflow note, and only the authority-file sections the work needs; do not expand a project backbone or README into a research plan. Identify:

- objective; project backbone and GitHub issue when named; stable plan labels;
- research question and estimand or descriptive object; baseline; current choice register;
- the live object vs any benchmark block; outputs in scope; code role when code is in scope;
- whether reporting is in scope, and if so the reader, finished note format, and whether figures are required;
- which inputs a real rerun requires, and whether a review bundle already exists.

*Close when:* the objective, baseline, research object, feasible run boundary, and review route are named, and a task list exists for non-trivial work.

### Stage 1 — Code execution and run checks

Implement the smallest authorised change per code unit, using stable entrypoints, and record what actually ran and which outputs are newly generated vs pre-existing. Run the unit's verification before moving on. When writing or editing research code, the taste rules and worked examples live in `references/research-code-quality.md`; when the language is R, also consult `references/r-defaults.md` for package and tool defaults. Mandatory inside Stage 1:

- the research-code-quality floor: descriptive names that put the economic object before the plumbing, visible entrypoints, named object-defining parameters, no stale debug or test fragments, analytical logic separated from formatting when practical;
- input checking matched to provenance (the Provenance Ladder in `references/research-code-quality.md`): validate external/untrusted inputs properly; give self-authored workbooks and configs one thin boundary check, never repeated defensive parsing; check generated intermediates on the economic object, not every column; no defensive scaffolding, option flags, or fallback routes in internal helpers for callers that do not exist;
- object-defining assertions for row counts, keys, merge cardinality, denominators, weights, dimensions, convergence, residuals, or identities;
- helper-behaviour checks when a helper defines probabilities, bins, sample keys, denominators, matching, or timing;
- output-specification-first checks when the main output family changes, and a model-spec-ledger refresh when the realised model surface changed;
- for computational work, checks matched to the object (dimensions, convergence, residuals, feasibility, conservation, market clearing, deterministic simulation, small transparent benchmarks).

*Close when:* code changed or was skipped with a reason, what ran is recorded, and changed output families have current specifications and checks.

### Stage 2 — Output inspection and empirical audit

Read the realised outputs, not just the scripts that made them: sample accounting, merge and key diagnostics, missingness and support, weighting, grouping, and denominator, canonical tables and figures, and benchmark diagnostics when benchmark-facing. Make the realised sample legible before interpreting. For a diagnostic that may enter the note, organise the audit as total impact → composition of affected cases → selection consequence. Then simplify the surface without deleting evidence: tag every output with the two orthogonal tags in `references/execution_reference.md` ("Output provenance status vocabulary") — provenance status (`refreshed`/`inherited`/`inspected-only`/`scaffolded`/`stale`) and role tag (`support-only`/`report-input`).

*Close when:* outputs were inspected, the audit surfaces exist or were refreshed, report inputs are separated from support-only diagnostics, and stale or inherited outputs are named rather than silently trusted.

### Stage 3 — Economic interpretation and headline triage

Stop and answer: the main finding; what actually matters in the data; what to visualise; what follow-up is immediately implied. Build `interpretation_brief.md` (template in the reference), tagging claims as observed fact / diagnostic explanation / limitation / open question. When reporting is in scope, build `note_brief.md` after it, as a delta on the interpretation brief, from defended report inputs, never from raw diagnostics; if revising an existing note, diagnose the old note first.

If the run turns up a genuinely surprising finding, write a surprise memo (HTML via `econ-html-memo` when installed, plain standalone HTML under the same content discipline otherwise). Keep it as a normal local user-facing output: state the minimal validation already completed, plausible explanations, decisive missing evidence, and the research decision or next local check needed to continue.

*Close when:* the interpretation brief exists, the note brief exists when reporting is in scope, and the main finding, figure priority, and main-text-vs-appendix split are explicit.

### Stage 4 — Note writing and figures

Only after Stage 3. Draft from the note brief, interpretation brief, output-consistency map, tagged sources, and the existing note when revising — revising from the brief, not line-editing machine sentences. Keep the output-consistency map current (minimum structure in the reference) whenever note, memo, table, or figure claims are in scope. Standalone researcher-facing notes and memos default to HTML through `econ-html-memo` when installed; use plain HTML under the same discipline otherwise. Produce TeX and PDF only when the user explicitly requests those formats or explicitly asks for integration into a paper. Markdown is an agent-facing drafting scaffold. Insert existing figures rather than leaving placeholders. Before closing, run the text-figure consistency test and the local **Reader-facing note gate** in `references/execution_reference.md`.

*Close when:* the note is economist-facing, figure order follows the briefs, the consistency map is current, report paths are portable, and the explicitly agreed output format exists or the blocker is named.

### Verify and close

Run the verification ladder in `references/execution_reference.md`, covering only the rungs that apply; scale named tests by code role. Build or refresh the review bundle (minimum structure in the reference) only when the closeout routes to `econ-review` on a bundle or mixed surface, or the work goes to a coauthor or external reviewer — otherwise skip it. Default review target: empirical or hybrid work → `econ-review` (apply its escalation triggers; when in doubt, the stricter tier); pure software → the Compound Engineering review skill.

Fill the closeout in `references/execution_reference.md`; the run is complete only when it is filled — a script run, a generated file, or one passing check is not completion. Route any durable lesson to the lightest surface (issue comment when issue-linked and approved; a drafted project-backbone update applied only on approval; a dated follow-up plan; or closeout-only). Old memos, exploratory reports, and externally supplied packages are leads, not authority, until traced to the underlying source, output, script, or review finding.

## Internal return to `econ-lfg`

An `econ-lfg` parent may supply the private caller contract `caller_contract: econ-lfg/v1`. This is orchestration metadata, not a user-facing option. Return the inline `econ-work-for-caller/v1` envelope defined in `references/execution_reference.md`. Do not deliver the final user closeout or perform Git actions; the parent owns the next stage and final handoff.

## Hard stops

Each is a named failure this workflow exists to prevent; the stage close-conditions above enforce them.

- Do not write the note or memo before the realised outputs are inspected and the interpretation brief exists (and the note brief when reporting is live).
- Do not let old or inherited outputs be presented as freshly regenerated.
- Do not stage, commit, or push unless the user explicitly requests that Git action.
- Do not treat GitHub issue text as analytical evidence without checking the actual plan, outputs, code, or bundle.
- Do not silently change the baseline, sample, estimand, benchmark treatment, or note scope — those are Class A; ask first.
- Do not write a durable learning or project-state update (including `PROJECT_BRIEF.md`, `CLAUDE.md`, or `README.md`) without its evidence paths and scope, or without approval for a substantive backbone change.
- Do not delete, overwrite, or hide stale empirical evidence without explicit approval.
