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

## Cleaning / Data Construction Review

```text
$econ-review surface:diff tier:standard cleaning/sample_build_changes
```

Expected behavior:

- treats data construction as a first-class empirical trust surface;
- selects provenance, specification, transformation/sample, and output consistency;
- checks lineage, keys, joins, filters, missingness, support, denominators, weights, timing alignment, and rerun status;
- does not add inference or design reviewers unless the target also contains estimates, causal claims, dynamic objects, or promoted interpretation.

## Inference-Heavy Results Review

```text
$econ-review surface:results tier:promotion interpretation:yes outputs/headline_table_bundle
```

Expected behavior:

- includes the core data reviewers;
- adds estimation-practice and inference reviewers when coefficients, standard errors, p-values, confidence intervals, clustering, or significance language carry the claim;
- adds design, dynamics, or robustness reviewers only when the method or promotion decision calls for them.

## Note-Facing Review

```text
$econ-review surface:note tier:promotion notes/results_note.tex
```

Expected behavior:

- reviews the note against its interpretation brief, note brief, cited outputs, checks, and captions;
- includes claim discipline, output perception when tables/figures drive interpretation, and the parent reader-facing note gate;
- treats missing evidence or unclear benchmark boundaries as promotion risks.

## Cross-Language Validation Planning

```text
$econ-review surface:bundle tier:promotion crosslang:plan review_bundle/
```

Expected behavior:

- prepares a cross-language validation handoff;
- does not claim validation has been run;
- does not spawn a full equivalence audit over nonexistent scripts.

## Cross-Language Validation Audit

```text
$econ-review surface:bundle tier:promotion crosslang:audit validation/cross_language_manifest.md
```

Expected behavior:

- selects cross-language validation and software-equivalence reviewers;
- checks object parity before numeric parity;
- blocks equivalence claims when N, cluster counts, missing-value rules, weights, fixed effects, or omitted categories differ without explanation.

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
