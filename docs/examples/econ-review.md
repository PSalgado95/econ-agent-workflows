# `econ-review` Examples

These examples are generic prompts for testing the review-panel workflow after installing the skills and custom reviewer agents.

## Plan Review

```text
$econ-review surface:plan mode:headless plan:docs/plans/2026-05-07-baseline-rerun-econ-plan.md
```

Expected behavior:

- selects a compact panel, normally provenance and specification, plus any role needed by the plan surface;
- reports on reviewability, not whether realised empirical outputs are correct;
- labels missing source-of-truth files or unclear audit surfaces as diagnostic gaps.

## Results Review

```text
$econ-review surface:results tier:standard outputs/review_bundle
```

Expected behavior:

- selects the core results panel: provenance, specification, transformation/sample, and output consistency;
- adds estimation, design, dynamics, reproducibility, or hybrid-implementation reviewers when the target implies those risks;
- merges JSON reviewer payloads into findings with stable `F1`, `F2`, ... IDs.

## Note-Facing Review

```text
$econ-review surface:note tier:promotion notes/results_note.tex
```

Expected behavior:

- reviews the note against its interpretation brief, note brief, cited outputs, checks, and captions;
- includes claim discipline and the parent reader-facing note gate;
- treats missing evidence or unclear benchmark boundaries as promotion risks.

## Bundle Review

```text
$econ-review surface:bundle tier:promotion review_bundle/
```

Expected behavior:

- checks whether the bundle is complete, fresh, and legible enough for external handoff;
- includes bundle and reproducibility reviewers when handoff quality matters;
- does not treat GitHub issue text as analytical evidence without checking plans, outputs, checks, and bundle contents.

## Degraded Review

If reviewer agents are not configured, `econ-review` should clearly say the panel did not fully run.

- `tier:quick`: may continue with a labelled degraded review.
- `tier:standard`: may continue with an explicit warning and list of missing roles.
- `tier:promotion`: should stop or ask whether a degraded review is acceptable. In headless mode, it should return a degraded verdict rather than certifying promotion readiness.
