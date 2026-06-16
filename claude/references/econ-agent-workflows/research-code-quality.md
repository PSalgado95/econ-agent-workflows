<!-- GENERATED FROM CODEX SOURCE - DO NOT EDIT. Edit the Codex sources (skills/, .codex/agents/, references/) and run build_claude.py. -->

# Research Code Quality

This standard applies when code is part of an economics research object: data construction, estimation, simulation, calibration, model solving, numerical routines, reusable research tooling, or code-generated outputs. It does not keep pure app, API, UI, infrastructure, or general software work inside the economics workflow.

The purpose is research trust. Code quality matters here when it makes a research object easier to read, check, rerun, modify, or hand to another researcher. Do not turn this into a style guide. Suppress preferences that have no consequence for interpretation, rerun safety, reviewability, or future modification.

## Code Role

Use the lightest role that honestly fits the task.

- `none`: no code is being written, changed, inspected, or used as evidence.
- `exploratory`: scratch code for local inspection; keep the object legible, but do not require package structure.
- `analysis-pipeline`: code that creates data, outputs, tables, figures, estimates, model objects, or diagnostics used by the project.
- `shared-collaborator`: code another collaborator is expected to read, rerun, or edit.
- `replication-facing`: code that supports an external replication, review bundle, or publication-facing handoff.
- `library-tool`: reusable research machinery, model code, helper packages, APIs, or command-line tools whose behavior other work depends on.

## Always-On Floor

Whenever research code is written or changed, the first pass should satisfy this floor unless the task is explicitly throwaway exploration:

- use descriptive names for research objects, samples, variables, model components, and outputs;
- make the entrypoint visible;
- keep object-defining parameters named rather than buried as magic numbers;
- separate analytical logic from formatting, plotting polish, and report rendering when practical;
- delete stale commented-out code, temporary prints, scratch plots, and ad hoc debug fragments from tracked research code;
- add assertions or equivalent checks for object-defining facts;
- leave enough rerun information that another agent or collaborator can see what command, script, notebook, or workflow created the reviewed object.

## Assertions and Tests

A passing script run is not enough for substantial research code. Protect object-defining facts close to where they are created.

Use inline assertions or language equivalents for local invariants such as:

- row counts, unique keys, merge cardinality, support bounds, and denominators;
- treatment, exposure, timing, sample, or weighting definitions;
- array, matrix, panel, or state-space dimensions;
- convergence, residuals, feasibility conditions, accounting identities, or mass conservation;
- output freshness, expected file counts, and one-row-per-unit assumptions.

Use named tests when checks are reusable, collaborator-facing, replication-facing, library-like, or protect a bug that should not recur. Do not require a full test suite for every exploratory script, but do not bury durable checks inside production functions as temporary debug code.

## Data and Construction Code

For data and sample construction, readable code makes the transformation legible. An abstraction that hides a filter, merge, sample restriction, denominator, timing rule, weighting rule, or variable definition is a code-quality problem even if the abstraction looks tidy.

The code-quality lens may flag missing assertions or hidden logic, but it should not decide whether the transformation, sample, estimator, or inference choice is substantively correct.

## Notebooks

Notebook exploration is fine. Notebook state should not be the only durable record when code will be reused, reviewed, promoted, or handed to someone else.

Promote durable logic, reusable helpers, model routines, data transformations, and repeatable checks into scripts or modules when the code role warrants it. Keep notebooks as inspection, exposition, or orchestration surfaces rather than the only location where the research object exists.

## Model Computation

For model-computation objects, the primary object is a solver, simulation, calibration routine, numerical method, estimation machine, computational model object, or reusable research tool.

Verification should match the object. Depending on the task, use checks such as:

- dimensions and indexing consistency;
- convergence, residual, feasibility, or market-clearing checks;
- mass conservation, law-of-motion, accounting, or aggregation identities;
- deterministic simulation checks;
- small-grid or transparent benchmark cases;
- comparison to an analytical limit, baseline object, or known special case;
- rerun determinism when deterministic output is expected.

Do not force empirical-rerun language onto model-computation work. A full computational run can be the right execution mode.

## Performance

Correct, transparent code comes first. Performance advice is off by default for ordinary data cleaning, note writing, and one-off analysis code.

Performance guidance is in scope only when the user asked for it, the code role is `library-tool`, or there is profiling, runtime, memory, scale, bottleneck, or repeated-work evidence. In those cases, prefer:

- profiling or timing before optimization;
- small transparent benchmarks before optimized paths;
- avoiding repeated expensive work when the repeated object is the same;
- using sparse, structured, vectorized, compiled, cached, or precomputed operations only when they preserve the mathematical object and remain reviewable.

## Reviewer Guardrails

The research-code-quality reviewer should:

- report only defects with a readability, rerun, modification, reviewability, or research-trust consequence;
- prefer small local improvements over broad refactors;
- suppress pure style nits;
- avoid language-preference claims;
- avoid performance advice without performance-sensitive scope or bottleneck evidence;
- route pure software work away from the economics workflow;
- avoid duplicating provenance, transformation/sample, specification, inference, robustness, reproducibility, software-equivalence, cross-language-validation, hybrid-implementation, or bundle findings.
