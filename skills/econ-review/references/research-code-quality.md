# Research code quality

Use this guardrail when code affects an economics research object: data
construction, estimation, simulation, calibration, model solving, numerical
routines, reusable research tooling, or code-generated outputs.

The purpose is research trust. Report a code-quality problem only when it harms
readability, rerun safety, reviewability, safe modification, or confidence in
the analytical object. Suppress pure style preferences.

## Code roles

- `exploratory`: local inspection; keep the object legible without demanding
  package structure.
- `analysis-pipeline`: creates data, estimates, tables, figures, model objects,
  or diagnostics used by the project.
- `shared-collaborator`: another researcher is expected to read, rerun, or edit.
- `replication-facing`: supports a replication or review package.
- `library-tool`: reusable machinery whose behavior other work depends on.

## Always-on floor

- make entrypoints and rerun paths visible;
- use descriptive names for research objects and object-defining parameters;
- keep analytical logic distinct from rendering when practical;
- remove tracked debug prints, scratch plots, stale commented code, and ad hoc
  test fragments;
- assert object-defining invariants such as keys, merge cardinality, dimensions,
  support, denominators, convergence, residuals, accounting identities, and
  expected outputs;
- use named tests for reusable, collaborator-facing, replication-facing, or
  recurring-bug behavior.

## Hidden machinery

Custom interfaces, compiled routines, services, manifests, helpers, or notebook
state are material when they can change the object. Check:

- parameter plumbing and interface defaults;
- hidden filters, missingness rules, weights, scaling, cluster choices, and
  output-generation behavior;
- synchronization between code, manifests, checks, and output families;
- durable module boundaries for notebook-only logic that must be reused;
- transparent error, convergence, and fallback behavior;
- tests or benchmark cases for custom numerical paths.

The code-quality lens flags opacity, missing checks, unsafe defaults, or
unreviewable machinery. It does not decide whether an estimand, sample rule,
estimator, inference choice, or claim is economically correct. Those decisions
belong to their canonical lenses.

## Model computation

Match verification to the object: dimensions and indexing; convergence,
residual, feasibility, or market-clearing checks; mass conservation and
accounting identities; deterministic simulations; transparent small-grid
benchmarks; analytical limits; or known special cases.

## Performance

Performance advice is off by default. It is in scope only when requested, when
the code is reusable machinery, or when profiling, runtime, memory, scale, or
bottleneck evidence exists. Preserve transparency and the mathematical object.
