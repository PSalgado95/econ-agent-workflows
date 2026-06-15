---
name: econ-work
description: "Execute economics research, empirical economics, or hybrid analysis-engineering work. Use when the task involves code changes, reruns, output inspection, interpretation, review-bundle preparation, GitHub issue-linked research work, or economist-facing note production from defended outputs. Work in order: execution, output inspection, interpretation brief, note brief, then note or figures."
---

<!-- GENERATED FROM CODEX SOURCE - DO NOT EDIT. Edit the Codex sources (skills/, .codex/agents/, references/) and run build_claude.py. -->

# Economist Execution Workflow

Execute the work without losing the research object, realised sample, audit trail, benchmark boundary, or reader-facing deliverable.

## Direct invocation contract

When directly invoked, stay inside the `econ-work` execution workflow. Never treat explicit skill invocation as casual advice or as permission to skip the staged empirical workflow.

A valid direct invocation must do one of these:
- execute from a saved plan, issue-linked work object, or clear work request;
- triage a bare request and write a short execution outline before non-trivial edits or reruns;
- ask one focused blocking question when the missing answer would materially change the baseline, estimand, output surface, rerun scope, note scope, or destructive-overwrite decision;
- route pure software work to the current Compound Engineering work skill; or
- label the response as advice-only when the user explicitly asked for advice rather than execution.

Do not start code changes, empirical reruns, output promotion, or note drafting until input triage and execution mode are explicit.

Route pure software tasks to the current Compound Engineering work skill, such as `compound-engineering:ce-work` when available.

Keep this file as the execution contract. Read `references/execution_reference.md` only when you need the exact templates or checklists for `interpretation_brief.md`, `note_brief.md`, `surprise_memo.md`, the output-consistency map, the verification ladder, the review bundle, the issue checkpoint comment, or the closeout format.

## Input

<work_object> #$ARGUMENTS </work_object>

If the input is empty, use `AskUserQuestion` and ask:
"What empirical or hybrid work should I execute? Please name the plan, issue, output, note, or concrete task."

## Input triage

Classify the input before execution:
- `saved plan`: a plan file or explicit execution document is provided -> read it and use it as the decision artifact;
- `bare empirical request`: no plan path is provided, but the empirical task is clear -> scan the relevant work surface, then write a short execution outline before non-trivial edits or reruns;
- `trivial one-off`: narrow check, inspection, or mechanical edit with low empirical stakes -> proceed compactly, but still state execution mode and closeout status;
- `issue-linked work`: a GitHub issue, issue number, or issue-derived task is provided -> treat the issue as coordination context, not analytical evidence;
- `missing or unclear work object`: the task, output, baseline, or rerun scope is unclear -> ask one focused blocking question before execution.

Do not require a saved plan for every small task. Do require an explicit execution outline for non-trivial bare requests.

## Core contract

Keep these distinctions explicit throughout the run:
- project backbone versus dated execution plan;
- plan labels versus incidental task names;
- GitHub issue coordination versus analytical evidence;
- the live research object versus any benchmark or comparison object;
- rerun outputs versus pre-existing outputs being inspected;
- audit outputs versus report inputs;
- the execution note versus the reader-facing note;
- observed facts versus diagnostic explanations versus limitations;
- surprising findings that justify escalation versus routine diagnostics that do not.

Default order:
1. code and run checks;
2. output inspection;
3. economic interpretation and headline triage;
4. if reporting is in scope, build the note brief;
5. only then draft the note and build figures.

Do not let the note become the place where the analysis is first figured out.

## Non-negotiables

- Keep the baseline, estimand, or descriptive object explicit before comparing results or writing claims.
- Distinguish outputs to build now, outputs kept for support, and outputs deliberately deferred.
- Treat missing raw or restricted data as a mode change, not as a minor caveat.
- When code changes the main output family, update the corresponding specification, manifest, and checks in the same unit of work.
- When code changes sample construction, missingness, grouping, denominator, weighting, or timing rules, refresh the corresponding audit before closing.
- When the plan provides stable labels, use those labels in execution notes, closeout, review bundle, and issue checkpoint comments.
- When work is issue-linked, update or draft issue comments only when the user requested or approved it.
- Use one writer per mutable empirical output family unless isolated output roots or worktrees are explicit. Mutable families include derived datasets, tables, figures, logs, model-spec ledgers, note drafts, review bundles, output manifests, and output specifications.
- Do not start a reader-facing note until the interpretation brief exists.
- If reporting is in scope, do not start drafting until the note brief exists.
- Keep the execution note and the reader-facing note separate.
- Do not leak workflow nouns or absolute paths into note, caption, or figure surfaces.

## Execution modes

Every non-trivial run must be classified before major edits or reruns:

`structure-only`
- required raw or restricted inputs are absent, inaccessible, stale, or intentionally not being rerun;
- allowed work includes code edits, manifests, checks, specifications, syntax checks, static validation, interpretation of already-existing outputs, note rewriting from defended outputs, and bundle preparation;
- forbidden claim: that the main empirical outputs were regenerated now.

`full empirical rerun`
- required inputs are present, usable, and the rerun is authorised;
- allowed work includes the full code and empirical path, including regenerated outputs that the plan treats as current.

If the task is note-only or bundle-only and does not regenerate outputs, keep it in `structure-only` and say clearly that existing outputs were interpreted or repackaged rather than rerun.

If the mode is `structure-only`, closeout must name the missing inputs or the exact reason the rerun stayed out of scope.

## Ask rather than guess

Use `AskUserQuestion` when the next step could materially change:
- the baseline, estimand, or main output;
- benchmark treatment;
- whether the run should remain `structure-only` or become a `full empirical rerun`;
- whether a destructive overwrite is acceptable;
- whether a new empirical branch should be opened;
- whether the task really includes a reader-facing note or figures; or
- whether a surprising finding deserves deeper follow-up or GPT Pro escalation.

Prefer one short question with a recommended default.

If `AskUserQuestion` is unavailable, ask concise numbered choices in chat, name the recommended conservative default, and wait for the user's answer for Class A choices.

## Choice classes

`Class A`
- estimand-defining;
- identification-defining;
- sample-boundary;
- baseline-defining;
- main-output choice;
- benchmark-treatment choice; or
- note-scope-defining choice when reporting is live.

Action: ask if unresolved. If forced to proceed, mark the choice as provisional and high-priority in the choice register.

`Class B`
- important specification or inference choice within the allowed hierarchy.

Action: choose using the plan or repo conventions, log it, and note credible alternatives worth stress testing.

`Class C`
- low-stakes implementation detail.

Action: choose directly and log only when the audit trail benefits.

## Plan-derived task tracking

For non-trivial work, create and maintain a task list using `update_plan` or the platform's equivalent after Phase 0 and before major edits or reruns.

Derive tasks from the actual work surface:
- saved-plan stages, work units, labels, and stop conditions;
- the user's concrete request when no saved plan exists;
- required inputs, output families, report inputs, and review surfaces;
- verification needs from the execution mode and research object; and
- interpretation, note, bundle, or issue-update obligations when they are in scope.

Do not impose a fixed universal checklist. A baseline rerun, output inspection, note rewrite, and bundle cleanup should produce different task lists. For trivial one-off work, a formal task list may be skipped, but the closeout must still state what was checked, what changed, and what remains uncertain.

Keep task statuses current as work progresses. Preserve plan labels when present, and add new tasks only when they are necessary to complete the authorised scope or to record a blocker/follow-up.

## Workflow

### Phase 0: Ingest the work surface

Read the plan when present, then read the current workflow note and current authority files.

If a saved plan is present, treat it as a decision artifact, not a progress log. Read enough of it to understand scope, labels, stop conditions, review route, and non-goals. Do not rewrite the plan body to track execution progress. If reality diverges from the plan, record the divergence in the task tracker, working notes, closeout, review bundle, or a follow-up plan recommendation.

Identify:
- objective;
- project-backbone document, if named;
- GitHub issue link or issue number, if named;
- stable plan labels for decisions, outputs, and work units;
- research question and estimand or descriptive object;
- baseline;
- current choice register;
- live object versus benchmark block;
- outputs in scope;
- whether reporting is in scope;
- whether a review bundle already exists; and
- which inputs are required for a real rerun.

If reporting is in scope, also identify:
- note type;
- intended reader;
- finished note format and render target;
- whether figures are required;
- whether there is an existing note to revise; and
- which existing artefacts are for support only and should not govern the note.

If no plan exists and the task is not trivial, write a short inline execution outline before editing anything.

If a plan names a project backbone such as `PROJECT_BRIEF.md`, read only the sections needed for the current work. Do not expand `AGENTS.md` or `README.md` into a research plan.

If a GitHub issue is named, treat it as coordination context:
- read it when `gh` or the GitHub connector is available;
- extract objective, done-when condition, linked branches or worktrees, and follow-up links;
- do not treat issue comments as a substitute for outputs, checks, or plans; and
- record whether issue updates are requested, approved, or out of scope.

### Phase 1: Lock the execution mode and input gate

Before major edits or reruns:
1. name the exact required inputs by file name, pattern, manifest, or known artefact signature;
2. verify that those actual inputs are present and usable;
3. classify the run as `structure-only` or `full empirical rerun`; and
4. record the result in the execution outline or working notes.

A directory such as `raw/` is never enough proof by itself.

Before promoting a run from `structure-only` to `full empirical rerun`, re-check:
- actual files and access conditions;
- rerun scope and authorised workstream;
- which outputs are stale or inherited versus which will be regenerated now;
- whether the active output specification still matches the intended run; and
- the stable entrypoint that will regenerate the intended surface.

### Phase 2: Set execution posture

Default posture:
- keep one blocking writer on mutable files;
- use deterministic entrypoints where possible;
- keep notebook state from becoming the only record of the analytical object; and
- use small read-heavy sub-agents only when they make the live evidence cleaner.

Use sub-agents for evidence collection, not for parallel writes.

For empirical branches and worktrees:
- record the current branch or worktree when it matters for later recovery;
- do not mix unrelated empirical lanes in the same closeout;
- when output folders are mutable, prefer one active writer unless the plan explicitly creates isolated output roots;
- separate newly refreshed outputs from inherited or inspected-only outputs.

### Phase 3: Stage 1 — code execution and run checks

For each code unit:
1. mark the unit in progress using the plan label when one exists;
2. read the relevant files and artefacts together;
3. implement the smallest authorised code change;
4. use stable entrypoints where possible;
5. record what actually ran and which outputs are newly generated versus pre-existing; and
6. run the unit's verification before moving on.

Mandatory checks inside Stage 1:
- helper-behaviour checks whenever a helper or rule directly defines probabilities, bins, sample keys, denominator rules, matching rules, timing rules, or any other object-defining parameter;
- output-specification-first checks whenever the main output family changes;
- model-spec-ledger refreshes whenever realised estimates or model-based descriptives are in scope and the realised model surface changed materially.

Stage 1 close condition:
- code changes were made or deliberately skipped with reason;
- execution mode is still correct; and
- changed output families have current specification and checks.

### Phase 4: Stage 2 — output inspection and empirical audit

Read the realised outputs, not just the scripts that made them.

Inspect, when relevant:
- sample accounting;
- merge and key diagnostics;
- missingness and support diagnostics;
- weighting, grouping, and denominator checks;
- canonical tables and figures for the main object; and
- benchmark diagnostics when the task is benchmark-facing.

Whenever sample formation, overlap, weighting, grouping, denominator, or support restrictions matter, make the realised sample legible before moving to interpretation.

If a diagnostic claim may later enter the note, organise the supporting audit in this order:
1. total impact;
2. composition of affected cases; and
3. selection consequence for the final analytical sample or comparison.

Stage 2 close condition:
- realised outputs were inspected;
- the main audit surfaces exist or were refreshed; and
- candidate report inputs are separated from backend diagnostics.

### Phase 4b: Analysis surface simplification before interpretation and review

Before interpretation, note writing, review bundle preparation, or closeout, simplify the analysis surface without deleting evidence.

Classify relevant outputs and artefacts as:
- `refreshed`: regenerated in this run;
- `inherited`: produced earlier and still intentionally used;
- `inspected-only`: read or interpreted in this run but not regenerated;
- `stale`: likely superseded, no longer current, or inconsistent with the active object;
- `support-only`: useful diagnostic or backend evidence, but not a report input;
- `report-input`: candidate table, figure, note excerpt, or bundle surface for reader-facing use.

Check for:
- duplicate execution paths;
- redundant diagnostics;
- unclear figure or table naming;
- old benchmark or comparison objects drifting into the live object;
- output folders that mix refreshed and inherited objects without a manifest note.

Do not delete, overwrite, or hide stale evidence without explicit approval. Mark it, separate it from report inputs, or recommend a cleanup follow-up.

Surface simplification close condition:
- report inputs are separated from support-only diagnostics;
- stale or inherited outputs are named rather than silently trusted;
- no destructive cleanup was performed without approval.

### Phase 5: Stage 3 — economic interpretation and headline triage

Stop after Stage 2 and answer explicitly:
- what is the main finding;
- what actually matters out of all the things in the data;
- what should be visualised; and
- what follow-up checks or deeper investigation are immediately implied.

Build `interpretation_brief.md` using the template in `references/execution_reference.md`.

Tag candidate claims as one of:
- `observed fact`;
- `diagnostic explanation`;
- `limitation`; or
- `open question`.

If a reader-facing note is required, build `note_brief.md` after the interpretation brief and before any drafting. Use the template in `references/execution_reference.md`.

Rules:
- build the note brief from the interpretation brief plus defended report inputs;
- do not build it from raw diagnostics alone;
- do not let the execution note or file names determine the narrative; and
- if the note is a rewrite, diagnose the old note first and then update the brief before rewriting.

If execution reveals a genuinely surprising finding, write `surprise_memo.md` using the template in `references/execution_reference.md` and ask whether the user wants GPT Pro escalation when the finding is materially important, not explained by a quick definitional or sample check, and likely to benefit from a deeper second opinion.

Stage 3 close condition:
- the interpretation brief exists;
- the note brief exists when reporting is in scope;
- the main finding and figure priority are explicit; and
- the main-text versus appendix split is explicit.

### Phase 6: Stage 4 — note writing and figures

Only start this stage after Stage 3 is complete.

If a reader-facing note is in scope:
- use `econ-note-writing` as the main drafting and rewriting layer;
- provide `note_brief.md`, `interpretation_brief.md`, the output-consistency map, tagged source material, the existing note when revising, and figure notes when relevant; and
- revise from the brief rather than line-editing machine language sentence by sentence.

Format rule:
- if the repo already has a viable TeX/PDF note path, the finished note
  deliverable is `.tex` plus rendered `.pdf` unless the user explicitly asked
  for another format;
- Markdown can be a drafting scaffold, but not the finished note in that case;
- if figures are in scope and already exist, insert them rather than leaving
  placeholders.

Use `writing-clear-prose` only for non-note human-facing documents or for local sentence-level polish after the note structure and register are already correct.

When note, memo, table, or figure claims are in scope, keep an output-consistency map current using the minimum structure in `references/execution_reference.md`.

Before closing a note or figure pack, run:
- the text-figure consistency test; and
- the reader-facing note integrity test in `econ-note-writing`.

Stage 4 close condition:
- note structure is economist-facing;
- figure order reflects the interpretation brief and note brief;
- the output-consistency map is current when note-facing claims are in scope; and
- report paths are portable; and
- when the agreed note format is `tex-plus-pdf`, the `.tex` and `.pdf`
  artefacts both exist or the blocker is named explicitly.

### Phase 7: Verification ladder

Run the relevant checks from `references/execution_reference.md`.

At minimum, cover the levels that apply:
- input integrity;
- code and helper integrity;
- transformation integrity;
- realised-sample audit;
- grouping and denominator integrity;
- object comparability;
- output-specification integrity;
- text-figure and report-build integrity;
- interpretation discipline;
- reader-facing note integrity; and
- reproducibility rerun status.

For hybrid work, add targeted software checks such as tests, lint, interface checks, and manifest synchronisation where those surfaces matter for analytical trust.

### Phase 8: Review bundle and closeout

If interpretation, adjudication, or external review is in scope, build or refresh a compact bundle using the minimum structure in `references/execution_reference.md`.

Default review target:
- empirical or hybrid work -> `econ-review`;
- pure software -> the current Compound Engineering review skill.

Review-tier routing:
- claim-bearing empirical changes should route to at least `econ-review tier:standard`;
- coauthor, supervisor, paper, appendix, replication, or public-facing promotion should route to `econ-review tier:promotion`;
- changed sample construction, estimand, specification, weighting, clustering, inference, treatment timing, inclusion/exclusion rules, or headline output should not route to `tier:quick`.

Before closing, write a compact evidence pulse:
- what changed in the research object, sample, outputs, note surface, or review surface;
- what became more trustworthy;
- what became weaker, unresolved, or newly risky;
- which outputs were refreshed, inherited, inspected-only, or scaffolded;
- which plan labels, issue numbers, branch/worktree names, or output files the next session should use; and
- what should be planned next.

Route durable lessons to the lightest appropriate surface:
- issue comment when the work was issue-linked and the user approved an update;
- project backbone when the paper/data-project state changed, but draft substantive updates in the closeout and apply them only when the user requested or approved the update;
- README only when the repo dictionary changed;
- dated follow-up plan when the next round needs planning; and
- closeout only when the lesson is task-local.

Old memos, exploratory reports, GPT bundles, and project briefs are not durable update targets by default. Treat them as leads unless they were explicitly reviewed or accepted for a defined purpose, and trace any claim back to the underlying source, data output, script, or review finding before relying on it.

Add a reusable lesson checkpoint before the recommended next command:
- `Reusable lesson checkpoint: none` when the run did not reveal a reusable lesson;
- `Reusable lesson checkpoint: closeout-only` when the lesson is task-local and should stay in the closeout;
- `Reusable lesson checkpoint: econ-compound candidate` when the run revealed a reusable economics research lesson that future `econ-plan`, `econ-work`, or `econ-review` should consult.

If the checkpoint is `none`, keep it to one compact line and do not turn the closeout into a reflection exercise.

When the checkpoint is `econ-compound candidate`, name the lesson in one sentence and recommend `econ-compound` with the relevant plan, review, output, note, source bundle, or closeout path. Do not silently write durable learning notes from `econ-work` unless the user explicitly asked for learning capture or the larger autonomous run explicitly includes compounding.

Use the issue checkpoint comment and closeout formats in `references/execution_reference.md`.

Completion gate:
- this run is not complete until the closeout states objective, domain mode, execution mode, furthest stage reached, output status, analysis-surface simplification status, verification performed, interpretation/note status, review-bundle or review-route status, evidence pulse, reusable lesson checkpoint, blockers or residual risks, and recommended next command;
- a script run, a generated file, or one passing check is not enough to declare completion;
- for trivial one-off work, use a compact closeout, but still state execution mode, what was checked or changed, output status, remaining risk, and next step.

## Hard stops

- Do not skip from code execution straight to note writing.
- Do not treat generated outputs as understood until they were inspected.
- Do not write the note directly from raw diagnostics without an interpretation brief and, when reporting is in scope, a note brief.
- Do not declare success on the basis of one passing run alone.
- Do not leave the baseline, estimand, or execution mode implicit.
- Do not treat folder existence as proof that required data are present.
- Do not change the output surface without updating the corresponding specification, manifest, and checks in the same unit.
- Do not let pre-existing outputs be mistaken for rerun outputs after a `structure-only` pass.
- Do not let the execution note stand in for the reader-facing note.
- Do not let multiple writers mutate the same empirical output family unless isolated roots or worktrees are explicit.
- Do not delete, overwrite, or hide stale empirical evidence without explicit approval.
- Do not silently update `PROJECT_BRIEF.md` or another project-backbone document with substantive interpretation, claim-budget, baseline, or bottleneck changes.
- Do not treat GitHub issue text as analytical evidence without checking the actual plan, outputs, code, or bundle.
- Do not write durable research-state updates into `AGENTS.md` or `README.md` unless the change is truly an agent rule or repo dictionary change.
