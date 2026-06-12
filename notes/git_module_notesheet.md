# Git Module — Notesheet (DE Academy)

Quick reference for the 10-item git module. Skim 1–6 (review), focus on 7–8 (rebase/squash)
and the two projects. Keep this open while working.

---

## 1. Why git
Version control: full history, branches, rollback, and collaboration without overwriting
each other. `main` = source of truth; branches = isolated workspaces (your "blast radius").

## 2. Install (Mac)
```bash
git --version            # confirm it's installed
xcode-select --install   # or: brew install git  (if missing)
git config --global user.name  "Your Name"
git config --global user.email "you@example.com"   # one-time identity setup
```

## 4. Create / clone a repo
```bash
git init                 # make the current folder a git repo
git clone <url>          # copy a remote repo locally
```

## 5. The everyday workflow
```bash
git status               # what's changed
git add <file>           # stage a change   (git add .  = stage everything)
git commit -m "msg"      # snapshot the staged changes
git push                 # upload commits to remote
git pull                 # download + merge others' commits
```
Mental model: **working dir → (add) → staging → (commit) → local repo → (push) → remote.**
The dbt IDE "commit and sync" button = add + commit + push.

## 6. Branching
```bash
git checkout -b feature/x   # create + switch to a branch
git switch main             # (newer syntax) switch branches
git merge feature/x         # bring a branch's work into the current branch
git branch -d feature/x     # delete a merged branch
git branch                  # list branches
```
`main` stays clean; do work on a branch; merge when ready. (= the dbt loop.)

---

## Repos vs branches, merge vs PR, protection (key clarifications)
- **Separate repos** = separate codebases that evolve independently (main app, microservices, landing page). Different *thing* → new repo.
- **Branches** = parallel versions of the *same* codebase (feature work, or environment branches like Amplify `main`/`demo` → different deploys). Same thing, different state → branch.
- Branch name `feature/add-sales`: the `/` is cosmetic (groups in the UI), NOT "under main." All branches still start from main. Conventions: `feature/`, `bugfix/`, `hotfix/`, `chore/`. One branch per unit of work, deleted after merge.
- **`git merge` + `git push`** = goes STRAIGHT into main, **no PR**. A **PR** is the other route: push the branch (unmerged), open the PR yourself on GitHub, merge there after review. Never automatic. They're two different paths, not a sequence.
- **Branch protection rules** (repo settings) lock `main`: require a PR, require approvals, require CI to pass, restrict who can push. On a protected repo a direct push to main is REJECTED → PR is enforced. Personal repos are unprotected by default (direct push works). Separately, deploy hooks (Amplify) react AFTER something lands in main — protection controls entry, deploy reacts.

## 7. Rebasing  ⭐ NEW
Replays your branch's commits **on top of** another branch's latest state.

```bash
git fetch origin
git rebase origin/main      # move my commits to sit on top of latest main
git rebase --continue       # after resolving a conflict
git rebase --abort          # cancel, restore pre-rebase state
```

**Rebase vs merge:**
| | result | history |
|---|---|---|
| `git merge main` | pulls main in, makes a **merge commit** | branches + rejoins (diamond) |
| `git rebase main` | replays your commits **on top of** main | **linear** (straight line) |

**Golden rule:** only rebase commits that are **yours and not yet pushed/shared.**
Rebasing public history rewrites it under everyone who already pulled it. Branch cleanup = safe.

## 8. Squashing  ⭐ NEW
Collapse several messy WIP commits into one clean commit (a use of interactive rebase).

```bash
git rebase -i HEAD~3        # interactive, last 3 commits
```
In the editor: keep the **first** line `pick`, change the rest to `squash` (`s`). Save,
then write one combined commit message. `git log --oneline` now shows one commit.

- Do it **before** opening the PR — one commit = one logical change, easy to review/revert.
- If you already pushed: `git push --force-with-lease` (your branch only, never shared).

## Merge conflicts (you'll hit these during rebase/merge)
Two branches edited the **same lines**. Not an error — git asks *you* to choose.
```
<<<<<<< HEAD
    their version
=======
    your version
>>>>>>> your-commit
```
Edit the file to the result you want, **delete the `<<<`, `===`, `>>>` markers**, save, then:
```bash
git add <file>
git rebase --continue        # (or git commit, if you were merging)
```
`git merge --abort` / `git rebase --abort` bails out cleanly.

---

## Cheat sheet
```
git checkout -b <b>            create + switch branch
git add <f> / git add .       stage
git commit -m "msg"           commit   (git commit -am = stage tracked + commit)
git push / git pull           sync with remote
git merge <b>                 combine a branch in (merge commit)
git rebase origin/main        replay your branch on latest main (linear)
git rebase -i HEAD~N          squash/reorder last N commits
git rebase --continue/--abort after conflict / to cancel
git push --force-with-lease   push rewritten history safely (own branch only)
git log --oneline             compact history
```
**Rule of thumb:** merge to combine shared work; rebase to tidy your own branch before sharing.

---

## 9–10. The two projects
- **`git_project_1_etl_pipeline/`** — Python EL → Snowflake raw (feeds your dbt sources).
  Practice: branch + PR → squash → rebase onto updated main. See its `GIT_EXERCISE.md`.
- **`git_project_2_data_quality_engine/`** — config-driven DQ checks vs Snowflake
  (dbt-tests-as-Python). Practice: add a check → squash → **resolve a merge conflict**.
  See its `GIT_EXERCISE.md`.

Use the repos as the *thing you branch and rebase on* — real code beats toy commits.

---

## One-line summaries to remember
- **commit** = snapshot. **branch** = parallel line of work. **merge** = join two lines.
- **rebase** = move your line to start from a newer point (linear history).
- **squash** = combine several commits into one.
- **conflict** = two edits to the same lines; you pick the winner.
- Never rewrite (rebase/squash + force) history that's already shared on `main`.
