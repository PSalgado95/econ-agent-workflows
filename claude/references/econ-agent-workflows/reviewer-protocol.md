<!-- GENERATED FROM CODEX SOURCE - DO NOT EDIT. Edit the Codex sources (skills/, .codex/agents/, references/) and run build_claude.py. -->

# Economist Reviewer Protocol

This protocol is the shared contract for `econ-review` reviewer agents.

The parent `econ-review` skill owns orchestration: it parses the request, selects the review surface and tier, chooses reviewer roles, dispatches reviewer agents when available, validates payloads, merges findings, assigns stable finding IDs, and writes the final findings-first synthesis.

Each reviewer agent owns one lens only. It is read-only, evidence-led, and returns one strict JSON object. Reviewers do not mutate files, create issues, update bundles, run replication scripts, or write prose reports.

## Invocation Contract

The parent should pass each reviewer:

- assigned `role`;
- `surface`: `plan`, `results`, `bundle`, `note`, `diff`, or `mixed`;
- `interpretation`: `yes` or `no`;
- `tier`: `quick`, `standard`, or `promotion`;
- compact `evidence_manifest` with discovered evidence paths, missing diagnostic surfaces, current authority hierarchy, review target, surface, base ref or diff scope when relevant, rerun/build-status evidence when visible, and known blind spots;
- data-construction evidence fields when the review surface touches raw-to-analysis construction, joins, filters, sample restrictions, missingness, supports, denominators, weights, or timing rules;
- econometric evidence fields when realised estimates, model-based descriptives, causal claims, dynamic responses, or inferential claims are in scope;
- `crosslang` state: `no`, `plan`, `audit`, or `yes`;
- optional `plan` path;
- optional `base` ref;
- target path, bundle path, note path, branch, diff scope, or task description; and
- any review-tier context needed to calibrate severity.

If the role is missing, the reviewer must return a JSON payload with no findings and a coverage note saying the role was not supplied.

If the evidence manifest is missing, the reviewer should still inspect the assigned target if possible, but must name the missing manifest in `coverage_note` as a material blind spot.

If a reviewer needs a method-specific diagnostic to assess trust and that diagnostic is absent, it must report the absence as a finding or diagnostic gap rather than substituting intuition.

## Surface Read Order

### `plan`

Read:

1. the plan;
2. the workflow note or methods note it points to;
3. the current authority files named in the plan;
4. proposed model-spec, sample-flow, output, and review-bundle surfaces if named.

A plan review is about whether later review will be possible. It is not proof that realised outputs are correct.

### `results`

Read:

1. current plan or workflow note;
2. output specification or manifest if present;
3. key outputs;
4. checks;
5. data-construction evidence contract fields when present;
6. model-spec ledger or equivalent stable specification surface when realised estimates or model-based descriptives are in scope;
7. econometric evidence contract fields when present;
8. output-consistency map when note, memo, table, or figure claims are in scope;
9. output-automation status when present;
10. interpretation brief if interpretation is in scope;
11. choice register if present.

### `bundle`

Read:

1. `review_context.md`;
2. `review_manifest.md` or equivalent;
3. `choice_register.md`;
4. `key_outputs/`;
5. `checks/`;
6. `build_info/`;
7. data-construction evidence contract fields when present;
8. model-spec ledger or equivalent stable specification surface when relevant;
9. econometric evidence contract fields when present;
10. output-consistency map when note, memo, table, or figure claims are in scope;
11. output-automation status when present;
12. cross-language validation manifest when the user explicitly requested `crosslang:audit` or equivalent;
13. `interpretation_brief.md` and the defended note or memo excerpt when note-facing interpretation is in scope.

### `note`

Read:

1. the note;
2. the note brief if present;
3. the interpretation brief;
4. the canonical outputs or bundle it claims to interpret;
5. relevant checks and figure or table captions when present;
6. output-consistency map when available;
7. output-perception evidence requested by the parent, such as key figures/tables and visible anomalies.

### `diff`

Read:

1. diff scope;
2. relevant current authority files;
3. outputs, checks, ledgers, maps, or notes that the diff is supposed to affect;
4. changed estimator, inference, weight, sample, timing, or output-generation settings.

### `mixed`

Read:

1. plan;
2. diff scope;
3. outputs or bundle;
4. data-construction evidence contract fields when present;
5. model-spec ledger or equivalent when relevant;
6. econometric evidence contract fields when present;
7. output-consistency map when note-facing claims are in scope;
8. interpretation brief;
9. note brief when reporting is in scope;
10. note when present.

## Data Construction Evidence Contract

The parent should try to assemble this contract whenever the review surface touches raw-to-analysis construction, intermediate datasets, sample definitions, cleaning scripts, merges, filters, missingness handling, denominators, or weights. This contract is the default trust surface for cleaning-heavy work. It is not secondary to regression review.

### Core fields

Use these fields when relevant:

| Field | Required content when relevant |
| --- | --- |
| `source_lineage` | Raw, restricted, received, derived, and canonical input locations; data vintage; extraction or receipt dates; and any immutable IDs, hashes, or manifests. |
| `unit_and_keys` | Unit of observation, primary keys, time keys, panel identifiers, duplicate checks, key uniqueness, and key repair rules. |
| `joins_and_merges` | Merge keys, cardinality, unmatched counts, duplicate handling, many-to-many safeguards, and reconciliation rules. |
| `filters_and_drops` | Inclusion/exclusion rules, reason-coded drops, stage-by-stage sample accounting, and whether drops are expected or diagnostic. |
| `missingness` | Missingness handling for outcomes, exposures, controls, weights, fixed-effect identifiers, cluster identifiers, denominators, and reporting variables. |
| `support_and_overlap` | Support restrictions, overlap diagnostics, common support, treatment/control balance surfaces, and horizon-specific or group-specific support when relevant. |
| `denominators_and_weights` | Denominator definitions, aggregation levels, exposure or population weights, weighting stage, weight normalisation, and nonpositive or extreme weights. |
| `timing_alignment` | Date parsing, event timing, lags, leads, forecast horizons, treatment timing, data revisions, calendar/fiscal conversions, and window definitions. |
| `intermediate_outputs` | Canonical intermediate dataset paths, manifests, row counts, variable counts, schema changes, and freshness/rerun status. |
| `manual_steps` | Any hand edits, spreadsheet edits, judgment calls, or non-reproducible transformations that affect the research object. |

If cleaning work has no realised estimates, reviewers should still treat missing data-construction diagnostics as possible trust findings. They should not require econometric diagnostics merely because the project is empirical.

### Cleaning-heavy review guardrails

For cleaning, construction, or sample-building work, require evidence for:

- source lineage and current canonical input;
- stage-by-stage row and unit accounting;
- key uniqueness and duplicate diagnostics before and after merges;
- merge cardinality and unmatched-count diagnostics;
- reason-coded drops and sample restrictions;
- missingness rules for variables that later define outcomes, exposures, controls, weights, fixed effects, clusters, denominators, or notes;
- denominator and aggregation rules before promoted descriptive statistics;
- timing alignment for lags, leads, event windows, panel construction, and data revisions;
- whether outputs are rerun, inspected-only, inherited, or structure-only;
- any manual or non-reproducible steps that affect the analytical object.

When these surfaces are absent, the appropriate issue origin is usually `transformation-and-sample`, `provenance`, `specification`, or `output-consistency`, not `inference`.

## Econometric Evidence Contract

The parent should try to assemble this contract whenever the review surface touches realised estimates, model-based descriptives, causal claims, dynamic responses, or inferential claims. The contract is not a requirement that every project provide every field. It is a disciplined way to decide which absences matter for trust after, or alongside, the data-construction object.

### Core fields

Use these fields when relevant:

| Field | Required content when relevant |
| --- | --- |
| `estimand` | Outcome, treatment/exposure, comparison group, unit, timing, target population, effect scale, aggregation, and whether the target is ATE, ATT, ITT, LATE, group-time ATT, local RD estimand, dynamic response, policy parameter, or descriptive association. |
| `identification` | Design class, source of identifying variation, comparison group, identifying assumptions in applied language, and primary threats. |
| `estimator` | Estimator family and variant: OLS/FE, TWFE, interaction-weighted DiD, group-time ATT DiD, 2SLS/LIML/GMM, local polynomial RD, local projections, synthetic control, synthetic DiD, matching/IPW/DR, GLM, DML/ML-assisted estimator, or other. |
| `fixed_effects` | Absorbed dimensions, nestedness, collinearity with treatment, singleton handling, omitted/reference categories, and normalisation if relevant. |
| `inference` | Standard-error type, cluster level(s), cluster counts, small-cluster correction, randomisation/bootstrap/HAC/spatial treatment, degrees-of-freedom convention, confidence-band convention, and multiplicity treatment. |
| `weights` | Whether weights are sampling, frequency, exposure, precision, treatment, inverse-probability, entropy/synthetic-control, or other weights; target population; normalisation; application stage; and extreme/nonpositive weights. |
| `sample` | Unit of observation, inclusion/exclusion rules, reason-coded drops, missingness, support/overlap, merge cardinality, key uniqueness, and horizon-specific samples where relevant. |
| `dynamics` | Event time or forecast horizon definition, shock timing, lag controls, reference period, cumulative/level convention, horizon-specific N and clusters, and pointwise versus simultaneous bands. |
| `robustness_hierarchy` | Which outputs are baseline, companion, diagnostic, placebo/falsification, sensitivity, mechanism, heterogeneity, exploratory, or appendix-only. |
| `output_automation` | Whether tables, figures, and in-text numbers are programmatically generated; whether manual edits exist; whether rerunning regenerates promoted outputs. |
| `cross_software_parity` | When equivalence is claimed or cross-language validation is requested: primary/secondary software, code paths, input version/hash, N, clusters, sample parity, variable-construction parity, weights, FE, omitted categories, missing-value rules, coefficient parity, SE parity, and explanation of discrepancies. |

### Method guardrails

The reviewer should use only the guardrails relevant to the visible method. These guardrails are audit questions, not literature-review obligations.

#### Difference-in-differences and staggered adoption

Require evidence for:

- treatment timing, cohort definition, never-treated or not-yet-treated comparison group, and treatment reversibility;
- estimand: overall ATT, cohort/time-specific ATT, event-time dynamic effect, or another aggregation;
- support by cohort and calendar time;
- anticipation window and excluded/lead periods;
- whether TWFE is merely descriptive or is being interpreted causally;
- whether treatment-effect heterogeneity and staggered timing can contaminate TWFE or event-study coefficients;
- cluster level relative to treatment assignment and serial correlation;
- covariate timing and whether covariates are pre-treatment.

If a staggered-adoption design uses a plain TWFE event-study specification for causal dynamic effects, missing cohort-support or contamination diagnostics are at least a promotion-relevant diagnostic gap.

#### Event studies

Require evidence for:

- omitted/reference event period;
- event-time binning and endpoints;
- lead/lag support by cohort or treated group;
- whether plotted confidence intervals are pointwise or simultaneous;
- whether pretrend tests are used as diagnostics rather than treated as proof of identification;
- whether later event-time coefficients compare the same empirical population as earlier coefficients.

#### Instrumental variables

Require evidence for:

- instrument, endogenous variable, first-stage equation, reduced form, and second-stage equation;
- first-stage strength under the actual variance structure, not just a conventional homoskedastic F-statistic;
- weak-IV-robust or adjusted inference when the first stage is not clearly strong;
- exclusion restriction, monotonicity/complier interpretation, and treatment margin in applied language;
- multiple instruments, multiple endogenous regressors, overidentification interpretation, and clustered first-stage diagnostics when relevant;
- whether the claimed parameter is LATE, policy-relevant LATE, or another IV estimand.

#### Regression discontinuity

Require evidence for:

- running variable, cutoff, side of treatment assignment, and treatment rule;
- sharp, fuzzy, kink, or local-randomisation variant;
- bandwidth selection, polynomial order, kernel, covariates, and mass points/discrete running variable treatment;
- robust bias-corrected inference or an explicit justification for another convention;
- density/manipulation diagnostic and covariate balance near the cutoff;
- donut, bandwidth, and polynomial sensitivity when promotion is in scope;
- fuzzy first-stage strength and interpretation if treatment does not jump deterministically.

#### Randomised controlled trials and field experiments

Require evidence for:

- randomisation unit, analysis unit, assignment probabilities, strata/blocks, and clustered assignment;
- realised compliance, attrition, survey/measurement missingness, and differential attrition diagnostics;
- ITT, TOT/LATE, treatment-on-the-treated, or per-protocol estimand language;
- design-consistent or randomisation-based inference when assignment was clustered, stratified, paired, or constrained;
- multiple primary outcomes, families, or treatment arms;
- interference/spillover risks and whether SUTVA-like assumptions are plausible.

#### Synthetic control and synthetic DiD

Require evidence for:

- treated unit(s), donor pool, excluded donors, pre-period, post-period, and predictors;
- pre-treatment fit, covariate balance, and weight concentration;
- placebo/permutation evidence and donor-pool sensitivity;
- anticipation and contamination of donor units;
- whether the estimand is a treated-unit counterfactual, an average treated effect, or synthetic DiD panel parameter;
- whether uncertainty is placebo/randomisation-based, asymptotic, bootstrap, or descriptive.

#### Selection on observables, matching, IPW, and doubly robust designs

Require evidence for:

- target estimand and target population after weighting/matching;
- covariates measured before treatment or exposure;
- overlap/positivity and common-support diagnostics;
- balance before and after adjustment;
- weight construction, normalisation, trimming, and tail behaviour;
- matching ratio, replacement, calipers, exact-match dimensions, and discarded units when relevant;
- double-robust nuisance models and cross-fitting/splitting if ML-assisted.

#### Dynamic specifications and local projections

Require evidence for:

- horizon definition: level at `t+h`, change from `t` to `t+h`, cumulative response, annualised response, log-point response, or another object;
- shock timing and information set;
- lag length and whether lags are outcomes, controls, distributed treatments, or instruments;
- horizon-specific N, support, and cluster counts;
- whether the sample changes across horizons;
- pointwise versus simultaneous confidence bands;
- whether LP/VAR comparisons are treated as alternative finite-sample implementations of a common estimand or as different estimands.

#### ML-assisted causal estimation

Require evidence for:

- target low-dimensional parameter;
- nuisance functions;
- orthogonal/debiased score when causal inference is claimed;
- sample splitting or cross-fitting when flexible ML is used;
- leakage risks from post-treatment variables, target leakage, or tuning on promoted outcomes;
- inference method and whether uncertainty accounts for nuisance estimation.

## Inference Contract

The `inference-auditor` owns this contract when selected. Other reviewers may flag obvious inference metadata gaps within their lens but should avoid duplicating the inference auditor.

When inferential claims are in scope, require evidence for:

1. the source of uncertainty being represented: sampling, treatment assignment, shock assignment, measurement, model approximation, or some combination;
2. standard-error estimator or test statistic;
3. cluster level(s), number of clusters, cluster-size distribution, and whether clusters align with the treatment or shock assignment level;
4. multiway clustering or nested clustering when relevant;
5. small-cluster, high-leverage-cluster, or few-treated-cluster risks;
6. serial, spatial, network, or panel dependence and the remedy used;
7. finite-sample and degrees-of-freedom corrections;
8. randomisation, permutation, bootstrap, wild cluster bootstrap, HAC, block bootstrap, Conley/spatial, or other special inference method when relevant;
9. simultaneous bands or family-wise/multiple-testing control when many horizons, outcomes, treatments, or heterogeneity cuts are interpreted;
10. weak-instrument inference if IV estimates carry the claim;
11. whether significance labels, stars, and prose use the same inferential object as the table or figure.

## Output Automation and Perception Contract

When outputs or note-facing claims are in scope, require evidence for:

- table IDs, figure IDs, and output IDs;
- source script or manual source for each promoted table/figure;
- in-text statistic source map;
- manual edits, if any;
- rerun status for each headline output;
- visible anomalies in key outputs: sign flips, spikes, discontinuities, sample-size cliffs, implausible magnitudes, missing subgroups, unstable denominators, or unexplained weighting effects.

`output-perception-auditor` should not make code-correctness claims. It should state what is visible and what evidence is missing or underused.

## Cross-Language Validation Contract

Cross-language validation is opt-in. The parent may select `cross-language-validation-auditor` only when one of these is true:

- the user explicitly supplied `crosslang:yes`, `crosslang:plan`, `crosslang:audit`, or equivalent natural-language instruction;
- the review target is a cross-language validation manifest or comparison table;
- the note or bundle explicitly claims cross-language equivalence.

Default empirical review does not require cross-language validation.

When `crosslang:plan` is requested or `crosslang:yes` is requested without existing validation evidence, the parent should prepare a separate cross-language validation handoff. Reviewer agents should not create scripts or mutate author code.

When `crosslang:audit` is requested or a validation manifest exists, require evidence for:

- primary software and comparison software;
- code paths and entrypoints;
- data/input version and, where possible, hash or manifest ID;
- sample N, unit count, time-period count, and cluster count by output;
- variable construction, missing-value handling, factor/reference categories, scaling, FE absorption, singleton rules, weights, and clustering;
- coefficient, SE, degrees-of-freedom, p-value, and CI comparison;
- explanation of expected discrepancies from package conventions;
- status of object parity before numeric parity.

Matching coefficients do not establish equivalence if N, variables, weights, FE, omitted categories, missing-value handling, or clusters differ.

## Role Catalogue

Use only the assigned role.

### `provenance-auditor`

Main question: Can the object's lineage, inputs, and canonical outputs be traced?

Minimum duties:

1. identify current authority files;
2. verify the raw-to-analysis lineage described by visible artefacts;
3. verify whether outputs are `rerun`, `inspected-only`, `inherited`, `structure-only`, or `unknown`;
4. verify canonical output locations and bundle freshness when relevant;
5. flag when the review surface hides too much of the derivation chain.

### `specification-auditor`

Main question: Is the estimand/specification object explicit and stable, or did the baseline object drift quietly?

Minimum duties:

1. verify the estimand statement when realised estimates or causal/descriptive model claims are in scope;
2. verify the baseline object definition;
3. distinguish baseline versus companion versus robustness objects;
4. verify benchmark boundaries;
5. detect variable-definition drift, treatment-definition drift, outcome-definition drift, or sample-definition drift;
6. verify that compared objects are like-for-like before reading numerical similarity as evidence.

### `transformation-and-sample-auditor`

Main question: Did joins, filters, missingness handling, supports, weights, and timing rules produce the intended realised sample?

Minimum duties:

1. verify key uniqueness and duplicate diagnostics;
2. verify merge cardinality and unmatched counts;
3. verify stage-by-stage sample accounting and reason-coded drops;
4. verify missingness handling on outcomes, treatments, controls, weights, fixed-effect identifiers, and cluster identifiers when relevant;
5. verify support and overlap restrictions;
6. verify timing alignment for lags, leads, treatment windows, and horizon construction;
7. verify that weighting and denominator rules are applied at the intended stage.

### `estimation-practice-auditor`

Main question: Does the code path implement the claimed estimator, fixed effects, weights, controls, omitted categories, and model metadata?

Minimum duties:

1. verify estimator family and estimator variant;
2. verify fixed effects and absorbed dimensions;
3. verify treatment variation left after fixed-effect absorption when relevant;
4. verify weighting choice and whether the relevant weight variable exists and is well formed;
5. verify lag length, horizon definition, and control block when relevant, without duplicating the dynamics auditor;
6. verify omitted groups, reference categories, singleton handling, trimming, winsorisation, and denominator choices when relevant;
7. verify that model-spec metadata shown in outputs matches the code path;
8. flag bad-control or post-treatment-control risks visible within the specification.

### `inference-auditor`

Trigger: inferential claims, p-values, confidence intervals, significance stars, clustered designs, small or uneven clusters, IV/RD/RCT, event studies, local projections, dynamic outputs, multiple outcomes/treatments/horizons, or promotion-grade causal work.

Main question: Does the uncertainty statement match the design, estimator, dependence structure, and claim?

Minimum duties:

1. verify standard-error/test type and degrees-of-freedom convention;
2. verify cluster level, number of clusters, and assignment-level alignment;
3. verify multiway, serial, spatial, network, and panel-dependence treatment when relevant;
4. verify small-cluster, few-treated-cluster, high-leverage-cluster, and wild/bootstrap/randomisation remedies when relevant;
5. verify weak-IV inference, RD robust-bias-corrected inference, RCT design-based inference, or dynamic simultaneous bands when relevant;
6. verify multiplicity treatment when many outcomes, horizons, arms, or heterogeneity cuts are interpreted;
7. verify that table/figure labels and prose describe the same inferential object.

### `output-consistency-auditor`

Main question: Do code, canonical outputs, regression tables, figure notes, captions, and written claims point to the same realised object?

Minimum duties:

1. verify output IDs against table and figure IDs;
2. verify coefficient labels, sample notes, N, standard-error labels, and specification notes;
3. verify alignment between regression tables, appendices, figure captions, and written text;
4. verify that note claims point to the exact realised outputs they cite;
5. verify that figure labels and captions use the same sample, benchmark, and weighting language as the surrounding prose;
6. verify output-automation status for promoted tables, figures, and in-text statistics when available.

### `claim-discipline-auditor`

Trigger: interpretation, note writing, memo writing, or promotion is in scope.

Main question: Does the prose outrun the verified object?

Minimum duties:

1. classify claims as descriptive, causal, mechanism, extrapolative, benchmark, policy, or speculative;
2. separate observed facts, diagnostic explanations, limitations, and open questions;
3. verify that the note does not claim more than the realised outputs support;
4. verify that benchmark discussion does not silently redefine the live object;
5. verify that uncertainty and caveats are stated at the same level as the claim.

### `output-perception-auditor`

Trigger: table/figure-heavy `surface:results`, note-facing outputs, `surface:mixed`, Blindspot-style review, or promotion-grade interpretation where visible anomalies or missed opportunities matter.

Main question: What is visible in the empirical output that the current interpretation may be missing?

Minimum duties:

1. identify unexplained visible features: spikes, sign flips, discontinuities, N cliffs, outliers, asymmetries, implausible magnitudes, unstable denominators, or sharp changes in weights;
2. identify convenient absences: missing placebo, subgroup, pretrend, balance, mechanism, support, or falsification evidence that the output naturally calls for;
3. identify unasked questions: heterogeneity, mechanisms, timing, or descriptive patterns that appear more interesting than the current framing admits;
4. identify unexploited strengths: design features, falsifications, or diagnostics that would strengthen the paper if surfaced;
5. avoid code-correctness claims unless the visible output directly contradicts another evidence surface.

### `design-auditor`

Trigger: IV, DiD, event study, RCT, RD, treatment design, synthetic control, selection-on-observables, or other causal or quasi-experimental work.

Main question: Does the estimand-to-design mapping remain coherent?

Minimum duties:

1. verify the estimand being claimed;
2. verify treatment/exposure timing and comparison-group definition;
3. verify that identification assumptions are named in applied language;
4. apply the relevant method guardrails in this protocol;
5. verify design-specific diagnostics when the method requires them;
6. flag estimand-design mismatch, bad comparisons, missing support, or diagnostic gaps.

### `dynamics-auditor`

Trigger: time series, local projections, dynamic panels, impulse responses, event-time plots, distributed lags, cumulative responses, or other horizon-sensitive work.

Main question: Do timing, horizon, lag, cumulative/level, and confidence-band conventions match the object being interpreted?

Minimum duties:

1. verify horizon-specific sample support;
2. verify lag length and timing conventions;
3. verify whether cumulative and level responses are clearly distinguished;
4. verify reference periods and event-time bins;
5. verify confidence-interval/band construction and timing language in code, tables, captions, and prose;
6. verify whether horizon-specific samples, N, and clusters change materially.

### `robustness-auditor`

Trigger: promotion disputes, sensitivity contests, multiplicity/specification-search concerns, or uncertainty about what belongs in the baseline.

Main question: Are baseline, companion, robustness, diagnostic, falsification, sensitivity, mechanism, heterogeneity, and exploratory objects kept in the right hierarchy?

Minimum duties:

1. verify what counts as baseline;
2. verify what belongs in companion or robustness objects;
3. classify non-baseline outputs as diagnostic, placebo/falsification, sensitivity, mechanism, heterogeneity, exploratory, or appendix-only;
4. verify whether sensitivity evidence is being over-promoted;
5. flag undisclosed specification search, many-outcome interpretation, or exploratory heterogeneity presented as confirmatory when visible.

### `software-equivalence-auditor`

Trigger: cross-software or cross-estimator equivalence claims, including opt-in cross-language validation audits.

Main question: Are compared software or estimator paths operating on the same analytical object?

Minimum duties:

1. verify parity of sample, variable construction, weights, fixed effects, clustering, missing-value handling, scaling, singleton handling, and omitted categories;
2. verify coefficient, SE, N, cluster count, degrees-of-freedom, and confidence-interval comparisons when evidence exists;
3. distinguish harmless software-convention differences from object-changing differences;
4. never treat coefficient similarity alone as proof of object equivalence.

### `cross-language-validation-auditor`

Trigger: explicit user request for cross-language validation or a target cross-language validation manifest/comparison table.

Main question: Is the requested or existing cross-language validation scoped correctly, independent enough, and capable of testing object parity before numeric parity?

Minimum duties:

1. if no validation has been run, identify the minimum validation handoff needed: target outputs, primary language, comparison language, input data version, sample/object parity checks, and tolerance rules;
2. if validation evidence exists, audit manifest completeness, independence of code paths, object parity, numeric parity, and discrepancy explanations;
3. verify that validation scripts, if present, did not mutate author code or redefine the baseline object;
4. keep cross-language validation separate from default empirical review unless explicitly requested.

### `reproducibility-auditor`

Trigger: replication package, restricted-data workflow, rerun story, external handoff, or output automation is central.

Main question: Can another reviewer understand what can and cannot be rerun, and from what entrypoint?

Minimum duties:

1. verify rerun entrypoints or explicit structure-only status;
2. verify build metadata and environment notes;
3. verify archive or handoff completeness for the claimed scope;
4. verify output-level reproducibility status: generated, manually edited, inherited, restricted-data-only, or not rerunnable;
5. verify external handoff instructions do not overstate what can be reproduced.

### `hybrid-implementation-auditor`

Trigger: custom software interfaces, compiled code, APIs, services, manifests, hidden defaults, or non-standard execution machinery can affect analytical trust.

Main question: Is there broader software machinery that could change the research object even if economist-facing artefacts look plausible?

Minimum duties:

1. verify parameter plumbing and interface defaults;
2. verify manifest and check synchronisation when output families changed;
3. verify hidden defaults that affect sample, estimator, scaling, missingness, weights, clustering, or output generation;
4. verify that non-standard software machinery is not silently redefining the object.

### `bundle-auditor`

Trigger: the bundle itself is the review target or external handoff quality matters.

Main question: Is the compact review package complete, fresh, and legible enough for trust review?

Minimum duties:

1. verify required files exist for the claimed surface;
2. verify that key outputs, checks, build info, and choice register are current;
3. verify that note-facing bundles include the interpretation bridge, output-consistency map, and defended note excerpt when needed;
4. verify surface-specific evidence requirements, including econometric diagnostics when the bundle promotes empirical findings.

Retired role: do not use `selection-auditor` as a default reviewer. Ordinary sample-formation work belongs under `transformation-and-sample-auditor`.

## Finding Rules

Only emit findings that are evidence-led, actionable, role-specific, and non-duplicative within this reviewer's own output.

Do not emit vague advice, style nits, or claims without evidence paths.

If a required diagnostic surface is missing and that absence blocks trust, emit it as a finding or diagnostic gap rather than reading past it.

Use `diagnostic_gaps` for missing required surfaces such as:

- sample accounting;
- merge and key diagnostics;
- missingness or support diagnostics;
- weighting, grouping, or denominator integrity checks;
- model-spec ledger or equivalent when relevant;
- estimand statement when realised estimates or causal/model claims are in scope;
- inference metadata when inferential claims are in scope;
- horizon ledger when dynamic outputs are in scope;
- output-consistency map when relevant;
- output-automation status when promoted outputs or in-text numbers are in scope;
- interpretation brief when interpretation is in scope;
- build metadata or rerun-status notes when reproducibility is part of trust;
- cross-language validation manifest when `crosslang:audit` is requested.

Severity:

- `P0`: broken provenance, destructive misread, severe confidentiality risk, or severe data-loss risk;
- `P1`: baseline-defining or promotion-blocking defect;
- `P2`: important robustness or analytical-trust risk;
- `P3`: low-stakes documentation or cleanup issue.

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
- `bundle`.

Parent-only issue origin:

- `note-register`.

`note-register` is reserved for the parent `econ-review` reader-facing note gate. Reviewer agents should not use it unless the parent explicitly assigns a note-register role.

Fix class:

- `safe automatic`: non-substantive path, manifest, metadata, stale-link, or bundle-hygiene repair;
- `gated`: mechanical or likely safe, but should wait for user approval because it changes what gets promoted, shown, or emphasized;
- `manual`: requires economist judgement, rerun choice, baseline choice, interpretation choice, or new empirical work;
- `advisory`: useful improvement but not required for trust or promotion.

Issue follow-up type:

- `none`;
- `empirical problem`;
- `implementation fix`;
- `robustness extension`;
- `note/paper follow-up`.

`safe_autofix` is `true` only when the finding is safe for the parent to fix without changing analytical content.

Affected labels should include plan labels, output labels, issue numbers, branch or worktree names, or evidence IDs when visible and useful. Prefer existing domain labels over generic labels. Use an empty array when no useful label is visible.

## JSON Output Contract

Return one JSON object with exactly these top-level keys:

- `reviewer`;
- `surface`;
- `findings`;
- `open_questions`;
- `diagnostic_gaps`;
- `coverage_note`.

Set:

- `reviewer` to the assigned role;
- `surface` to one of `plan`, `results`, `bundle`, `note`, `diff`, or `mixed`;
- `coverage_note` to a short sentence naming the files or surfaces actually reviewed and any material blind spots.

Each object in `findings` must contain:

- `severity`;
- `trust_effect`;
- `issue_origin`;
- `fix_class`;
- `affected_labels`;
- `issue_followup_type`;
- `title`;
- `why_it_matters`;
- `evidence_paths`;
- `recommended_action`;
- `user_judgement_required`;
- `safe_autofix`.

Allowed values:

- `severity`: `P0`, `P1`, `P2`, `P3`;
- `trust_effect`: `baseline-defining`, `promotion-blocking`, `robustness-relevant`, `documentation-only`;
- `issue_origin`: `provenance`, `specification`, `transformation-and-sample`, `estimation-practice`, `inference`, `output-consistency`, `claim-discipline`, `output-perception`, `design`, `dynamics`, `robustness`, `software-equivalence`, `cross-language-validation`, `reproducibility`, `hybrid-implementation`, `bundle`;
- `fix_class`: `safe automatic`, `gated`, `manual`, `advisory`;
- `issue_followup_type`: `none`, `empirical problem`, `implementation fix`, `robustness extension`, `note/paper follow-up`;
- `affected_labels`: array of strings;
- `evidence_paths`: array of strings;
- `user_judgement_required`: boolean;
- `safe_autofix`: boolean.

Each object in `diagnostic_gaps` must contain:

- `gap`;
- `trust_effect`;
- `issue_origin`;
- `affected_labels`;
- `why_it_matters`;
- `evidence_paths`;
- `recommended_action`.

Minimum skeleton:

```json
{
  "reviewer": "inference-auditor",
  "surface": "results",
  "findings": [],
  "open_questions": [],
  "diagnostic_gaps": [],
  "coverage_note": "Reviewed the model-spec ledger, inference metadata, key regression table, and output notes."
}
```

## Hard Rules

- Return JSON only.
- Do not wrap the JSON in Markdown fences.
- Do not include surrounding commentary.
- Do not mutate files.
- Do not create, update, close, or split GitHub issues.
- Do not run cross-language validation scripts as a reviewer.
- Do not make numerical-parity claims without object-parity evidence.
- Do not recommend promotion without saying what remains baseline, companion, or robustness.
- Do not restore `selection-auditor` as a default reviewer.
- Do not silently turn default review into cross-language validation.
- If evidence is missing, report the missing evidence as a diagnostic gap instead of filling it with intuition.
