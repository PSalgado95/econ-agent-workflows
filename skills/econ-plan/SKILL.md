---
name: econ-plan
description: "Build plans for empirical economics or hybrid analysis-engineering work. Use when a user wants an execution plan, scoping decision, workflow design, GitHub issue-linked plan, or project-brief-backed plan for data, estimation, output, interpretation, or economist-facing note tasks. Restate the empirical task plainly, force an explicit reporting-class decision, ask rather than infer when it is materially unclear whether a reader-facing note or figures are part of the deliverable, and hand off a stage-sequenced plan to econ-work."
argument-hint: "[optional: empirical task, existing plan path, project brief path, GitHub issue, output/table/figure to plan around]"
---

# Economist Planning Workflow

Plan only. Do not execute code, run empirical work, build outputs, or draft the note in the same turn unless the user later gives a separate instruction.

## Direct invocation contract

**When directly invoked, always plan.** Never classify a direct invocation as "not an economist planning task" and abandon the workflow. If the input is unclear, ask a blocking clarifying question or use the intake steps below to establish enough context, but always stay in the `econ-plan` planning workflow.

A valid direct invocation must do one of two things before the turn is complete:
- ask one focused blocking question, with enough context to answer, when a missing answer would materially change the plan;
- write or refresh a saved plan file, then return the mandatory visible output summary as a receipt.

Writing or refreshing a saved markdown plan is required for every direct invocation that does not end with a blocking question. The saved file is the planning artifact; the chat response is only the summary and handoff. An inline-only plan is not a valid completion for direct invocation. Do not use a no-save path unless file creation is genuinely blocked by missing write access, missing workspace location, or a failed file operation. State the blocker and exact no-save reason if no plan file is written.

For direct software invocations, still produce the `econ-plan` artifact. Use `domain_mode: hybrid` when the task touches empirical workflow, reproducibility, outputs, data pipelines, or research repo structure; otherwise use `domain_mode: software-handoff`. Keep `domain_mode` separate from `reporting_class`.

Keep this file as the workflow contract. Read `references/plan_template.md` only when writing or refreshing the saved plan file. Read `references/project_brief_template.md` only when the user approves creating a project-backbone document.

## Interaction method

When asking a material planning question, use the platform's blocking question tool when available, such as `request_user_input` in Codex. Fall back to structured numbered choices in chat only when no blocking tool exists or the call errors. Never silently skip a material question.

Ask one decision at a time when possible. Include enough context, examples, or tradeoffs for the user to answer confidently, and name a conservative default when one exists.

## Planning input

<planning_input> #$ARGUMENTS </planning_input>

If the input is empty, use the interaction method above and ask:
"What would you like to plan? Please describe the empirical task and say whether you also want a reader-facing note or figures."

If the input is present but unclear or underspecified, use Phase 0 only to check whether the missing answer is already explicit in local context. If it remains material after that read, ask one blocking clarifying question before writing or saving the plan.

Saved plan documents must use repo-relative paths for files, folders, scripts, outputs, and evidence, such as `analysis/build_sample.do` or `outputs/tables/main.csv`, not absolute paths such as `/path/to/repo/analysis/build_sample.do`. Use absolute paths only in the final chat response when linking the saved plan file for the user.

## Mandatory visible output skeleton

Unless the turn ends with one focused blocking question, the visible response must include these fields in this order:
1. `Task restatement` - one plain-language paragraph saying what is in scope, out of scope, and what assumption would change the plan.
2. `Classification` - `domain_mode`, `reporting_class`, `round_type`, and secondary lanes if any.
3. `Decision frame` - final human reader, desired output, project backbone used or proposed, GitHub issue action, if any.
4. `Central bottleneck` - the one constraint the plan is organised around.
5. `Execution path` - the four `econ-work` stages, with the expected stop conditions.
6. `Review and handoff` - saved plan path or explicit no-save reason, plan-review route or skip reason, and recommended next command.
7. `Open questions` - only non-blocking questions or deferred choices; material questions must be asked with the interaction method above before finalising.

## Core contract

A ready plan must:
- briefly restate the empirical task in plain language before committing to the plan;
- identify the decision problem, not just the topic;
- identify the final human reader and output;
- name any project-backbone document used, or say that none was found;
- classify the reporting class explicitly as `coding-only`, `analysis-only`, `analysis-plus-note-report`, or `analysis-plus-note-report-plus-figures`;
- classify the round as `current-evidence-cleanup`, `current-evidence-clarification`, or `new-empirical-work`;
- isolate one central bottleneck;
- use sparse stable labels for important decisions, outputs, work units, and review findings;
- hand off a four-stage execution path to `econ-work`:
  1. code and run checks;
  2. output inspection;
  3. economic interpretation and headline triage;
  4. note writing and figures.

For `coding-only` or `analysis-only` plans, keep Stage 4 as an explicit skip stage: state that no reader-facing note or figures are in scope, list any handoff artifact if relevant, and mark `econ-note-writing` as not called.

If reporting is in scope, the plan must also lock the reader-facing note contract before execution:
- note type;
- question the note must answer;
- what the note is for;
- what the reader should know by the end;
- what definitions must appear before findings;
- finished note format and render target;
- whether figures are required;
- what belongs in the appendix or execution note rather than the main text.

Always keep:
- the live empirical object separate from any benchmark or comparison block; and
- audit outputs separate from report inputs.

## Planning rules

When the user names a specific file, folder, GitHub issue, prior plan, output, table, figure, script, register, dataset, command, or document, treat it as authoritative planning input. Inspect it before substituting a generic alternative. If it cannot be found, say so explicitly.

Do not pre-write implementation code or detailed command choreography in the plan. It is fine to name likely scripts, outputs, checks, and expected changes, but execution details belong to `econ-work`.

## Plan quality bar

A saved `econ-plan` is ready only when it passes the minimum quality check in `references/plan_template.md`.

## Plain-language restatement gate

Before writing or refreshing a plan, state the task in one short paragraph:
- what the user appears to want;
- what is in scope;
- what is out of scope; and
- which assumption would materially change the plan, if any.

Do not turn this into a long interview. If the task is clear, continue. If one missing answer would materially change the reporting class, output surface, baseline, benchmark treatment, or rerun scope, ask one focused question before writing the plan.

Example:

> I understand this as: rerun the main figure under the current sample rule, inspect whether the headline changes, and prepare a coauthor-facing note only if the result is stable. I will not change the identification strategy unless you ask.

## Ask rather than infer

Use the interaction method above after a first repo read whenever the answer could materially change the plan.

Favor asking early over guessing silently. A good `econ-plan` question is decision-relevant, answerable from the user's perspective, and includes the context needed to choose between options. It should clarify the empirical object, output surface, reader, rerun scope, benchmark treatment, or plan artifact. Do not bury a material decision in the final `Open questions` section.

Ask when any of these are materially unclear:
- the objective or decision problem;
- the intended reader;
- the reporting class;
- the desired output surface, such as note, memo, report, figure pack, or review bundle;
- the note type or what the note needs to contain when reporting is in scope;
- the baseline or main comparison;
- whether a benchmark is a diagnostic comparison or the target to match;
- whether an expensive rerun or destructive overwrite is acceptable; or
- whether the round is mainly `current-evidence-cleanup`, `current-evidence-clarification`, or `new-empirical-work`.

Mandatory clarification triggers:
- if the task could plausibly be either `analysis-only` or `analysis-plus-note-report`, ask rather than infer;
- if reporting is plausibly in scope but the note type, note contents, or purpose are not already clear from the request and local context, ask rather than infer;
- if figures may be part of the intended deliverable and that is not already clear, ask rather than choose for the user.

Question rules:
- ask one decision at a time when possible;
- include enough context, examples, or tradeoffs for the user to answer confidently;
- say why the answer matters for the plan; and
- give a recommended default when a conservative default exists.

If uncertainty remains after reasonable clarification, mark it explicitly as an assumption, non-blocking open question, or stop condition. Use `Open questions` only for non-blocking leftovers or choices intentionally deferred to execution; blocking or plan-shaping questions must be asked before the final plan.

## Domain routing

Classify `domain_mode` before writing the plan:
- `empirical` -> data, estimation, descriptive outputs, interpretation, reporting, benchmark comparison, or reproducibility;
- `hybrid` -> both empirical integrity and software implementation integrity matter;
- `software-handoff` -> pure app, API, UI, infra, tooling, refactor, or debugging work with no empirical, output, interpretation, or reporting stakes.

If the task touches sample construction, variable definitions, outputs, interpretation, note writing, reproducibility, data pipelines, or research repo structure, keep it in the economist workflow. For direct invocations, never stop at `software-handoff`; instead, produce the best `econ-plan` planning artifact.

## Workflow

### Phase 0: Locate the active planning surface

Read the request and find the active planning surface:
- existing plan;
- project-backbone document;
- workflow note;
- methods note;
- benchmark note;
- prior note or report; or
- source-of-truth code or config.

If the user references an existing plan, or there is an obvious recent matching plan:
- read it;
- ask whether to update it in place or create a new plan when the choice is ambiguous; and
- if updating, revise only still-relevant sections rather than creating a duplicate. Plans do not carry execution progress logs.

Treat `AGENTS.md` and `README.md` carefully:
- `AGENTS.md` is for compact repo and agent rules because it enters every session. Do not make it the research plan.
- `README.md` is the repo dictionary and orientation layer. Do not make it the live empirical plan.
- Use both for orientation when present, then look elsewhere for the project backbone.

Project-backbone discovery order:
1. repo-specific project brief named in `README.md` or docs index;
2. `PROJECT_BRIEF.md`;
3. `RESEARCH_BRIEF.md`;
4. paper outline, coauthor memo, methods note, current project note, or equivalent;
5. the most relevant dated plan only when it is clearly acting as the current backbone.

Interpret the project backbone as the place for:
- research question or descriptive object;
- data vintage and current sample boundary;
- main definitions and benchmark treatment;
- active empirical tracks;
- current canonical outputs;
- claim budget and intended reader; and
- open decisions or bottlenecks.

If no backbone exists and the task is broad enough that future sessions will need the context, ask whether to create a compact `PROJECT_BRIEF.md`. Do not ask for narrow one-off tasks.

### Phase 0b: Detect GitHub issue coordination

If the request names a GitHub issue URL, `#123`, or `repo#123`, treat the issue as coordination context:
- read it when `gh` or the GitHub connector is available;
- summarize only the decision-relevant context;
- keep plans, outputs, and review bundles as the analytical record; and
- add an `Issue coordination` section to the plan.

If the task is a diagnosis, follow-up implementation lane, robustness/sensitivity lane, or note/paper preparation lane, and GitHub issue tracking is available or already used in the repo, ask whether the user wants an issue drafted or created. Never create or update issues without an explicit request or approval.

Preferred plan locations:
- repo convention if one exists;
- otherwise `docs/plans/YYYY-MM-DD-<slug>-econ-plan.md`;
- fallback `.codex/plans/YYYY-MM-DD-<slug>-econ-plan.md`.

### Phase 1: Write the decision frame first

Before building workstreams, lock:
- `Objective`;
- `Project backbone`;
- `Issue coordination` when issue-linked;
- `Reader contract`;
- `Reporting class`;
- `Reader-facing note contract` when reporting is in scope;
- `Round type`;
- secondary lanes, if any;
- `Central bottleneck`.

Round type rules:
- mixed tasks are allowed, but choose one `round_type` and label secondary lanes explicitly;
- `current-evidence-cleanup` means the validated evidence already exists and the work is mainly exposition, structure, packaging, or bounded correction;
- `current-evidence-clarification` means the main object exists but a targeted diagnostic or comparison is still needed before writing a confident note;
- `new-empirical-work` means the object, sample, variable, benchmark treatment, or main output family is not yet live and must be created or materially extended.

Anti-sprawl rule:
- for cleanup or clarification rounds, default to the smallest correct next round;
- do not reopen broad adjacent branches unless the central bottleneck truly requires it.

### Phase 2: Gather and classify local evidence

Read local material before finalising the plan. Minimum local research normally includes:
- object-defining code, config, scripts, or notebooks;
- current outputs and checks;
- active workflow notes;
- prior plans or choice registers when relevant;
- prior notes, reports, or bundles when relevant; and
- benchmark or comparison material when the task is benchmark-facing.

Build a compact evidence map with these buckets:
- `live and checked`;
- `live but unchecked or secondary`;
- `missing relative to the requested target`;
- `ambiguous or unverifiable with current evidence`.

Call out missing evidence or ambiguities before leaning on them.

### Phase 3: Add read-only investigation only when it clarifies the evidence map

Use extra read-only investigation only when it materially clarifies source-of-truth files, benchmarks, selection risks, reproducibility, or hybrid implementation risks. Do not build a large planning apparatus by default.

### Phase 4: Lock definitions, comparisons, and deliverables

Before sequencing execution, make these explicit:
- research question and estimand, or the descriptive object;
- definition registry for terms that can drift;
- source-of-truth files for the live object versus supporting or benchmark files;
- interpretation scope;
- audit outputs;
- report inputs.

If reporting is in scope, also lock:
- the note type;
- the question or puzzle the note must answer;
- the one-sentence headline the note is allowed to make if the evidence holds;
- the definitions and sample distinctions that must appear before findings;
- the finished note surface, such as `tex-plus-pdf` or `markdown-only`, and
  the render target when relevant;
- the likely headline figure; and
- what belongs in the appendix or execution note rather than the main text.

Do not draft the note contract from raw diagnostics alone.

Default note-format rule:
- if the repo already has a viable TeX/PDF note path, default to `.tex` plus
  `.pdf` for substantive reader-facing notes;
- use Markdown only when the user explicitly wants it or the repo cannot render
  PDF.

### Phase 5: Design the four-stage execution path for `econ-work`

Every non-trivial plan must hand off the same stage sequence used by `econ-work`.

`Stage 1: Code and run checks`
- likely files or entrypoints;
- expected generated objects;
- whether the task is probably `structure-only` or a `full empirical rerun`;
- helper, manifest, or interface checks; and
- stop conditions if required inputs are absent or stale.

`Stage 2: Output inspection`
- realised outputs that must be inspected before interpretation;
- sample, grouping, denominator, missingness, and overlap audits;
- audit-layer outputs versus report-input outputs; and
- accounting objects needed to defend the explanatory text.

`Stage 3: Economic interpretation and headline triage`
- where the workflow must stop and decide what the main finding is, what matters, what should be visualised, and which follow-up checks are implied;
- how the workflow will separate observed facts, diagnostic explanations, limitations, and open questions;
- whether `interpretation_brief.md` is required; and
- whether `note_brief.md` is required.

`Stage 4: Note writing and figures`
- note or memo structure;
- definitions and sample distinctions that must appear before findings;
- likely figure order and figure budget;
- what benchmark material belongs in the main text versus appendix;
- text-figure consistency checks;
- report-build portability checks; and
- when to call `econ-note-writing`.

For `coding-only` or `analysis-only` plans, Stage 4 should explicitly say it is skipped and name any non-note handoff artifact instead.

Use `writing-clear-prose` only for non-note prose or for local sentence-level polish after the note structure already works.

### Phase 6: Write ordered execution stages

Use the lightest structure that still protects the object. For most empirical tasks, one ordered section per stage is enough.

Use stable labels sparingly:
- prefer domain labels already present in the repo, such as case IDs, issue numbers, branch names, output filenames, or fixed vocabulary fields;
- use generic labels only when no clearer label exists:
  - `D1`, `D2`: empirical decisions, definitions, sample rules, benchmark treatments;
  - `O1`, `O2`: outputs, figures, tables, bundles;
  - `U1`, `U2`: work units or stages;
  - `F1`, `F2`: review findings reserved for `econ-review`;
- do not label every small task.

Each stage or work unit should contain:
- goal;
- mode;
- main files or artefacts;
- inputs required;
- outputs expected;
- checks and audits;
- stop conditions;
- user-question trigger; and
- review route.

Split unknowns explicitly:
- `resolved before planning` - answered by repo context, user choice, or local evidence before saving;
- `execution-deferred` - depends on reruns, generated outputs, or inspection during `econ-work`;
- `deferred follow-up scope` - real work, but outside this plan.

### Phase 7: Design verification, review, and escalation

At minimum specify:
- what proves input integrity;
- what proves transformation integrity;
- what proves realised sample, grouping, and denominator integrity;
- what proves object comparability before any benchmark claim;
- which audit outputs and report inputs must exist;
- whether `interpretation_brief.md` is required;
- whether `note_brief.md` is required;
- what text-figure consistency check is required if reporting is in scope;
- what proves the report build is portable;
- whether a compact review bundle is required; and
- which findings should trigger a stop-and-ask moment or a GPT Pro escalation question.

Use `econ-review` by default for empirical and hybrid work.

Plan reviewability gate:
- for substantive empirical or hybrid plans, the default next step is `econ-review surface:plan mode:headless plan:<saved-plan>`;
- the plan-review verdict is about whether later empirical review is possible, not whether realised outputs are correct;
- direct `econ-work` is acceptable only for narrow or trivial plans, or when the user explicitly wants to skip plan review;
- when plan review is skipped, state the skip reason in the plan and final route.

### Phase 8: Save a durable plan

Use `references/plan_template.md` for the saved or refreshed plan required by the direct invocation contract. If writing is blocked, state the blocker and exact no-save reason under `Review and handoff`.

Before saving or presenting the final plan, check whether any material question remains. If yes, use the interaction method above and wait; do not finalize the plan with that question buried in `Open questions`.

After drafting, strengthen only the weak sections needed to pass the template's minimum quality check.

## Final route

End with the mandatory visible output skeleton and stop after delivering the plan and next-command recommendation.

## Hard stops

- Do not execute the plan inside the planning turn.
- Do not leave the objective, reader, reporting class, or desired output implicit when they materially affect the work.
- Do not use `AGENTS.md` or `README.md` as the main home for long research-state content.
- Do not create or update GitHub issues unless the user requested or approved it.
- Do not hide missing evidence or ambiguities.
- Do not let a benchmark silently redefine the live object.
- Do not treat the execution note as the reader-facing note.
- Do not plan to draft the note directly from raw diagnostics, manifests, or execution logs.
- Prefer the smallest safe path that can still support an economist-facing final output.
