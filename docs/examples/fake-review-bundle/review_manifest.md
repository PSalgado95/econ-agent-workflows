# Review Manifest

## Inputs

| Input | Role | Status |
| --- | --- | --- |
| `toy_raw_county_panel.csv` | fake raw panel input | not included |
| `toy_policy_dates.csv` | fake policy timing input | not included |

## Outputs

| Output | Role | Status |
| --- | --- | --- |
| `analysis_county_year_stub.csv` | fake constructed analysis file | represented by checks only |
| `key_outputs/descriptive_table_stub.md` | fake descriptive output | included |

## Diagnostic Surfaces

| Surface | Status |
| --- | --- |
| Source lineage | documented in `review_context.md` |
| Key uniqueness | documented in `checks/sample_construction_checks.md` |
| Merge cardinality | documented in `checks/sample_construction_checks.md` |
| Reason-coded drops | documented in `checks/sample_construction_checks.md` |
| Missingness | documented in `checks/sample_construction_checks.md` |
| Rerun status | documented in `build_info/rerun_status.md` |
| Model-spec ledger | not applicable; no realised estimates |
| Cross-language validation | not applicable; not requested |
