# Review reference

Read this file only when you need the detailed read order, reviewer matrix, taxonomy, or headless envelope.

## Surface-specific read order

`plan`
- review whether the plan names the baseline object, source-of-truth files, reporting class, note contract when relevant, audit outputs versus report inputs, review route, and interpretation boundary.

`results`
- workflow note or plan -> output specification or manifest -> canonical outputs -> checks -> model-spec ledger when relevant -> output-consistency map when note-facing claims are in scope -> interpretation brief when interpretation is in scope -> note brief when reporting is in scope -> choice register.

`note`
- note -> note brief -> interpretation brief -> cited outputs -> relevant checks -> captions or figure notes when present -> output-consistency map when available.

`bundle`
- `review_context.md` -> `review_manifest.md` or equivalent -> `choice_register.md` -> `key_outputs/` -> `checks/` -> `build_info/` -> model-spec ledger when relevant -> output-consistency map when note-facing claims are in scope -> `interpretation_brief.md` -> `note_brief.md` and defended note excerpt when note-facing.

`diff`
- diff scope -> current plan -> workflow note -> affected outputs, checks, and specification objects -> affected output-consistency map or note artefacts.

`mixed`
- plan -> diff -> outputs or bundle -> model-spec ledger when relevant -> output-consistency map when note-facing claims are in scope -> interpretation brief -> note brief when reporting is in scope -> note when present.

## Reviewer-role matrix

Always include:
- `provenance-auditor`;
- `specification-auditor`.

For any surface other than `plan`, default the economist core to:
- `transformation-and-sample-auditor`;
- `output-consistency-auditor`.

Add when relevant:
- `estimation-practice-auditor` for realised estimates, model-based descriptives, or inferential work that should already specify estimator, weights, fixed effects, clustering, lags, horizons, or inference rules;
- `claim-discipline-auditor` whenever interpretation is in scope;
- `dynamics-auditor` for macro, time-series, local projections, dynamic panels, impulse responses, or other horizon estimators;
- `design-auditor` for IV, DiD, event studies, treatment designs, or other causal or quasi-experimental work;
- `robustness-auditor` when promotion, baseline placement, or sensitivity evidence is disputed;
- `reproducibility-auditor` for review bundles, replication packages, restricted-data work, or external handoff where rerun status matters;
- `software-equivalence-auditor` when multiple software or estimator paths are being compared;
- `hybrid-implementation-auditor` for custom software interfaces, compiled code, services, or non-standard execution machinery that can affect analytical trust;
- `bundle-auditor` when the target is the bundle itself.

Typical panel size:
- `surface:plan` -> 3 to 4 roles;
- `surface:results` or `surface:diff` -> 4 to 6 roles;
- `surface:note`, `surface:mixed`, or `surface:bundle` with interpretation or external handoff live -> 5 to 7 roles.

## Review tiers

`quick`
- narrow hygiene, plan reviewability, bundle metadata, or documentation pass;
- should still surface missing evidence if the target unexpectedly makes empirical claims.

`standard`
- default empirical review tier;
- checks whether the object can be trusted for the current internal purpose.

`promotion`
- coauthor, supervisor, paper, appendix, replication, or public-facing readiness;
- missing diagnostics, inherited outputs, unclear rerun status, or note-claim drift should be treated more strictly.

Escalation triggers:
- claim-bearing empirical change -> at least `standard`;
- coauthor, supervisor, paper, appendix, replication package, presentation, or public-facing promotion -> `promotion`;
- changed sample construction, estimand, specification, weighting, clustering, inference, treatment timing, inclusion/exclusion rules, or headline table/figure -> not `quick`;
- uncertain tier with possible promotion -> choose the stricter tier.

## Finding taxonomy

Severity:
- `P0`;
- `P1`;
- `P2`;
- `P3`.

Trust effect:
- `baseline-defining`;
- `promotion-blocking`;
- `robustness-relevant`;
- `documentation-only`.

Issue origin:
- `provenance`;
- `specification`;
- `transformation-and-sample`;
- `estimation-practice`;
- `output-consistency`;
- `claim-discipline`;
- `design`;
- `dynamics`;
- `robustness`;
- `software-equivalence`;
- `reproducibility`;
- `hybrid-implementation`;
- `bundle`;
- `note-register`.

Fix class:
- `safe automatic`;
- `gated`;
- `manual`;
- `advisory`.

Stable finding IDs:
- assign `F1`, `F2`, ... after merging and deduplication;
- preserve existing IDs when reviewing residual work from a prior pass;
- use IDs in closeouts, residual summaries, and issue drafts.

Reviewer JSON compatibility:
- reviewer subagents should return `fix_class` on every finding;
- reviewer subagents should return `affected_labels` as an array, using plan labels, output labels, issue numbers, branch/worktree names, or evidence IDs when visible;
- reviewer subagents should return `issue_followup_type` as `none`, `empirical problem`, `implementation fix`, `robustness extension`, or `note/paper follow-up`;
- keep `safe_autofix` as a compatibility boolean, normally true only when `fix_class` is `safe automatic`.

## Issue-ready follow-up template

Use only when the user asked to draft or file GitHub issues.

```md
## <Issue title>

Finding IDs: F<n>
Issue type: empirical problem|implementation fix|robustness extension|note/paper follow-up

### Objective

### Evidence surface
- Plan:
- Output/check/bundle/note:
- Review finding:

### Why this matters

### Out of scope

### Done when

### Links
```

Do not include raw restricted data, confidential evidence, or long logs. Link to plans, outputs, bundles, commits, or review artefacts instead.

## Headless output envelope

```text
Economist review complete (headless mode).

Scope: <target>
Surface: <surface>
Mode: headless
Reviewers: <reviewer-list>
Artifact: <artifact-path>
Verdict: <clean|issues-found|degraded>

Blocking before trust:
[F1][P1][promotion-blocking][transformation-and-sample][manual] <title> -- <evidence paths>

Worth checking before promotion:
[F2][P2][robustness-relevant][estimation-practice][gated] <title> -- <evidence paths>

Diagnostic gaps:
- <gap>

Reader-facing note register:
[F3][P2][promotion-blocking][note-register][manual] <title> -- <evidence paths>

Documentation / cleanup:
[F4][P3][documentation-only][bundle][safe automatic] <title> -- <evidence paths>

Open questions:
- <question>

Review complete
```

Omit empty sections and end with `Review complete`.
