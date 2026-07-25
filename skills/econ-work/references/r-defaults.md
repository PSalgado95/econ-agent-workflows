# R Defaults

Applies when writing or editing R for research: data construction, panels, estimation, and figures. This file is mostly tool selection, not taste. The general code standard for naming, provenance, pruning, comments, and tests lives in `research-code-quality.md` and is not restated here.

## Package defaults

| Job | Default | Why this one |
|-----|---------|--------------|
| Panel / fixed-effects regressions | `fixest` | Econ-native: fast high-dimensional fixed effects, clustered standard errors, and `etable` for output. |
| Data of real size on disk | `arrow` (Parquet) + `duckdb` + `DBI` | Push filtering, joins, and aggregation into the query layer; materialize only the analysis slice into R memory. Never load-then-filter a file that is large enough to make that wasteful. |
| Reading SAS / Stata sources | `haven` | Read once, convert to typed Parquet at the curation boundary, then work from Parquet. |
| In-memory wrangling | per-project dialect, declared once | `data.table` when the slice is large or speed matters; `dplyr` when readability dominates. Never mix `%>%`, `|>`, and `[.data.table]` idioms in one script. State the project's choice at the top of the project, not per script. |
| Pipes | native `|>` | No extra dependency. Keep `%>%` only where a project already standardized on it. |

Spark and `sparklyr` are out of scope by default: they target distributed cluster pipelines maintained by an IT team, not ordinary single-server research work. DuckDB covers most single-server research scale.

## The large-data pattern

For any dataset big enough that a full in-memory read is wasteful:

1. **Inspect** a sample of the source files first: delimiters, encodings, types, and format changes across years.
2. **Convert once** to typed, compressed Parquet. This is the curation boundary. The provenance ladder's heavy checks live here: row counts by source file or year, key uniqueness, expected columns, and type coercions made explicit. Add a short metadata note with columns, types, units, and availability.
3. **Query through the layer** with `arrow::open_dataset()` plus dplyr verbs, or DuckDB SQL via `DBI`, whichever reads clearer for the operation. Filtering and aggregation happen on disk.
4. **Materialize the slice** with `collect()` only when it is analysis-ready, then hand it to `fixest` or the project's wrangling dialect.

Downstream of the conversion, the Parquet is self-authored data: one thin boundary check, then straight to the economics. Do not re-validate fields the conversion already typed.

## R idioms

- Joins always name their keys: `left_join(a, b, by = c("pnr", "year"))`; never positional or implicit.
- Handle missing values explicitly at the point they matter; do not let `NA` semantics ride through silently.
- Write a function when a transformation repeats; do not wrap a one-off cleaning step in a function or config object.
- Scripts declare their inputs and outputs near the top; a reader should see what the script consumes and produces without scrolling.

## Tests with testthat

Use `testthat` for checks worth re-running, saved under `tests/testthat/` so they outlive the session. Worth a named test:

- data invariants after a build step: row counts, key uniqueness, expected columns, support bounds;
- a derived aggregate checked against a hand-computed value;
- a bug that already bit once and should not recur.

Not worth a named test: glue code, one-off exploration, or formatting. Inline `stopifnot()` at the point of construction is often enough for local invariants; promote to a named test when the check is durable or collaborator-facing.
