# Economics review persona catalogue

This file is the authoritative catalogue for `econ-review`. Personas are prompt
assets, not registered agents, commands, skills, or user-selectable products.
The parent selects checks for coverage. It may apply lenses locally or group
related lenses in one bounded worker assignment. Lens count is not agent count.

## Canonical role order

All ordered unions, coverage rows, and finding-source lists use
this order:

1. `provenance`
2. `specification`
3. `transformation-and-sample`
4. `estimation-practice`
5. `inference`
6. `output-consistency`
7. `claim-discipline`
8. `output-perception`
9. `code-quality`
10. `design`
11. `dynamics`
12. `robustness`
13. `software-equivalence`
14. `reproducibility`
15. `bundle`

| Role | Prompt asset |
| --- | --- |
| `provenance` | `personas/provenance.md` |
| `specification` | `personas/specification.md` |
| `transformation-and-sample` | `personas/transformation-sample.md` |
| `estimation-practice` | `personas/estimation-practice.md` |
| `inference` | `personas/inference.md` |
| `output-consistency` | `personas/output-consistency.md` |
| `claim-discipline` | `personas/claim-discipline.md` |
| `output-perception` | `personas/output-perception.md` |
| `code-quality` | `personas/code-quality.md` |
| `design` | `personas/design.md` |
| `dynamics` | `personas/dynamics.md` |
| `robustness` | `personas/robustness.md` |
| `software-equivalence` | `personas/software-equivalence.md` |
| `reproducibility` | `personas/reproducibility.md` |
| `bundle` | `personas/bundle.md` |

## Base-surface matrix

Normalize requested surfaces into this table order. For `depth: quick`, add
each applicable quick core. For `depth: standard`, add each standard core.
`depth: full` also starts from the standard core; full means all applicable
cores and triggered lenses, not all fifteen roles.

| Surface | Quick core | Standard core |
| --- | --- | --- |
| `plan-design` | `design`, `specification` | `design`, `specification`, `claim-discipline` |
| `implementation-code` | `transformation-and-sample`, `code-quality` | `transformation-and-sample`, `code-quality`, `reproducibility` |
| `empirical-results` | `specification`, `inference`, `output-consistency` | `specification`, `inference`, `robustness`, `output-consistency`, `claim-discipline` |
| `replication-handoff` | `provenance`, `reproducibility`, `bundle` | `provenance`, `reproducibility`, `bundle`, `output-consistency` |

## Conditional triggers

Apply every true trigger; triggers compose rather than replace one another.

| Trigger | Add |
| --- | --- |
| Source lineage, imported evidence, uncertain authority, or freshness risk | `provenance` |
| Joins, filters, missingness, support, denominators, weights, timing, or realised sample formation | `transformation-and-sample` |
| Non-trivial estimator, optimiser, weighting, fixed-effect, convergence, or numerical choice | `estimation-practice` |
| P-values, intervals, bands, clustering, design-based uncertainty, dependence, or multiplicity | `inference` |
| Substantive tables, figures, captions, or in-text statistics | `output-perception`, `output-consistency` |
| Code, notebooks, helpers, tests, custom interfaces, compiled machinery, hidden defaults, or parameter plumbing affect research trust | `code-quality` |
| Causal or quasi-experimental claim | `design` |
| Event time, local projections, impulse responses, lags, horizons, cumulative responses, or dynamic bands | `dynamics` |
| Baseline placement, sensitivity, falsification, mechanism, heterogeneity, multiplicity, or specification-search discipline | `robustness` |
| Cross-software, cross-estimator, or cross-language equivalence claim | `software-equivalence` |
| Rerun, environment, restricted-data, automation, or replication completeness matters | `reproducibility` |
| The compact review package itself is in scope | `bundle` |

### Cross-language fold

There is no cross-language persona. A cross-language comparison always selects
`software-equivalence`. It also selects:

- `transformation-and-sample` when data construction, sample formation,
  variable construction, missingness, weights, or object support may differ;
- `reproducibility` when independent rerun paths, input versions, environments,
  or build parity matter.

The comparison must establish object parity before numeric parity, use
independent enough code paths to expose shared mistakes, state tolerances, and
classify discrepancies as object mismatch, software-convention difference,
tolerance-level numerical difference, or unresolved.

### Hybrid/custom implementation fold

There is no hybrid-implementation persona. Custom software machinery always
selects `code-quality` for transparency, interface defaults, parameter plumbing,
tests, and hidden machinery, and `estimation-practice` for estimator or
numerical validity. Also add:

- `transformation-and-sample` when the machinery can change construction or the
  realised sample;
- `reproducibility` when it changes entrypoints, environments, or rerun status;
- `output-consistency` when it changes generated outputs, manifests, or labels.

## Promotion modifier

`promotion: true` is independent of the base surfaces. Add
`reproducibility` and `claim-discipline`, then apply these promotion triggers:

- baseline, companion, sensitivity, falsification, mechanism, heterogeneity, or
  exploratory-result placement adds `robustness`;
- a promoted causal claim adds `design`;
- a promoted table, figure, caption, or in-text statistic adds
  `output-perception` and `output-consistency`;
- a promoted replication deliverable adds `bundle`;
- every ordinary conditional trigger remains active.

## Deterministic selection algorithm

1. Reject an unknown request version before selection.
2. Normalize and order base surfaces by the matrix order.
3. Add each applicable quick or standard core. Full starts from standard.
4. Add every conditional role, including all fold co-selections.
5. Apply the promotion modifier.
6. Deduplicate and sort by canonical role order.
7. Record the coverage inventory, then decide separately which checks merit delegation.
   Reassess coverage as relevant evidence emerges within the authorised scope.

Do not turn this inventory into a mandatory child queue. Relevant lenses may be
covered by the parent. Explain material scope choices and disclose unchecked
concerns; delegation budgets limit workers, not the questions the parent can ask.
