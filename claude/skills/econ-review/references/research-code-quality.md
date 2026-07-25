<!-- GENERATED FROM CODEX SOURCE - DO NOT EDIT. Edit the Codex sources and run build_claude.py. -->

# Research Code Quality

This standard applies when code is part of an economics research object: data construction, estimation, simulation, calibration, model solving, numerical routines, reusable research tooling, or code-generated outputs. It does not pull pure app, API, UI, infrastructure, or general software work into the economics workflow.

The purpose is research trust. Code quality matters when it makes a research object easier to read, check, rerun, modify, or hand to another researcher. Do not turn this into a style guide. Suppress preferences that have no consequence for interpretation, rerun safety, reviewability, or future modification.

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

- name research objects, samples, variables, model components, and outputs for the economics rather than the plumbing; use paper notation when it is readable;
- match input checking to input provenance;
- make the entrypoint visible;
- keep object-defining parameters named rather than buried as magic numbers;
- separate analytical logic from formatting, plotting polish, and report rendering when practical;
- delete stale commented-out code, temporary prints, scratch plots, and ad hoc debug fragments from tracked research code;
- add assertions or equivalent checks for object-defining facts;
- leave enough rerun information that another agent or collaborator can see what created the reviewed object.

## Assertions and Tests

A passing script run is not enough for substantial research code. Protect object-defining facts close to where they are created: row counts, unique keys, merge cardinality, support bounds, denominators, timing, weighting, array dimensions, convergence, residuals, accounting identities, output freshness, expected file counts, and one-row-per-unit assumptions.

Use named tests when checks are reusable, collaborator-facing, replication-facing, library-like, or protect a bug that should not recur. Do not require a full test suite for every exploratory script, but do not bury durable checks inside production functions as temporary debug code.

## Provenance Ladder

How hard code should work to validate an input depends on where the input came from and what a check would protect. Checks on the wrong rung are a defect in both directions: missing checks on external data, and defensive ceremony on objects the project authored itself.

- **External or untrusted input**: validate properly and fail early with a clear message.
- **Restricted or expensive source data**: keep checks that catch a broken pull: row counts, key coverage, merge cardinality, and source receipts.
- **Self-authored workbook or config**: use one thin boundary check with an economist-facing error message. Do not re-validate every field on every read unless multiple independent producers edit the file.
- **Generated intermediate output**: check the economic or statistical object: sample size, group support, horizon coverage, key uniqueness, benchmark parity.
- **Internal helper code**: avoid wrappers, option flags, fallback routes, and type checks that serve hypothetical callers. When the source route is fixed, keep one narrow path.

The ladder never removes checks that protect a real result: benchmark parity, accounting identities, mass conservation, sample and merge diagnostics, and validators on publication-facing artifacts stay.

```python
# Bad: self-authored spec sheet treated as hostile input
spec = pd.read_excel(path)
for col in ["var", "lag", "horizon"]:
    if col not in spec.columns:
        raise KeyError(col)
if not np.issubdtype(spec.lag.dtype, np.integer):
    raise TypeError("lag must be int")
# ...many more checks before any economics

# Good: one boundary check, then the economics
spec = pd.read_excel(path)
assert {"var", "lag", "horizon"} <= set(spec.columns), spec.columns
for row in spec.itertuples():
    irf = run_lp(row.var, row.lag, row.horizon)
```

## Code Taste

Remove generality unless it earns its keep. Internal research code may assume local callers obey the repo's conventions. Delete thin wrappers that only rename arguments, one-off config objects, optional branches no current workflow uses, fallback routes kept after the source route was fixed, and hooks nobody asked for. Keep structure that encodes a real research choice or removes real duplication across variants.

```python
# Bad: a dataclass for values used once, carrying no invariant
@dataclass
class HouseholdConfig:
    beta: float = 0.96
    sigma: float = 2.0
    n_grid: int = 500

# Good: explicit locals where the values are chosen
def solve_baseline():
    beta, sigma = 0.96, 2.0
    grid = make_asset_grid(amin=0, amax=80, n=500)
    return solve_household(beta, sigma, grid)
```

Triage question: would removing this option, object, or branch change any current result, figure, table, or meaningful check? If not, remove it.

- Keep code scanable. Keep simple calls, signatures, dicts, and conditionals on one line when they stay readable. Prefer removing unnecessary arguments over reformatting a long call, especially keyword arguments that restate defaults. Repeated `f(x=x, y=y, z=z)` forwarding is a sign of the wrong interface.
- Comments explain reasoning. Keep comments that connect code to equations, explain ordering, flag data quirks, cite a source, or mark meaningful blocks. Delete comments that restate the next line. Avoid formal docstring boilerplate on internal helpers.
- Modules follow the research workflow. One module should have one substantive job: data construction, calibration or estimation, model solution, experiments, tables, or figures. Merge tiny modules that split one conceptual step across many files.
- Tests protect claims. Keep tests that check a proposition, identity, special case, residual, or data assumption the project relies on. Delete tests that only freeze glue code.

Before finishing an edit, scan the diff for defensive checks on the wrong provenance rung, exploded calls and restated defaults, one-use wrapper layers, boilerplate docstrings, dead branches and fallback routes, and names that put plumbing before economics.

## Data and Construction Code

For data and sample construction, readable code makes the transformation legible. An abstraction that hides a filter, merge, sample restriction, denominator, timing rule, weighting rule, or variable definition is a code-quality problem even if the abstraction looks tidy. The code-quality lens may flag missing assertions or hidden logic, but it should not decide whether the transformation, sample, estimator, or inference choice is substantively correct.
