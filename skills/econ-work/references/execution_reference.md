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

```md
## Note brief
- Reader:
- Note type:
- Question the note answers:
- One-sentence answer:
- Why the note is worth reading:
- Definitions that must appear before the findings:
- Main sections in order:
- Candidate headline figure:
- Supporting figures or tables:
- What belongs only in the appendix or execution note:
- Terms that must not appear in the main text:
- Claims that need especially careful wording:
```

## Surprise memo template

```md
## Surprise memo
- Finding:
- Why it is surprising:
- Minimal validation already completed:
- Plausible explanations:
- Immediate follow-up checks:
- Does this look important enough for a deeper second opinion?
- Recommendation: continue in current workflow | ask user about GPT Pro escalation
```

## Output-consistency map minimum

Keep at least:
1. the canonical output ID or file backing each claim, table, or figure;
2. the note, memo, table, or figure label that uses it;
3. the key sample, benchmark, weighting, or specification note needed to keep the mapping honest; and
4. whether the cited object is current, inherited, or inspected-only when that status matters.

## Analysis surface simplification checklist

Use this after output inspection and before interpretation, review bundle preparation, or closeout.

```md
## Analysis surface simplification
- Refreshed outputs:
- Inherited outputs still intentionally used:
- Inspected-only outputs:
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

## Verification ladder

Run the levels that apply:
1. input integrity;
2. code and helper integrity;
3. research-code-quality floor;
4. transformation integrity;
5. computational-object integrity;
6. realised-sample audit;
7. grouping and denominator integrity;
8. object comparability;
9. output-specification integrity;
10. text-figure and report-build integrity;
11. interpretation discipline;
12. reader-facing note integrity;
13. reproducibility rerun status.

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
- `surprise_memo.md`.

## Issue checkpoint comment

Use this only when the work is issue-linked and the user asked for or approved an issue update.

```md
## Checkpoint
- Objective:
- Branch or worktree:
- Execution mode: structure-only|full empirical rerun|full computational run
- Code role: none|exploratory|analysis-pipeline|shared-collaborator|replication-facing|library-tool
- Plan labels touched:
- Outputs refreshed:
- Outputs inspected only:
- Empirical finding or diagnostic update:
- What remains unresolved:
- Recommended issue action: keep open|close|split follow-up|needs user decision
```

Do not include raw restricted data, confidential evidence, or long logs in issue comments. Link to plans, outputs, bundles, or commits instead.

## Evidence pulse

Use this inside closeouts for substantial empirical or hybrid work.

```md
## Evidence pulse
- What changed:
- What became more trustworthy:
- What became weaker or remains unresolved:
- Outputs refreshed:
- Outputs inherited or inspected only:
- Labels/issues/branches the next session should use:
- Suggested next planning question:
- Durable update target: none|closeout-only|econ-compound candidate|issue comment|project backbone|README dictionary|follow-up plan
- Proposed project-backbone update, if any:
- Project-backbone update approval status: not needed|drafted only|approved and applied
```

## Closeout format

Use this as the completion gate for non-trivial `econ-work` runs. Do not declare the run complete until the applicable items are stated or explicitly marked not applicable.

End with:
1. objective completed;
2. domain mode;
3. execution mode;
4. code role when code is in scope;
5. furthest stage reached;
6. outputs refreshed versus inspected-only versus scaffolded;
7. analysis-surface simplification status;
8. files and artefacts changed;
9. key findings taken into the interpretation brief;
10. note brief status when reporting is in scope;
11. surprise memo and GPT Pro escalation status, if any;
12. choice-register updates;
13. verification performed;
14. research-code-quality checks when code is in scope;
15. review-bundle status;
16. data or computational blockers, if any;
17. evidence pulse;
18. issue checkpoint status, if issue-linked;
19. remaining risks or open questions;
20. reusable lesson checkpoint; and
21. recommended next command.

Reusable lesson checkpoint format:
- `Reusable lesson checkpoint: none` when the run did not reveal a reusable lesson. Keep this to one compact line.
- `Reusable lesson checkpoint: closeout-only` when the lesson is task-local and should stay in the closeout.
- `Reusable lesson checkpoint: econ-compound candidate` when the run revealed a reusable economics research lesson. Include one sentence plus the evidence path a later `econ-compound` run should read.

Do not write durable learning notes from the closeout unless the user explicitly asked for learning capture or the larger autonomous run explicitly included compounding.
