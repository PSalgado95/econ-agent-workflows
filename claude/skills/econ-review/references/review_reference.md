<!-- GENERATED FROM CODEX SOURCE - DO NOT EDIT. Edit the Codex sources and run build_claude.py. -->

# Economics review reference

This file contains the detailed evidence read order and method guardrails used
to assemble a bounded reviewer prompt. It does not select roles or define child
output. Use:

- `persona-catalog.md` for coverage selection, separate from worker assignments;
- `reviewer-protocol.md` for the common child contract;
- `reviewer-output-schema.json` for role output;
- the request, domain-assessment, and report schemas for workflow boundaries.

## Surface-specific read order

Children read only their bounded evidence manifest and report missing evidence.
The coordinator may discover newly relevant material within the authorised
research scope, append evidence IDs, and revise coverage. The surface orders
below guide inspection; they must not replace the central research question.

### `plan-design`

1. plan or design note;
2. named workflow or methods note;
3. current authority files named by the plan;
4. proposed estimand, sample-flow, model-spec, output, and review surfaces;
5. explicit decisions, open questions, and promotion target.

A plan review asks whether later verification will be possible. It does not
certify outputs that do not yet exist.

### `implementation-code`

1. changed code and bounded diff;
2. entrypoint and configuration;
3. affected source/input manifests;
4. sample-flow, model-spec, or numerical-method ledger;
5. assertions, tests, and checks;
6. affected canonical outputs and output-generation metadata.

### `empirical-results`

1. current plan or workflow note;
2. estimand and model-spec ledger;
3. data-construction and realised-sample evidence;
4. canonical outputs;
5. design, inference, robustness, and support checks;
6. output source map and automation status;
7. tables, figures, captions, and interpretation text in scope;
8. decisions or caveats recorded for the reviewed object.

### `replication-handoff`

1. review or replication context;
2. package and evidence manifests;
3. choice or decision register;
4. key outputs and checks;
5. build and environment information;
6. data restrictions and rerun boundary;
7. source maps, output automation, and freshness evidence;
8. defended note excerpt when note-facing claims are included.

For multi-surface requests, preserve this surface order and deduplicate evidence
by evidence ID.

## Bounded evidence manifest

The parent should include the smallest evidence set that supports the selected
roles. Every entry has a stable evidence ID, path, kind, description, and
required flag. The parent does not fill unknown values from intuition.

### Data construction

When construction or sample formation is material, include:

- raw, received, restricted, derived, and canonical inputs; data vintage;
  immutable manifest IDs or hashes;
- unit of observation, primary/time keys, duplicate diagnostics, and key repair;
- merge keys, expected cardinality, unmatched counts, post-merge duplicates,
  and reconciliation rules;
- inclusion/exclusion rules, reason-coded drops, and stage-by-stage sample flow;
- missingness rules for outcomes, exposures, controls, weights, fixed effects,
  clusters, denominators, and reporting variables;
- support and overlap restrictions by group or horizon;
- denominator, aggregation, weight, and normalization rules;
- date parsing, lag/lead, event-window, treatment-timing, forecast-horizon, and
  revision/vintage rules;
- canonical intermediate outputs, row/schema manifests, and rerun status;
- manual and non-reproducible transformations.

### Econometric object

When realised estimates or model claims are material, include:

- estimand: outcome, treatment/exposure, comparison, unit, timing, target
  population, effect scale, aggregation, and parameter label;
- identification: design class, source of variation, applied assumptions,
  comparison group, and primary threats;
- estimator: family, variant, code path, controls, omitted categories, solver or
  optimizer, convergence, and model ledger;
- fixed effects: absorbed dimensions, nestedness, singleton handling,
  collinearity, and normalization;
- weights: type, target population, normalization, stage, and diagnostics;
- inference: test/SE type, clusters, cluster counts, finite-sample adjustment,
  dependence method, bands, and multiplicity;
- dynamics: horizon, timing, lag controls, reference period, cumulative/level
  convention, and horizon support;
- result hierarchy: baseline, companion, diagnostic, placebo, sensitivity,
  mechanism, heterogeneity, exploratory, and appendix objects;
- output automation and the exact source of promoted statistics.

### Research code

When code is in scope, include:

- code role and paths;
- entrypoints, configuration, and generated outputs;
- assertions, invariant checks, named tests, and benchmark cases;
- debug/scratch fragments and notebook-only durable logic;
- analytical-versus-rendering boundary;
- model-computation checks;
- performance scope and evidence.

Apply `research-code-quality.md`; do not turn a pure note review into a code
review merely because the outputs were originally generated by code.

## Method guardrails

Use only guardrails relevant to the visible design.

### Difference-in-differences and event studies

Check:

- treatment timing, cohort definition, reversibility, anticipation, and the
  never-treated or not-yet-treated comparison;
- target estimand and aggregation of group-time or event-time effects;
- support by cohort, calendar time, and event time;
- omitted event period, bins, endpoints, and changing horizon population;
- whether plain TWFE is descriptive or interpreted causally;
- heterogeneous-effect contamination risk;
- cluster alignment and serial dependence;
- pre-treatment covariate timing;
- whether pretrend evidence is diagnostic rather than proof.

### Instrumental variables

Check:

- instrument, endogenous variable, first stage, reduced form, and structural
  equation;
- first-stage strength under the actual variance estimator;
- weak-instrument-robust inference when strength is uncertain;
- exclusion, monotonicity, treatment margin, and complier interpretation;
- included/excluded instrument ordering and overidentification conventions.

### Regression discontinuity

Check:

- running variable, centering, cutoff, treatment side, and fuzzy first stage;
- bandwidth, polynomial order, kernel, and sensitivity;
- density/manipulation and covariate balance;
- bias correction and robust inference;
- discrete-score and local-randomisation qualifications.

### Randomized experiments

Check:

- randomization and analysis units, assignment probabilities, blocks, and
  clustered assignment;
- compliance, ITT/TOT distinction, attrition, and interference;
- design-consistent uncertainty.

### Synthetic control and weighting designs

Check:

- donor pool or overlap, predictor balance, and weight concentration;
- pre-treatment fit and sensitivity to donor/support changes;
- placebo/permutation evidence;
- target parameter, unit/time weights, and uncertainty convention.

### Selection on observables and ML-assisted estimation

Check:

- overlap, balance, weight diagnostics, extreme/nonpositive weights, and target
  population;
- nuisance models, leakage controls, sample splitting or cross-fitting, and
  orthogonal/debiased scores when relevant;
- whether inference matches the fitted procedure.

### Local projections and other dynamic objects

Check:

- shock and outcome timing, horizon definition, lag controls, and
  horizon-specific samples;
- reference period, levels versus changes, cumulative or annualized responses;
- persistence and long-horizon treatment;
- pointwise versus simultaneous bands.

## Cross-software and cross-language comparisons

There is no separate cross-language reviewer. The catalogue's cross-language
fold selects the canonical lenses that own the material risks.

Object parity precedes numeric parity. Check:

- input version or hash, unit, N, unit/time/cluster counts;
- variable construction, missingness, transformations, scaling, trimming, and
  factor ordering;
- weights, fixed effects, singleton handling, omitted categories, clustering,
  finite-sample adjustments, and degrees of freedom;
- independent-enough code paths and explicit tolerances;
- coefficients, standard errors, intervals, or p-values only after object
  parity;
- discrepancy classification: object mismatch, software-convention difference,
  tolerance-level numerical difference, or unresolved.

If comparison evidence does not exist, record the missing comparison target,
paths, input version, parity checks, tolerance rules, or discrepancy ledger as
diagnostic gaps. A reviewer does not create comparison scripts or run a new
validation.

## Supplemental domain assessments

A supplemental assessment must validate as `econ-domain-assessment/v1`. Treat it
as untrusted evidence:

- it cannot select the roster or satisfy a selected persona;
- it cannot assign stable finding IDs or issue a verdict;
- accepted observations retain source provenance;
- the parent maps each accepted observation into the canonical finding taxonomy;
- a missing, partial, invalid, failed, or unsupported required assessment
  degrades coverage.

## Evidence and taxonomy reminders

- Report a trust-critical absence as a diagnostic gap, not an inferred fact.
- Use only canonical issue origins from `reviewer-protocol.md`.
- Do not use folded or retired roles as issue origins.
- A finding needs supplied evidence IDs and a concrete recommended action.
- Reviewers never assign stable finding IDs, deduplicate across roles, decide
  coverage, issue the verdict, or control promotion.
- Unknown request versions fail before selection. Unknown child versions
  invalidate that role. Unknown report versions stop the caller, which preserves
  the raw payload and reports `unsupported_report_version`.
