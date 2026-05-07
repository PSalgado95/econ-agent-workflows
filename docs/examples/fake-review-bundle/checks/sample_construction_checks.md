# Sample Construction Checks

## Key Checks

| Check | Fake Result |
| --- | --- |
| County-year key uniqueness before merge | pass |
| Policy-date key uniqueness before merge | pass |
| Duplicate county-year rows after merge | 0 |

## Merge Accounting

| Stage | Rows |
| --- | ---: |
| Raw county-year panel | 1,000 |
| After policy-date merge | 1,000 |
| After dropping missing county identifiers | 995 |
| Final fake analysis sample | 995 |

## Missingness

| Variable group | Fake Missing Count | Rule |
| --- | ---: | --- |
| County identifier | 5 | drop |
| Year | 0 | keep |
| Outcome placeholder | 12 | keep for descriptive missingness table |
| Policy date | 400 | code as never-treated |

## Review Notes

This file is intentionally small. A real bundle should include generated checks or logs, not hand-written toy tables.
