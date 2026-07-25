# Execution reference

Read this file only when you need a template or checklist during execution.

## Interpretation brief template

```md
## Interpretation brief
- Main finding:
- Why it matters economically:
- Best figure or table for the point:
- Supporting observed facts:
- Diagnostic explanation, if needed:
- Important limitations:
- Follow-up checks still worth doing now:
- What belongs in the main text versus appendix:
```

## Note brief template

The note brief is a delta on `interpretation_brief.md`: start from that brief and record only what changes now that a specific reader is in view. Do not restate the main finding, supporting facts, or limitations already in the interpretation brief.

```md
## Note brief (delta on the interpretation brief)
- Reader, and what they must take away:
- Note type (free text):
- Definitions that must appear before the findings:
- Main sections in order, and the headline figure:
- What drops to the appendix or execution note:
- Terms that must not appear in the main text:
- Claims that need especially careful wording:
```

## Surprise memo

The surprise memo is a local human-facing output: render it as HTML via the `econ-html-memo` skill and design system when installed, or as plain standalone HTML under the same content discipline when it is not. Use the content checklist below in either case. It records the result, evidence boundary, and next research decision without initiating another workflow.

```md
## Surprise memo
- Finding:
- Why it is surprising:
- Minimal validation already completed:
- Plausible explanations:
- Immediate follow-up checks:
- Which research decision or local check is now required?
- Recommendation: continue in current workflow | pause for researcher decision
```

## Output-consistency map minimum

Keep at least:
1. the canonical output ID or file backing each claim, table, or figure;
2. the note, memo, table, or figure label that uses it;
3. the key sample, benchmark, weighting, or specification note needed to keep the mapping honest; and
4. whether the cited object is current, inherited, or inspected-only when that status matters.

## Output provenance status vocabulary

Every output or artefact carries two orthogonal tags. These are the single vocabulary used wherever output status is recorded: `econ-work` Stage 2 and the closeout, the review bundle, and the reviewer evidence manifest passed to `econ-review`.

Provenance status (exactly one):
- `refreshed`: regenerated in this run;
- `inherited`: produced earlier and still intentionally used as current;
- `inspected-only`: read or interpreted in this run but not regenerated;
- `scaffolded`: created as structure, never executed;
- `stale`: likely superseded, no longer current, or inconsistent with the active object;
- `unknown`: reviewer-side fallback when the status cannot be read from the evidence. A producer should never leave its own output `unknown`.

Role tag (exactly one, orthogonal to status):
- `support-only`: useful diagnostic or backend evidence, not a reader-facing report input;
- `report-input`: candidate table, figure, note excerpt, or bundle surface for reader-facing use.

## Choice register row template

Log each Class A and Class B choice (see `econ-work` "Choice classes") as one row in `choice_register.md`:

```md
- [label] | class: A|B|C | choice: | alternatives worth stress-testing: | status: provisional|settled
```

Keep Class A rows `provisional` until the researcher confirms; record credible alternatives for Class B rows so they can be stress-tested later.

## Analysis surface simplification checklist

Use this after output inspection and before interpretation, review bundle preparation, or closeout. Tags follow the provenance vocabulary above.

```md
## Analysis surface simplification
- Refreshed outputs:
- Inherited outputs still intentionally used:
- Inspected-only outputs:
- Scaffolded outputs (created as structure, never executed):
- Stale or superseded outputs:
- Support-only diagnostics:
- Report inputs:
- Duplicate scripts or execution paths:
- Redundant diagnostics:
- Unclear figure/table names:
- Benchmark/comparison objects that must stay separate:
- Destructive cleanup requested or approved: yes|no
- Cleanup follow-up recommended:
```

Never delete, overwrite, or hide stale research evidence without explicit approval.

## Reader-facing note gate

Run this local gate after the text-figure consistency test and before treating a
note or memo as complete:

1. the opening states the economic question and defended result rather than the
   agent process;
2. every quantitative claim resolves through the output-consistency map to a
   named, non-stale report input;
3. observed facts, diagnostic explanations, limitations, and open questions
   remain distinguishable;
4. causal, mechanism, welfare, and policy language stays within the verified
   design and evidence;
5. figure and table titles, captions, units, denominators, samples, and
   directions agree with the text;
6. inherited or inspected-only material is labelled, portable paths resolve,
   and the requested reader-facing format opens or builds successfully.

If any item fails, keep `note_status` blocked and name the failing item and
evidence path in the closeout.

## Verification ladder

Run the rungs that apply; each gives an example check.
1. input integrity — the named inputs exist and match the expected signature or vintage, not just the folder.
2. code and helper integrity — a helper that defines bins, keys, denominators, or timing returns what the object needs on a small known case.
3. research-code-quality floor — entrypoints visible, object-defining parameters named, no stale debug or test fragments in tracked code.
4. transformation integrity — row and unit counts and key uniqueness hold through each join and filter; drops are reason-coded.
5. computational-object integrity — dimensions, convergence, residuals, feasibility, or conservation hold for the computational object.
6. realised-sample audit — the stage-by-stage sample flow reconciles to the final N.
7. grouping and denominator integrity — the denominator and aggregation level match the claim; weights applied at the intended stage.
8. object comparability — same sample filter, weights, and denominator on both sides of any benchmark claim, shown in one comparison table.
9. output-specification integrity — each promoted table or figure matches its specification and was regenerated by the stated entrypoint.
10. text-figure and report-build integrity — every number and direction claimed in the text matches the cited table or figure cell; the report builds from portable paths.
11. interpretation discipline — causal, mechanism, or policy language does not outrun the verified object.
12. reader-facing note integrity — the note passes the local **Reader-facing note gate** above.
13. reproducibility rerun status — the provenance status of each promoted output is stated.

## Minimal artefacts glossary

Create the minimal version of any of these when it is absent rather than working without it:
- **Model-spec ledger** — a stable list of the realised specification(s): estimator, sample, fixed effects, weights, inference, and the output each maps to.
- **Output specification / manifest** — what each canonical output family should contain and where it is written, so a changed output can be checked against intent.
- **Workflow note** — the running execution note (what was inspected, changed, run, regenerated, and what remains), kept separate from the reader-facing note.

## Research code quality checklist

Use when code is written, changed, or reviewed as part of the research object.

```md
## Research code quality
- Code role: none|exploratory|analysis-pipeline|shared-collaborator|replication-facing|library-tool
- Entry point or rerun path:
- Object-defining parameters named:
- Assertions or equivalent invariant checks added/refreshed:
- Named tests added/refreshed, if warranted by code role:
- Temporary debug/test fragments removed from tracked research code:
- Analytical logic separated from formatting/report rendering where practical:
- Notebook-only logic promoted or intentionally left as exploration:
- Performance scope: off|explicitly-requested|profiled-bottleneck|library-tool
```

For `task_family: model_computation`, add computational checks such as dimensions, convergence, residuals, feasibility, mass conservation, market clearing, deterministic simulation checks, small transparent benchmarks, or comparison to a known baseline or analytical limit.

## Review bundle minimum

A compact economist review bundle should normally contain:
- `review_context.md`;
- `review_manifest.md` or equivalent;
- `choice_register.md`;
- `key_outputs/`;
- `checks/`;
- `build_info/`.

Also include when relevant:
- a model-spec ledger or equivalent stable specification surface;
- an output-consistency map;
- `interpretation_brief.md`;
- `note_brief.md`;
- the defended note, memo, or excerpt and relevant caption material;
- `surprise_memo.html`.

## Issue checkpoint comment

Use this only when the work is issue-linked and the user asked for or approved an issue update.

```md
## Checkpoint
- Objective:
- Branch or worktree:
- What was run, and what was not run:
- Code role: none|exploratory|analysis-pipeline|shared-collaborator|replication-facing|library-tool
- Plan labels touched:
- Outputs refreshed:
- Outputs inspected only:
- Empirical finding or diagnostic update:
- What remains unresolved:
- Recommended issue action: keep open|close|split follow-up|needs user decision
```

Do not include raw restricted data, confidential evidence, or long logs in issue comments. Link to plans, outputs, bundles, or commits instead.

## Closeout

Use this as the completion gate for `econ-work` runs. The run is complete only when every applicable item is stated (or explicitly marked not applicable); a script run, a generated file, or one passing check is not completion.

1. objective and outcome;
2. what was inspected, changed, run, and regenerated, plus code role when code changed;
3. furthest stage reached;
4. outputs by provenance status (`refreshed`/`inherited`/`inspected-only`/`scaffolded`/`stale`) and role tag (`support-only`/`report-input`), named by file;
5. verification performed and what it proved;
6. interpretation and note status: interpretation brief, note brief, note or figures, and surprise memo with any unresolved research decision;
7. review route and bundle status, plus the issue checkpoint when the work is issue-linked;
8. blockers, risks, and open questions, plus choice-register updates and any durable residual sink (see below);
9. reusable lesson checkpoint (one line, format below);
10. recommended next command.

Durable residual sink: deferred or advisory findings that affect trust must land on a durable surface before delivery — the review bundle's residual section, a GitHub issue (with approval), or a dated `docs/residual-findings/<slug>.md` — with finding IDs preserved. Never close out with trust-affecting residuals recorded only in chat.

For trivial one-off work, use a compact closeout, but still state what was checked, changed, run, or regenerated, output status, remaining risk, and next step.

Reusable lesson checkpoint format:
- `Reusable lesson checkpoint: none` when the run did not reveal a reusable lesson. Keep this to one compact line.
- `Reusable lesson checkpoint: closeout-only` when the lesson is task-local and should stay in the closeout.
- `Reusable lesson checkpoint: econ-compound candidate` when the run revealed a reusable economics research lesson. Include one sentence plus the evidence path a later `econ-compound` run should read.

Do not write durable learning notes from the closeout unless the user explicitly asked for learning capture or the larger autonomous run explicitly included compounding.

## Private return-to-caller envelope

Return this object inline when an authorised `econ-lfg` parent supplies `caller_contract: econ-lfg/v1`. Do not save it automatically.

```json
{
  "contract": "econ-work-for-caller/v1",
  "status": "complete|blocked|failed",
  "objective": "<bounded research task>",
  "saved_plan_path": "<repo-relative path>",
  "furthest_stage": "intake|code-and-run|output-audit|interpretation|reporting|closeout",
  "inspected_paths": [],
  "changed_paths": [],
  "commands_or_entrypoints_run": [],
  "verification": [
    {
      "check": "<command, assertion, or inspection>",
      "evidence_path": "<repo-relative path or null>",
      "proved": "<bounded claim>"
    }
  ],
  "outputs": [
    {
      "path": "<repo-relative path>",
      "provenance": "refreshed|inherited|inspected-only|scaffolded|stale",
      "role": "support-only|report-input"
    }
  ],
  "code_role": "none|exploratory|analysis-pipeline|shared-collaborator|replication-facing|library-tool",
  "interpretation_status": "complete|not-required|blocked",
  "interpretation_brief_path": null,
  "note_status": "complete|not-required|blocked",
  "note_brief_path": null,
  "note_paths": [],
  "figure_status": "complete|not-required|blocked",
  "figure_paths": [],
  "bundle_status": "complete|not-required|blocked",
  "review_bundle_path": null,
  "choice_register_path": null,
  "review_route": "<tier and surface, or none>",
  "residual_risks": [],
  "reusable_lesson_checkpoint": "none|closeout-only|econ-compound candidate",
  "researcher_decision": null,
  "access_blocker": null
}
```

Use empty arrays and `null` rather than omitting keys. Set `status: complete` only when every applicable closeout field is filled; otherwise return the blocking researcher decision, access condition, or failure.
