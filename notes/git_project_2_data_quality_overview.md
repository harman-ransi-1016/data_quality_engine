# Git Project 2 — Data Quality Engine: Overview & Context

Context document for the second git build project. What it is, how it's built, how it ties
to the dbt work, and the git skills practiced (round-two reps).

---

## What this project is
A small, **config-driven data-quality checker** in Python. You declare checks in YAML, it
runs each as a SQL query against Snowflake tables, and prints a pass/fail report. Exits
non-zero if anything fails, so it can gate a CI job.

It is essentially **dbt tests rebuilt as a standalone tool** — the same assertions
(`not_null`, `unique`, `accepted_values`, `row_count_min`, `freshness`, `max_value`) but
runnable independently against any table, not tied to the dbt framework.

## Where it runs (important)
- The **Python runs on your laptop** (terminal / VS Code).
- It **connects to Snowflake** via the connector + `.env` creds and queries your tables.
- Snowflake is just the **data source it inspects** — you do NOT write this in Snowflake.
```
Python (laptop) ──connects──► Snowflake ──runs check SQL──► returns numbers ──► pass/fail report (terminal)
```

## How it works (architecture)
- `checks/checks.yml` — declarative checks (table, type, column, thresholds). Add coverage
  by adding YAML entries.
- `src/checks.py` — one function per check type; each runs a SQL query and returns a Result
  (pass if 0 offending rows / threshold met). A `REGISTRY` dict maps check name -> function.
- `src/runner.py` — loads the config, runs each check.
- `src/report.py` — formats the results table.
- `src/db.py` — Snowflake connection from `.env`.
- `main.py` — entry point; `--fail-fast` stops at first failure; non-zero exit on any fail.

## Three layers (the mental model this project teaches)
- **Your Python** = the brain — defines checks, decides pass/fail.
- **Snowflake** = data + SQL executor — runs the queries, returns numbers.
- **dbt** = a framework that automates this same pattern. This project shows the *mechanism*
  behind dbt tests: an assertion is just a SQL query that returns offending rows.

## Real results from the live run (your data)
```
PASS  CUSTOMER_SRC  not_null(CUSTOMER_ID)
PASS  CUSTOMER_SRC  unique(CUSTOMER_ID)
PASS  CUSTOMER_SRC  row_count_min(1)            5 rows
PASS  PURCHASE_SRC  accepted_values(STATUS)
FAIL  CUSTOMER_SRC  freshness(CREATED_AT)       360h old (limit 24h)
FAIL  SALES_SRC     max_value(TOTAL_AMOUNT<=100) 1 row over 100 (the 124.95 sale)
```
Both FAILs are the tool working correctly: the source data was ~15 days old (stale), and one
sale exceeded the $100 threshold. Real findings, not bugs.

## Functionality added during the exercise
- **`max_value` check** — new check type: a numeric column must stay <= a threshold. Added a
  `check_max_value` function, registered it in `REGISTRY`, and wired a YAML entry. This was
  the Exercise-A feature work (real code, not just a git rep).

## Git skills practiced (round-two reps)
- **Feature branch + PR** — added `max_value` on `feature/max-value-check`, PR, merge, cleanup.
- **Squashing** — 3 messy commits collapsed into one with `git rebase -i`.
- **Merge conflict** — `main` and a branch each set `max_age_hours` differently (12 vs 48),
  hit a CONFLICT on `git merge`, resolved in the VS Code merge editor, committed the merge.

## Friction hit (and the lessons — reinforced from Project 1)
- **Pushed before committing** — `git push` showed `Total 0` and GitHub said "up to date
  with main" because the changes were never committed. Lesson: commit THEN push.
- **"Already up to date" on merge** — the conflict wouldn't trigger because the `12` commit
  on `main` hadn't actually been made (edit not saved before `commit -am`). Lesson: a merge
  conflict needs two branches with *real, committed* changes to the same line.
- **`origin` clarified** — `origin` = the remote GitHub repo (a name for the URL), NOT "main"
  and NOT local. `git push origin <branch>` pushes that branch to the remote; `main` only
  changes via a merged PR. Conflicts are a LOCAL merge thing — no remote involved.
- **`commit --amend`** — rewrites the most recent commit (fix message / add forgotten file)
  instead of adding a new one. Only on unshared commits.

## How to run it
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env       # fill in Snowflake creds (DBT_PROD_USER)
python main.py             # run all checks -> pass/fail report
python main.py --fail-fast # stop at first failure
```

## Status
Project 2 complete — functional DQ engine (with the added `max_value` check) on GitHub,
plus full git exercises (branch/PR, squash, merge conflict) done as round-two reps.
Both git build projects (ETL pipeline + DQ engine) finished. Could be extended later
(more check types, richer reporting, scheduled CI runs) as a portfolio piece.
