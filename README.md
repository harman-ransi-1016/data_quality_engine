# Git Project 2 — Data Quality Engine (Python → Snowflake)

A small, config-driven data-quality checker: declare checks in YAML, run them against
Snowflake tables, get a pass/fail report. It's a **standalone Python version of dbt
tests** — same ideas (not_null, unique, accepted_values, row-count, freshness), but as
its own tool you could run from CI or an orchestrator against any table.

Ties to your dbt/Snowflake work: point it at your `*_SRC` sources or `DBT_CRANSI` models
and it validates them the same way dbt tests do.

This repo is also the vehicle for **Git Project 2** — see `GIT_EXERCISE.md`.

## What it does
- Reads `checks/checks.yml` (declarative checks per table/column).
- Runs each check as a SQL query against Snowflake.
- A check **fails** if its query returns offending rows / breaches a threshold.
- Prints a summary report (and exits non-zero if any check fails — so CI can gate on it).

## Supported checks
| check | meaning |
|-------|---------|
| `not_null` | column has no NULLs |
| `unique` | column has no duplicate values |
| `accepted_values` | column only contains an allowed set |
| `row_count_min` | table has at least N rows |
| `freshness` | max(timestamp col) is within N hours |

## Structure
```
data_quality_engine/
├── README.md
├── requirements.txt
├── .env.example
├── .gitignore
├── checks/
│   └── checks.yml        # declarative checks (what you edit to add coverage)
├── src/
│   ├── db.py             # Snowflake connection
│   ├── checks.py         # one function per check type (returns a Result)
│   ├── runner.py         # loads config, runs checks, collects results
│   └── report.py         # formats the summary
├── main.py
└── GIT_EXERCISE.md
```

## Setup & run
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env       # fill in Snowflake creds
python main.py             # run all checks
python main.py --fail-fast # stop at first failure
```
Exit code is non-zero if any check fails (gate a CI job on it).
