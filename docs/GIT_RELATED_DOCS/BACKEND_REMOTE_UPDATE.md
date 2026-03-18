# Backend Remote Update: Team Discussion & Decision Guide

**Date:** March 11, 2026  
**Branch:** Rebecca-Gautreaux-Work-Branch  
**Upstream Source:** https://github.com/QuiHu/Team6Project.git  

---

## Context

Our `backend/` directory was built on top of the original Team6Project (RiskRadar) codebase. To ensure we stay current with any upstream fixes, improvements, or additions in that source repository, we need to decide as a team how to handle synchronization.

This document outlines the available options, their trade-offs, and the recommended approach given our CMPS 357 extensions.

## Related Project Documentation

- Requirements and scope: [INSTRUCTIONS.md](./INSTRUCTIONS.md)
- Stage plan and implementation boundaries: [STAGES.md](./STAGES.md)
- Task/evidence tracker: [TODO.md](./TODO.md)
- Top-level status summary: [../README.md](../README.md)

---

## Step 1: Add the Upstream Remote (Required for All Options)

Before evaluating or applying any changes, fetch the upstream repository:

```bash
git remote add team6 https://github.com/QuiHu/Team6Project.git
git fetch team6
```

> If the remote already exists, skip the `add` step and just run `git fetch team6`.

---

## Step 2: Review Differences Before Committing to Anything

```bash
# List commits in team6/main that are not in our branch
git log HEAD..team6/main --oneline -- backend/

# See a full file-level diff of the backend directories
git diff HEAD team6/main -- backend/
```

**This step is critical.** Our `backend/` contains CMPS 357-specific additions that may not exist in the upstream repo, including:
- `db/migrations/2026-03-03_mariadb_scraper_alignment.sql`
- CMPS 357 test files under `tests/`
- Extensions planned in `docs/STAGES.md`

Reviewing the diff first prevents accidental overwrites.

---

## Option A — Full Backend Overwrite (Highest Risk)

Copy all files from `team6/main` directly into our `backend/`:

```bash
git checkout team6/main -- backend/
```

**Pros:**
- Guaranteed to be fully in sync with upstream
- Simple, one command

**Cons:**
- **Overwrites all of our custom additions** without warning
- Any CMPS 357-specific code (new scrapers, migration files, test setup) would be lost unless carefully re-applied afterward
- High risk of breaking the project

**Verdict:** ⚠️ Not recommended unless we are certain the upstream has no overlap with our work.

---

## Option B — Selective File Copy (Recommended for Targeted Updates)

Manually copy only the specific files we know have changed in upstream:

```bash
# Example: update only a specific scraper
git checkout team6/main -- backend/scrapers/nws_scraper.py

# Example: update only the database models
git checkout team6/main -- backend/db/models.py
```

**Pros:**
- Full control over what is updated
- Minimizes risk of overwriting our custom code
- Easy to review and test incrementally

**Cons:**
- Requires reviewing the diff output from Step 2 first
- More manual effort than a full merge

**Verdict:** ✅ Recommended for most cases. Review the diff, identify changed upstream files, and cherry-pick only what we need.

---

## Option C — Cherry-Pick Specific Commits (Recommended for Bug Fixes)

If the upstream repo made a specific fix or improvement, apply only that commit:

```bash
# Find the relevant commit hash from upstream
git log team6/main --oneline -- backend/

# Apply it to our branch
git cherry-pick <commit-hash>
```

**Pros:**
- Preserves our history cleanly
- Brings in a specific fix without touching unrelated files
- Conflict resolution is scoped to a single commit

**Cons:**
- Requires identifying the right commit manually
- Cherry-pick conflicts are still possible if our code has diverged significantly

**Verdict:** ✅ Recommended when a specific known fix or feature needs to be pulled in.

---

## Option D — Subtree Merge (Most Complete, Most Complex)

Merge the full upstream branch using a subtree strategy:

```bash
git merge -s subtree --allow-unrelated-histories team6/main
```

**Pros:**
- Full history from upstream is preserved
- All upstream changes are integrated in one step

**Cons:**
- Merges the **entire upstream repo**, not just `backend/`
- High likelihood of merge conflicts across unrelated files (e.g., frontend, docs)
- Requires careful conflict resolution

**Verdict:** ⚠️ Only appropriate if we want a comprehensive sync of the entire upstream repository. Not recommended for a targeted backend-only update.

---

## Most Optimal Option: B + C Combined

**Short answer: Use Option B (Selective File Copy) as the default, and Option C (Cherry-Pick) when a specific upstream commit addresses a known bug or feature.**

Here is why this combination is the best fit for our situation:

### Why not Option A?
A full overwrite is the fastest path to sync but the most destructive. Our `backend/` is not a clean fork — it has CMPS 357-specific migrations, test infrastructure, and planned extensions. A one-command overwrite would silently erase all of that with no guardrails. The time saved is not worth the recovery risk.

### Why not Option D?
A subtree merge pulls in the *entire* upstream repository history, including their frontend, docs, and any other non-backend files. Resolving those conflicts in unrelated files wastes team time and introduces noise into our commit history. It also does not limit the merge scope to `backend/` only.

### Why Option B is the right default
Option B gives us **surgical precision**. After reviewing the diff output (Step 2), we can identify exactly which upstream files changed and copy only those — one file at a time if needed. This means:

- Our CMPS 357 additions are never implicitly overwritten
- Each change is explicit and reviewable before it is applied
- The test suite can be run after each file update to catch breakage early
- Any team member can perform it without needing deep Git expertise

This is the lowest-risk, highest-control path for a project where our local changes and the upstream changes may overlap in the same files.

### When to use Option C instead
If the diff review (Step 2) reveals that an upstream change is contained within a **single, well-scoped commit** — for example, a bug fix to `nws_scraper.py` in one commit — then cherry-picking that commit is cleaner than manually copying the file. Cherry-pick preserves the upstream commit message and authorship in our history, which is useful for traceability.

**Use Option C when:** the upstream change is one commit, touches a limited set of files, and does not conflict with our additions.  
**Use Option B when:** the upstream change spans multiple commits, or only part of a changed file should be adopted.

### Summary

| Situation | Recommended Option |
|---|---|
| Default case (periodic sync check) | **Option B** — selective file copy |
| Single upstream bug fix in a clean commit | **Option C** — cherry-pick |
| Comprehensive upstream refactor | Discuss as a team before proceeding |
| Urgent full reset to upstream state | **Option A** — only as a last resort |

---

## Recommended Workflow for the Team

1. **One team member** runs the setup and diff steps:
   ```bash
   git remote add team6 https://github.com/QuiHu/Team6Project.git
   git fetch team6
   git diff HEAD team6/main -- backend/ > backend_diff.txt
   ```

2. **Share `backend_diff.txt`** with the team for review (or walk through it together).

3. **Decide together** which files (if any) need to be updated using the option that best fits each change:
   - Minor fix in an existing file → **Option B or C**
   - No changes needed → No action required
   - Major upstream refactor → **Discuss and plan before proceeding**

4. **After any changes**, run the test suite to confirm nothing is broken:
   ```bash
   cd backend
   python -m pytest -v
   ```

5. **Keep the remote** for future periodic checks:
   ```bash
   git fetch team6
   git diff HEAD team6/main -- backend/
   ```

---

## Files Most Likely to Have Upstream Changes

Based on the known project structure, these backend files are the most likely candidates for upstream updates:

| File | Description |
|---|---|
| `backend/scrapers/nws_scraper.py` | NWS data scraper |
| `backend/scrapers/airnow_scraper.py` | AirNow data scraper |
| `backend/scrapers/epa_scraper.py` | EPA data scraper |
| `backend/scrapers/firms_scraper.py` | FIRMS wildfire scraper |
| `backend/db/models.py` | Database models |
| `backend/llm/summarizer.py` | LLM summarization pipeline |
| `backend/api/alerts.py` | Alerts API |
| `backend/config/sources.yaml` | Scraper source configuration |

---

## Decision Required from Team

Please discuss and agree on:

1. **Do we need to sync at all right now?** (Review the diff output first)
2. **If yes, which option do we use?** (Option B or C are recommended)
3. **Who will perform the update and run tests?**
4. **How often should we check for upstream changes going forward?**
