# Review reference

Read this file only when you need the detailed read order, reviewer matrix, taxonomy, cross-language validation trigger, issue-ready template, or headless envelope.

## Surface-specific read order

`plan`
- review whether the plan names the baseline object, estimand, source-of-truth files, reporting class, note contract when relevant, audit outputs versus report inputs, review route, interpretation boundary, and minimum diagnostic surfaces needed for later trust review.

`results`
- workflow note or plan -> output specification or manifest -> canonical outputs -> checks -> data-construction evidence contract fields when present -> model-spec ledger when relevant -> econometric evidence contract fields when present -> output-consistency map when note-facing claims are in scope -> output-automation status when present -> interpretation brief when interpretation is in scope -> note brief when reporting is in scope -> choice register.

`note`
- note -> note brief -> interpretation brief -> cited outputs -> relevant checks -> captions or figure notes when present -> output-consistency map when available -> key visible tables/figures for output-perception review when relevant.

`bundle`
- `review_context.md` -> `review_manifest.md` or equivalent -> `choice_register.md` -> `key_outputs/` -> `checks/` -> `build_info/` -> data-construction evidence contract fields when present -> model-spec ledger when relevant -> econometric evidence contract fields when present -> output-consistency map when note-facing claims are in scope -> output-automation status -> `interpretation_brief.md` -> `note_brief.md` and defended note excerpt when note-facing -> cross-language validation manifest only when explicitly requested or directly targeted.

`diff`
- diff scope -> current plan -> workflow note -> affected outputs, checks, and specification objects -> changed estimator/inference/sample/weight/timing/output-generation settings -> affected output-consistency map or note artefacts.

`mixed`
- plan -> diff -> outputs or bundle -> data-construction evidence contract fields when present -> model-spec ledger when relevant -> econometric evidence contract fields when present -> output-consistency map when note-facing claims are in scope -> output-automation status -> interpretation brief -> note brief when reporting is in scope -> note when present.

## Input tokens owned by the parent

Parse these tokens when present:

- `mode:report-only|autofix|headless`;
- `tier:quick|standard|promotion`;
- `surface:plan|results|bundle|note|diff|mixed`;
- `interpretation:yes|no`;
- `issues:yes|no`;
- `crosslang:no|yes|plan|audit`;
- `plan:<path>`;
- `base:<ref>`.

`crosslang:` defaults to `no`. Do not infer cross-language validation merely because the repository contains multiple languages. Natural-language requests such as "prepare a Stata/R/Python validation", "cross-language check", "R = Stata", or "replicate in another language" count as `crosslang:yes` unless contradicted by `crosslang:no`.

## Reviewer-role matrix

Always include:

- `provenance-auditor`;
- `specification-auditor`.

For any surface other than `plan`, default the economist core to:

- `transformation-and-sample-auditor`;
- `output-consistency-auditor`.

Add when relevant:

- `estimation-practice-auditor` for realised estimates, model-based descriptives, or inferential work that should already specify estimator, weights, fixed effects, controls, omitted categories, lags, horizons, or model metadata;
- `inference-auditor` for p-values, confidence intervals, significance stars, clustered designs, small/uneven clusters, IV/RD/RCT, event studies, local projections, dynamic outputs, multiple outcomes/treatments/horizons, or promotion-grade causal work;
- `claim-discipline-auditor` whenever interpretation is in scope;
- `output-perception-auditor` for table/figure-heavy `surface:results`, note-facing outputs, Blindspot-style review, `surface:mixed`, or promotion-grade interpretation where visible anomalies or missed empirical opportunities matter;
- `dynamics-auditor` for macro, time-series, local projections, dynamic panels, impulse responses, event-time plots, cumulative responses, distributed lags, or other horizon estimators;
- `design-auditor` for IV, DiD, event studies, RCTs, RD, treatment designs, synthetic control, selection-on-observables, or other causal or quasi-experimental work;
- `robustness-auditor` when promotion, baseline placement, sensitivity evidence, multiplicity, heterogeneity, mechanism interpretation, or specification-search discipline is at stake;
- `reproducibility-auditor` for review bundles, replication packages, restricted-data work, external handoff, rerun status, or output automation where reproducibility matters;
- `software-equivalence-auditor` when multiple software or estimator paths are being compared or when an existing cross-language validation manifest claims equivalence;
- `cross-language-validation-auditor` only for explicit `crosslang:yes|plan|audit`, a target cross-language validation manifest, or a note/bundle that explicitly claims cross-language equivalence;
- `hybrid-implementation-auditor` for custom software interfaces, compiled code, services, manifests, hidden defaults, or non-standard execution machinery that can affect analytical trust;
- `bundle-auditor` when the target is the bundle itself or external handoff quality is central.

Typical panel size:

- `surface:plan` -> 2 to 4 roles;
- `surface:results` or `surface:diff` -> 4 to 7 roles;
- `surface:note`, `surface:mixed`, or `surface:bundle` with interpretation or external handoff live -> 6 to 9 roles;
- `crosslang:plan` adds a separate handoff section; it need not add the full equivalence panel unless existing validation evidence is being audited.

Do not duplicate roles that are asking the same question. The intended split is:

- `specification-auditor`: what is the object/estimand?
- `design-auditor`: why does the comparison identify the object?
- `estimation-practice-auditor`: does the code implement the model object?
- `inference-auditor`: does uncertainty match the design/dependence/claim?
- `dynamics-auditor`: are timing and horizon objects coherent?
- `robustness-auditor`: is the baseline/robustness hierarchy honest?
- `output-perception-auditor`: what visible output feature or absence is being missed?

## Custom reviewer agent mapping

Use these project-scoped Codex custom agents when available:

| Reviewer role | Custom agent name |
| --- | --- |
| `provenance-auditor` | `econ_provenance_reviewer` |
| `specification-auditor` | `econ_specification_reviewer` |
| `transformation-and-sample-auditor` | `econ_transformation_sample_reviewer` |
| `output-consistency-auditor` | `econ_output_consistency_reviewer` |
| `claim-discipline-auditor` | `econ_claim_discipline_reviewer` |
| `output-perception-auditor` | `econ_output_perception_reviewer` |
| `estimation-practice-auditor` | `econ_estimation_practice_reviewer` |
| `inference-auditor` | `econ_inference_reviewer` |
| `design-auditor` | `econ_design_reviewer` |
| `dynamics-auditor` | `econ_dynamics_reviewer` |
| `robustness-auditor` | `econ_robustness_reviewer` |
| `reproducibility-auditor` | `econ_reproducibility_reviewer` |
| `software-equivalence-auditor` | `econ_software_equivalence_reviewer` |
| `cross-language-validation-auditor` | `econ_cross_language_validation_reviewer` |
| `hybrid-implementation-auditor` | `econ_hybrid_implementation_reviewer` |
| `bundle-auditor` | `econ_bundle_reviewer` |

Each reviewer agent must run read-only, use only its assigned lens, and return JSON matching the shared protocol. Prefer the protocol excerpt passed by the parent `econ-review` skill. If no excerpt is passed, use `~/.codex/references/econ-agent-workflows/reviewer-protocol.md` when available. Use `references/reviewer-protocol.md` only when the parent confirms the current checkout is this package repository. If the protocol is unavailable, treat the panel as degraded before dispatch.

## Econometric evidence manifest checklist

When relevant, the parent should include these fields or list them as missing diagnostic surfaces:

```yaml
econometric_evidence:
  estimand:
    outcome:
    treatment_or_exposure:
    comparison_group:
    unit:
    timing:
    target_population:
    effect_scale:
    aggregation:
    parameter_label:
  identification:
    design_class:
    source_of_variation:
    identifying_assumptions:
    comparison_group:
    primary_threats:
  sample:
    unit_of_observation:
    sample_flow_path:
    merge_diagnostics_path:
    missingness_path:
    support_overlap_path:
    horizon_sample_path:
  estimator:
    family:
    variant:
    code_path:
    model_spec_ledger_path:
    controls:
    omitted_categories:
  fixed_effects:
    absorbed_dimensions:
    singleton_handling:
    collinearity_notes:
  weights:
    weight_type:
    target_population:
    normalisation:
    application_stage:
    diagnostics_path:
  inference:
    se_type:
    cluster_levels:
    cluster_counts:
    finite_sample_correction:
    special_method:
    multiplicity_or_band_method:
  dynamics:
    horizon_definition:
    reference_period:
    cumulative_or_level:
    horizon_ledger_path:
  robustness_hierarchy:
    baseline_outputs:
    companion_outputs:
    diagnostic_outputs:
    placebo_outputs:
    sensitivity_outputs:
    exploratory_outputs:
  output_automation:
    table_generation_status:
    figure_generation_status:
    in_text_stat_source_map:
    manual_edits:
  cross_language_validation:
    requested: no|yes|plan|audit
    manifest_path:
    primary_software:
    comparison_software:
```

The parent should not hallucinate field values. Unknown fields should remain missing or `unknown` and be handled as possible diagnostic gaps.

## Data-construction evidence manifest checklist

For cleaning-heavy or sample-building work, the parent should include these fields or list them as missing diagnostic surfaces:

```yaml
data_construction_evidence:
  source_lineage:
    raw_inputs:
    derived_inputs:
    canonical_input:
    data_vintage:
    input_manifest_or_hash:
  unit_and_keys:
    unit_of_observation:
    primary_keys:
    time_keys:
    duplicate_diagnostics_path:
    key_repair_rules:
  joins_and_merges:
    merge_keys:
    expected_cardinality:
    unmatched_counts_path:
    duplicate_after_merge_path:
    reconciliation_rules:
  filters_and_drops:
    inclusion_rules:
    exclusion_rules:
    reason_coded_drops_path:
    sample_flow_path:
  missingness:
    variables_checked:
    missingness_diagnostics_path:
    imputation_or_drop_rules:
  support_and_overlap:
    support_restrictions:
    overlap_diagnostics_path:
    group_or_horizon_support_path:
  denominators_and_weights:
    denominator_definition:
    aggregation_level:
    weight_type:
    weight_diagnostics_path:
  timing_alignment:
    date_rules:
    lag_lead_rules:
    event_window_rules:
    revision_or_vintage_rules:
  intermediate_outputs:
    canonical_intermediate_paths:
    row_count_manifest:
    schema_manifest:
    rerun_status:
  manual_steps:
    manual_edits:
    non_reproducible_steps:
```

Cleaning-heavy reviews should not be escalated into econometric review unless the target also contains realised estimates, causal/inferential claims, dynamic objects, or promotion-grade result interpretation.

## Cross-language validation behaviour

Default: `crosslang:no`.

`crosslang:plan`
- Do not audit nonexistent validation evidence.
- Prepare a separate cross-language validation handoff using `cross_language_validation_workflow.md`.
- The final synthesis should say that validation has not yet been run.

`crosslang:yes`
- If a validation manifest or comparison outputs are present, treat as `crosslang:audit`.
- If no usable validation evidence is present, treat as `crosslang:plan`.

`crosslang:audit`
- Select `cross-language-validation-auditor`.
- Usually also select `software-equivalence-auditor`.
- Require a manifest or comparison outputs; if absent, return a diagnostic gap and a validation handoff.

Cross-language validation should not mutate author code. Independent scripts, if later created by a separate workflow, should live in a validation/replication area and should write a manifest that `econ-review` can audit.

## Subagent fallback matrix

Use fallback only when subagent tools or selected reviewer agents are unavailable.

| Tier | Fallback behaviour |
| --- | --- |
| `quick` | May run a degraded single-thread review if the final output clearly labels that the panel did not run. |
| `standard` | May run a degraded review with an explicit warning and a list of missing reviewer roles. |
| `promotion` | Must stop or ask for explicit user acceptance before degraded review. In `mode:headless`, stop with a degraded verdict rather than certifying promotion readiness. |

Malformed reviewer payloads should be discarded or quarantined. Evidence-free findings should be suppressed unless the issue is a bundle-metadata gap visible in the bundle itself. Missing reviewer roles should appear in the artefact summary.

## Review tiers

`quick`
- narrow hygiene, plan reviewability, bundle metadata, or documentation pass;
- should still surface missing evidence if the target unexpectedly makes empirical claims.

`standard`
- default empirical review tier;
- checks whether the object can be trusted for the current internal purpose.

`promotion`
- coauthor, supervisor, paper, appendix, replication, or public-facing readiness;
- missing diagnostics, inherited outputs, unclear rerun status, note-claim drift, or portability overclaims should be treated more strictly.

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
- `inference`;
- `output-consistency`;
- `claim-discipline`;
- `output-perception`;
- `design`;
- `dynamics`;
- `robustness`;
- `software-equivalence`;
- `cross-language-validation`;
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

## Cross-language validation handoff template

Use only when the user explicitly requested cross-language validation and no completed validation manifest is available.

```md
## Cross-language validation handoff

Status: planned, not yet run
Primary software:
Comparison software:
Validation target:
- Output/table/figure ID:
- Baseline specification ID:
- Estimand:
- Source data/input version:

### Object parity checks required
- Sample N, unit count, time-period count, and cluster count
- Variable construction and missing-value handling
- Weights and normalisation
- Fixed effects, singleton handling, omitted/reference categories
- Clustering and finite-sample/degrees-of-freedom conventions
- Output labels and coefficient mapping

### Numeric comparison required
- Coefficients
- Standard errors
- Confidence intervals or p-values
- Degrees of freedom and cluster counts
- Known acceptable software-convention differences

### Independence boundary
- Validation scripts must not modify author code.
- Validation scripts should read approved inputs and write separate comparison outputs.
- Any discrepancy must be classified as object mismatch, software-convention difference, tolerance-level numerical difference, or unresolved.
```

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
Tier: <tier>
Cross-language validation: no|planned|audited|requested-but-missing
Reviewers: <reviewer-list>
Panel status: full|degraded|not-run
Artifact: <artifact-path>
Verdict: <clean|issues-found|degraded>

Blocking before trust:
[F1][P1][promotion-blocking][transformation-and-sample][manual] <title> -- <evidence paths>

Worth checking before promotion:
[F2][P2][robustness-relevant][inference][gated] <title> -- <evidence paths>

Diagnostic gaps:
- <gap>

Reader-facing note register:
[F3][P2][promotion-blocking][note-register][manual] <title> -- <evidence paths>

Cross-language validation handoff:
- <only when explicitly requested and not yet run>

Documentation / cleanup:
[F4][P3][documentation-only][bundle][safe automatic] <title> -- <evidence paths>

Open questions:
- <question>

Review complete
```

Omit empty sections and end with `Review complete`.
