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
task_family: source_collection|data_construction|model_computation|analysis|writing
code_role: none|exploratory|analysis-pipeline|shared-collaborator|replication-facing|library-tool
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

## Task family
- Primary family: source_collection|data_construction|model_computation|analysis|writing
- Secondary layers:
- Why this family fits:
- Sections included because relevant:
- Sections omitted because irrelevant:

## Code role
- Role: none|exploratory|analysis-pipeline|shared-collaborator|replication-facing|library-tool
- Why this role fits:
- Code paths or entrypoints expected:
- Maturity expected now:

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

## Live evidence and current authority surfaces

## Research question, estimand, or descriptive object

## Definition registry

## Benchmark and comparison block

## Audit outputs and report inputs
- Audit outputs:
- Report inputs:

## Implementation surface contract
- Include for `source_collection`, `data_construction`, `model_computation`, or complex `analysis`; omit when irrelevant.
- Base output directory:
- Output tree or file registry:
- Table/schema registry:
- Stable identifiers and join keys:
- Provenance fields required:
- Audit outputs:
- Report inputs:

## Research code quality contract
- Include when `code_role` is not `none`; omit when no code is in scope.
- Code role: none|exploratory|analysis-pipeline|shared-collaborator|replication-facing|library-tool
- Code paths or entrypoints expected:
- Always-on floor required:
- Object-defining invariants that should become assertions:
- Named tests expected now:
- Ad hoc debug/test code that must not remain in tracked research code:
- Notebook-to-script boundary:
- Research-computing checks, if `task_family: model_computation`:
- Performance scope: off|explicitly-requested|profiled-bottleneck|library-tool

## Source, provenance, and access plan
- Include when source discovery, external data collection, archives, APIs, registers, PDFs, or database exports are part of the task; omit when execution starts from fixed local inputs.
- Source families, data routes, or file/table routes:
- Query/source register or file/table registry fields:
- Access modes:
- Access blockers:
- Copyright, confidentiality, or redistribution constraints:
- Negative-evidence rule:
- Next action when a route is blocked:

## Evidence sorting and claim rules
- Include when interpretation depends on mixed source quality, constructed measures, or source-backed claims; omit for narrow execution-only plans.
- Task-specific source/evidence categories:
- Claim classes:
- What each category can support:
- What each category cannot support:
- Source/output-to-claim traceability rule:

## Pilot, expansion, and stopping logic
- Include for open-ended source discovery, large data construction, multi-wave measurement, or multi-agent reading; omit for narrow one-off tasks.
- Pilot or tranche purpose:
- Schema/access/calibration rule:
- Expansion triggers:
- Stop-and-ask triggers:
- Completion standard:
- Negative-evidence rule:

## Review packet contract
- Include only for large corpora, multi-source packages, external review bundles, or multi-agent reading.
- Batch or lens definitions:
- Required manifest IDs, source IDs, or output IDs:
- Coding fields to verify:
- Synthesis question:
- Overclaiming warnings:
- Expected output format:
- Rule for adding new evidence:

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

## Review route
- Default next step: `econ-work` on the saved plan
- Later `econ-review` surface expected after work: results|bundle|note|mixed|diff|none
- Artefacts `econ-work` should leave ready for later review:
- Optional pre-work plan review trigger, if any:
```

Optional insertion block. Add this only when relevant learning notes were actually consulted and changed the plan:

```md
## Prior research lessons consulted
- Lesson:
- Evidence path:
- How it shapes this plan:
- Reuse boundary or stale-note caution:
```

## Minimum quality check before saving

Confirm that the saved plan makes these explicit:
- short task restatement;
- project backbone used or reason none was used;
- issue coordination when issue-linked;
- reader contract;
- `domain_mode`, `round_type`, `reporting_class`, `task_family`, and `code_role`;
- note contract when reporting is in scope;
- task-family sections included or explicitly omitted;
- sparse labels for nontrivial decisions, outputs, and work units;
- `F1`, `F2`, ... reserved for review findings;
- origin trace for nontrivial decisions/outputs;
- prior research lessons consulted, with reuse boundary or stale-note caution, when such lessons shaped the plan;
- central bottleneck;
- live object versus benchmark block;
- audit outputs versus report inputs;
- stage order;
- stop conditions;
- review route;
- ordinary route is `econ-work` next unless an optional plan-review trigger is named;
- source/data/measurement plans specify required registries, identifiers, and audits;
- research-code plans specify `code_role` and the research code quality contract when code is in scope;
- ordinary analysis/writing plans omit irrelevant source/corpus machinery;
- material plan-shaping questions asked with the blocking question tool or explicitly resolved;
- all file, folder, script, output, and evidence references use repo-relative paths;
- user-named files, issues, outputs, datasets, registers, or documents were inspected or explicitly marked unavailable;
- decisions include rationale, not only tasks.
