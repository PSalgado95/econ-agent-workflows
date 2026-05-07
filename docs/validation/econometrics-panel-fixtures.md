# Econometrics panel validation fixtures

Use these as behavioural tests for the upgraded `econ-review` panel. They are not full datasets; they are minimal scenarios that can be represented by toy manifests, tables, or review bundles.

## Fixture 0: Cleaning-only sample construction

Scenario:
- A diff changes raw-to-analysis cleaning code.
- The work updates merge keys, sample restrictions, missingness rules, and denominator construction.
- No regression table, standard errors, causal claim, or note-facing interpretation is present.

Expected reviewers:
- `provenance-auditor`
- `specification-auditor`
- `transformation-and-sample-auditor`
- `output-consistency-auditor`

Expected findings/gaps:
- Missing duplicate/key diagnostics should be reported as data-construction gaps.
- Missing unmatched-count or merge-cardinality diagnostics should be reported as transformation/sample gaps.
- Missing denominator or sample-flow documentation should be reported before any promoted descriptive output.
- `inference-auditor`, `design-auditor`, `dynamics-auditor`, and `cross-language-validation-auditor` should not be selected.

## Fixture 1: Staggered-adoption DiD with plain TWFE

Scenario:
- Outcome: employment rate by county-year.
- Treatment: policy adoption in different years.
- Table reports TWFE coefficient and event-study leads/lags.
- No cohort-by-event-time support table.
- No statement of never-treated versus not-yet-treated comparison group.

Expected reviewers:
- `specification-auditor`
- `design-auditor`
- `dynamics-auditor`
- `inference-auditor`
- `robustness-auditor` at promotion tier

Expected findings/gaps:
- Missing group-time or event-time support diagnostic.
- Missing comparison-group definition.
- Potential TWFE/event-study contamination if heterogeneous effects are interpreted causally.
- Missing cluster count or assignment-level clustering evidence if not provided.

## Fixture 2: Event-study figure with pointwise CIs but simultaneous claim

Scenario:
- Figure plots 10 leads and 12 lags.
- Caption says "no pretrend and persistent effect at all horizons."
- CIs are pointwise, but not labelled.
- Later horizons have much smaller N.

Expected reviewers:
- `dynamics-auditor`
- `inference-auditor`
- `claim-discipline-auditor`
- `output-perception-auditor`

Expected findings/gaps:
- Pointwise versus simultaneous bands unclear.
- Horizon-specific sample support missing or changing.
- "No pretrend" language overstates a joint design diagnostic.
- Visible late-horizon instability should be flagged as output-perception issue.

## Fixture 3: IV with first-stage F but no weak-IV-robust inference

Scenario:
- Single endogenous treatment.
- Table reports 2SLS, robust SE, first-stage F = 11.5.
- Claim rests on statistical significance.
- No reduced form table and no weak-IV-robust inference.

Expected reviewers:
- `design-auditor`
- `estimation-practice-auditor`
- `inference-auditor`
- `claim-discipline-auditor`

Expected findings/gaps:
- Missing reduced form.
- Weak-IV inference not established by a conventional threshold alone.
- Complier/LATE interpretation missing if not stated.

## Fixture 4: RD with bandwidth sensitivity missing

Scenario:
- Sharp RD at eligibility cutoff.
- Table reports local linear estimate.
- No density/manipulation diagnostic.
- No bandwidth/polynomial sensitivity.
- No bias-corrected inference metadata.

Expected reviewers:
- `design-auditor`
- `estimation-practice-auditor`
- `inference-auditor`
- `robustness-auditor`

Expected findings/gaps:
- Running variable/cutoff may be clear, but manipulation and balance diagnostics missing.
- Bandwidth and inference convention missing.
- Promotion should be blocked until RD diagnostic surfaces exist.

## Fixture 5: Cluster-randomised trial with few clusters

Scenario:
- Treatment assigned at school level; outcomes at student level.
- 18 schools.
- Table uses heteroskedastic robust SEs clustered nowhere.
- Some attrition by treatment arm.

Expected reviewers:
- `design-auditor`
- `transformation-and-sample-auditor`
- `inference-auditor`
- `claim-discipline-auditor`

Expected findings/gaps:
- Inference not aligned with assignment level.
- Small-cluster remedy or randomisation inference missing.
- Attrition/missingness diagnostic required.

## Fixture 6: Synthetic control with donor contamination

Scenario:
- Treated state receives policy in 2015.
- Donor pool includes states adopting similar policy in 2016-2017.
- Pre-period fit is shown, but donor weights and placebo evidence are missing.

Expected reviewers:
- `design-auditor`
- `estimation-practice-auditor`
- `inference-auditor`
- `output-perception-auditor`

Expected findings/gaps:
- Donor-pool contamination/anticipation risk.
- Missing donor weights and placebo/permutation evidence.
- Strong-looking pre-period fit alone is insufficient.

## Fixture 7: Local projections with changing horizon samples

Scenario:
- LP impulse responses from h=0 to h=20.
- The dependent variable is `y_{t+h} - y_t`, but caption calls it level response.
- N falls sharply after h=12.
- Bands are not labelled as pointwise or simultaneous.

Expected reviewers:
- `dynamics-auditor`
- `inference-auditor`
- `output-consistency-auditor`
- `output-perception-auditor`

Expected findings/gaps:
- Level/cumulative/change convention mismatch.
- Horizon-specific N and support issue.
- Band convention unclear.

## Fixture 8: IPW/selection-on-observables with extreme weights

Scenario:
- Observational treatment comparison using inverse-probability weights.
- No overlap plot.
- Weight max is very large, but table only reports weighted regression.
- Covariates include one post-treatment variable.

Expected reviewers:
- `specification-auditor`
- `transformation-and-sample-auditor`
- `design-auditor`
- `estimation-practice-auditor`
- `robustness-auditor`

Expected findings/gaps:
- Target population after weighting unclear.
- Overlap/positivity diagnostics missing.
- Extreme weights and trimming/sensitivity needed.
- Post-treatment-control risk.

## Fixture 9: Output-perception t=1 spike

Scenario:
- Event-study graph has an isolated large positive effect at event time +1.
- Text discusses only the average post-treatment effect.
- No mechanism or timing explanation.

Expected reviewers:
- `output-perception-auditor`
- `dynamics-auditor`
- `claim-discipline-auditor`

Expected findings/gaps:
- Unexplained visible feature: t=1 spike.
- Potential missed mechanism/timing story or diagnostic check.
- Avoid claiming code error unless other evidence supports it.

## Fixture 10: Cross-language comparison with coefficient match but N mismatch

Scenario:
- User supplies `crosslang:audit`.
- R and Stata coefficients match to 5 decimals.
- R N = 42,010; Stata N = 41,887.
- Cluster counts differ by two.
- Manifest lacks missing-value handling and singleton rules.

Expected reviewers:
- `cross-language-validation-auditor`
- `software-equivalence-auditor`
- `reproducibility-auditor` if handoff is promotion-relevant

Expected findings/gaps:
- Object parity fails despite coefficient similarity.
- Missing missing-value/singleton explanation.
- Equivalence claim should be blocked until N and cluster-count discrepancy is resolved.

## Fixture 11: Cross-language requested but no manifest

Scenario:
- User asks: `crosslang:plan` or "prepare a Stata validation".
- No validation scripts or manifest exist.

Expected behaviour:
- Parent should prepare a cross-language validation handoff.
- It should not claim validation has been run.
- It need not spawn `software-equivalence-auditor` unless there is an existing equivalence object to audit.

Expected output section:
- `Cross-language validation handoff` with target outputs, primary/comparison software, object parity checks, numeric comparison checks, and independence boundary.
