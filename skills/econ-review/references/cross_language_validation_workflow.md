# Cross-language validation workflow

Cross-language validation is an optional, user-triggered extension to `econ-review`. It is not part of the default empirical-review panel.

## Trigger

Use this workflow only when:

- the user supplies `crosslang:yes`, `crosslang:plan`, `crosslang:audit`, or equivalent natural-language instruction;
- the review target is a cross-language validation manifest or comparison table; or
- the note/bundle explicitly claims cross-language equivalence.

Default review should not trigger this workflow.

## Parent behaviour

### `crosslang:plan`

Prepare a separate validation handoff. Do not claim validation has been run.

### `crosslang:yes`

If a validation manifest or comparison outputs are present, audit them. Otherwise, prepare a validation handoff.

### `crosslang:audit`

Audit an existing validation manifest or comparison outputs. If absent, report a diagnostic gap and prepare the handoff.

## Independence boundary

Cross-language validation should be independent enough to catch implementation mistakes, but it should not mutate author code.

Rules:

1. Validation scripts, if later created, should live in a separate validation or replication area.
2. They should read approved analysis inputs and write separate validation outputs.
3. They should not alter source data, analysis data, author scripts, or promoted outputs.
4. They should not redefine the baseline specification, sample, or estimand.
5. They should document all discrepancies as object mismatch, software-convention difference, tolerance-level numerical difference, or unresolved.

## Validation target ledger

A cross-language validation handoff should name the smallest set of objects worth validating.

Prefer:

- the baseline headline table;
- the headline figure if it is generated from a model object;
- one sample-construction or transformation object if sample risk is central;
- one robustness/appendix object only if the user asks or if it is promotion-critical.

Avoid trying to replicate the entire project in the first pass.

Template:

```yaml
cross_language_validation:
  status: planned|in_progress|complete|audited|failed
  requested_by_user: true
  primary_software:
  comparison_software:
  validation_targets:
    - output_id:
      table_or_figure:
      baseline_spec_id:
      estimand:
      source_data_or_input:
      expected_unit_of_observation:
      expected_N:
      expected_cluster_count:
      expected_weight:
      expected_fixed_effects:
      expected_cluster_level:
      primary_code_path:
      comparison_code_path:
```

## Object parity before numeric parity

Before comparing coefficients, require parity on:

- data/input version and hash or manifest ID when available;
- unit of observation;
- sample N, unit count, period count, and cluster count;
- treatment/exposure, outcome, controls, and covariate timing;
- missing-value handling;
- weights and normalisation;
- fixed effects, singleton dropping, and collinearity handling;
- omitted/reference categories and factor-level ordering;
- scaling, transformations, logs, winsorisation, and trimming;
- clustering and finite-sample/degrees-of-freedom conventions.

If object parity fails, numeric similarity is not evidence of equivalence.

## Numeric comparison expectations

For deterministic transformations:

- counts, sums over integer-valued indicators, and exact category totals should normally match exactly;
- floating-point transformations should match within a stated tolerance if implemented by different libraries.

For model outputs:

- coefficient equality can be expected for many linear models once sample, variables, weights, and fixed effects are equivalent;
- standard errors may differ because of degrees-of-freedom corrections, finite-sample adjustments, cluster conventions, absorbed-FE handling, or package defaults;
- p-values and confidence intervals should be compared only after the SE and DoF conventions are documented;
- exact six-decimal equality is a useful debugging target, not a universal pass/fail rule.

## Software-specific pitfalls

### Stata/R/Python high-dimensional fixed effects

Check:

- singleton handling;
- absorbed fixed-effect normalisation;
- collinearity and omitted category rules;
- cluster degrees-of-freedom corrections;
- treatment of weights;
- factor/interactions syntax;
- missing-value propagation.

### DiD/event-study packages

Check:

- estimand and aggregation target;
- comparison group: never-treated, not-yet-treated, or other;
- cohort support;
- event-time bins and reference period;
- standard-error bootstrap or clustering convention.

### IV packages

Check:

- endogenous/instrument variable order;
- included and excluded instruments;
- first-stage diagnostics under the actual variance estimator;
- weak-IV robust tests or adjustments;
- overidentification test conventions.

### RD packages

Check:

- running variable centring;
- cutoff side and treatment indicator;
- bandwidth selector;
- polynomial order and kernel;
- bias-correction and robust SE convention;
- fuzzy first-stage treatment.

## Minimum output manifest

A completed validation should write a manifest like this:

```md
# Cross-language validation manifest

Status: complete|failed|partial
Primary software:
Comparison software:
Validation date:
Validation author/agent:
Independence boundary:

## Inputs
- Source data/input version:
- Hash or manifest ID:
- Primary code path:
- Comparison code path:

## Target objects
| Output ID | Spec ID | Estimand | Primary path | Comparison path |
| --- | --- | --- | --- | --- |

## Object parity
| Output ID | N primary | N comparison | Clusters primary | Clusters comparison | Weights parity | FE parity | Missingness parity | Status |
| --- | ---: | ---: | ---: | ---: | --- | --- | --- | --- |

## Numeric parity
| Output ID | Coef primary | Coef comparison | Coef diff | SE primary | SE comparison | SE diff | DoF convention | Status |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |

## Discrepancies
| Output ID | Type | Explanation | Resolution |
| --- | --- | --- | --- |

## Verdict
- Object parity: pass|fail|partial
- Numeric parity: pass|fail|partial|not meaningful because object parity failed
- Remaining blockers:
```

## How `econ-review` should audit this manifest

Select:

- `cross-language-validation-auditor` to audit manifest completeness, independence boundary, target scope, and discrepancy classification;
- `software-equivalence-auditor` to audit object parity and numerical parity claims;
- `estimation-practice-auditor` or `inference-auditor` if the discrepancies involve estimator or inference conventions.

Do not claim validation passed unless object parity and numeric comparison evidence both support that conclusion for the target objects.
