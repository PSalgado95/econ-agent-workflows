# Plan template

Use this template when saving or substantially refreshing a plan.

```md
---
status: active
created: YYYY-MM-DD
updated: YYYY-MM-DD
domain_mode: empirical|hybrid|software-handoff
round_type: current-evidence-cleanup|current-evidence-clarification|new-empirical-work
reporting_class: coding-only|analysis-only|analysis-plus-note-report|analysis-plus-note-report-plus-figures
note_type: none|results-note|measurement-note|benchmark-note|decision-memo|other
---

# <Plan title>

## Task restatement

## Objective

## Project backbone
- Backbone used:
- If none, whether a compact `PROJECT_BRIEF.md` is needed:

## Issue coordination
- Linked issue:
- Issue role: none|diagnosis|implementation-lane|robustness-lane|note-or-paper-prep|review-follow-up
- Current issue action: none|read-only-context|draft-issue|create-issue|update-issue|close-or-split-recommended

## Reader contract

## Reporting class

## Reader-facing note contract
- Note type:
- Question the note must answer:
- What the note is for:
- What the reader should know by the end:
- Figures required:
- What must stay out of the main text:

## Decision frame
- Round type:
- Why this round type fits:
- Secondary lanes, if any:
- Desired final output:
- Final human reader:

## Central bottleneck

## Scope boundaries

## Assumptions
- Stated by user or project backbone:
- Inferred but not user-confirmed:
- Explicitly out of scope:

## Stable labels
- Key decisions:
- Key outputs:
- Work units:
- Review findings namespace: `F1`, `F2`, ... reserved for `econ-review`

## Origin trace
| Label | Object or decision | Evidence path | Expected output | Review surface |
| --- | --- | --- | --- | --- |
|  |  |  |  |  |

## Live evidence and source-of-truth surfaces

## Research question, estimand, or descriptive object

## Definition registry

## Benchmark and comparison block

## Audit outputs and report inputs
- Audit outputs:
- Report inputs:

## Ordered execution stages

### Stage 1: Code and run checks
- Goal:
- Mode:
- Main files / artefacts:
- Inputs required:
- Outputs expected:
- Checks and audits:
- Stop conditions:
- User question trigger:
- Review route:

### Stage 2: Output inspection
- Goal:
- Mode:
- Main files / artefacts:
- Inputs required:
- Outputs expected:
- Checks and audits:
- Stop conditions:
- User question trigger:
- Review route:

### Stage 3: Economic interpretation and headline triage
- Goal:
- Mode:
- Main files / artefacts:
- Inputs required:
- Outputs expected:
- Checks and audits:
- Stop conditions:
- User question trigger:
- Review route:

### Stage 4: Note writing and figures
- Goal:
- Mode:
- If `coding-only` or `analysis-only`, explicit skip reason:
- Main files / artefacts:
- Inputs required:
- Outputs expected:
- Checks and audits:
- Stop conditions:
- User question trigger:
- Review route:

## Choice register

## Open questions for the user
- Blocking questions already asked before finalising:
- Resolved before planning:
- Execution-deferred unknowns:
- Deferred follow-up scope:
- Other non-blocking questions:

## Risks and dependencies

## Review route and plan-reviewability gate
- Default next step: `econ-review surface:plan mode:headless plan:<saved-plan>` for substantive empirical/hybrid plans
- Skip reason, if direct `econ-work` is recommended:
```

## Minimum quality check before saving

Confirm that the saved plan makes these explicit:
- short task restatement;
- project backbone used or reason none was used;
- issue coordination when issue-linked;
- reader contract;
- `domain_mode`, `round_type`, and `reporting_class`;
- note contract when reporting is in scope;
- sparse labels for nontrivial decisions, outputs, and work units;
- `F1`, `F2`, ... reserved for review findings;
- origin trace for nontrivial decisions/outputs;
- central bottleneck;
- live object versus benchmark block;
- audit outputs versus report inputs;
- stage order;
- stop conditions;
- review route;
- material plan-shaping questions asked with the blocking question tool or explicitly resolved;
- plan-reviewability gate or explicit skip reason;
- all file, folder, script, output, and evidence references use repo-relative paths;
- user-named files, issues, outputs, datasets, registers, or documents were inspected or explicitly marked unavailable;
- decisions include rationale, not only tasks.
