# Git Exercise — Project 2 (Data Quality Engine)

Second repo to practice git on. Project 1 covered branching / squash / rebase basics —
here you add **a new check type** while practicing the same flow plus **a deliberate
merge conflict** so you learn to resolve one.

## Setup (one time)
```bash
cd git_project_2_data_quality_engine
git init && git add . && git commit -m "Initial commit: data quality engine"
# create empty GitHub repo data_quality_engine (no README), then:
git remote add origin git@github.com:<you>/data_quality_engine.git
git branch -M main && git push -u origin main
```

---

## Exercise A — Add a new check type, clean branch + PR
Goal: add a `max_value` check (column must be <= a threshold).

```bash
git checkout -b feature/max-value-check
```
1. In `src/checks.py`, add a `check_max_value(conn, c)` function and register it in `REGISTRY`.
2. Add a check entry to `checks/checks.yml` using it.
3. Commit in logical steps:
```bash
git add src/checks.py
git commit -m "Add max_value check implementation"
git add checks/checks.yml
git commit -m "Wire max_value check into config"
git push -u origin feature/max-value-check
```
4. PR → review → merge → clean up (`git checkout main && git pull && git branch -d feature/max-value-check`).

---

## Exercise B — Squash before merging
You made 2 commits in Exercise A. Practice collapsing them into one *before* the PR next time:
```bash
git rebase -i HEAD~2
# mark the 2nd as `squash`, write one message: "Add max_value check"
```
`git log --oneline` → one commit. Squashing keeps `main` history readable: one commit =
one logical change, not a trail of WIP.

---

## Exercise C — Create + resolve a MERGE CONFLICT (NEW, the key skill)
Conflicts happen when two branches edit the same lines. Force one on purpose:

1. On `main`, edit the `freshness` row's `max_age_hours` in `checks/checks.yml` to `12`,
   commit, push.
2. Make a branch from an OLDER main and edit the **same line** to `48`:
```bash
git checkout -b feature/freshness-window
# edit the same freshness max_age_hours to 48
git commit -am "Loosen freshness window to 48h"
```
3. Now try to bring main's change in:
```bash
git fetch origin
git rebase origin/main      # (or: git merge origin/main)
```
Git stops with a CONFLICT in `checks.yml`. Open it — you'll see:
```
<<<<<<< HEAD
    max_age_hours: 12
=======
    max_age_hours: 48
>>>>>>> (your commit)
```
4. **Resolve**: edit the file to the value you actually want, delete the
   `<<<<<<<`, `=======`, `>>>>>>>` markers, save. Then:
```bash
git add checks/checks.yml
git rebase --continue        # (or `git commit` if you used merge)
```
Conflict resolved. (`git rebase --abort` bails out if you want to start over.)

**The lesson:** a conflict isn't an error — it's git asking *you* to decide which change
wins when two edits touch the same lines. The markers show both sides; you pick/blend.

---

## Cheat sheet (conflict + rebase)
```
git rebase origin/main          # replay your work on latest main (may conflict)
# ... fix conflicted files ...
git add <file>
git rebase --continue           # proceed after resolving
git rebase --abort              # cancel, back to pre-rebase state
git merge origin/main           # alternative: creates a merge commit
git push --force-with-lease     # push rewritten history (your branch only)
```
Rule: **merge = combine shared branches (safe, keeps history). rebase = tidy/replay your
own branch before sharing (linear history, never on public commits).**
