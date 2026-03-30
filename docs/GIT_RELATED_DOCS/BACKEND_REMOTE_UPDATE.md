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

---

# 2026 Team6 Backend Sync Review & Action Plan

## Summary of Team6 Changes

The Team6 backend has diverged significantly from this project, with major changes in:
- API endpoints (alerts, location, risk)
- Database models
- Scrapers (NWS, AirNow, EPA, FIRMS, generic)
- Services (alert prioritization, risk scoring)
- Security/authentication
- Configuration and templates
- Test coverage

**A full overwrite or subtree merge is NOT recommended.** The safest approach is targeted, file-by-file review and selective merging (Option B/C), as outlined below.

---

## Team6 Improvements: Merge Recommendation Table

| File/Area                          | Likely Team6 Improvements                | Recommended Action for Merge/Update                | Notes/Feature Examples                        |
|-------------------------------------|------------------------------------------|---------------------------------------------------|-----------------------------------------------|
| backend/api/alerts.py               | Bug fixes, new endpoints, logic updates  | Review and merge relevant changes                 | Improved alert handling, new API features     |
| backend/api/location.py             | New/updated location logic               | Merge if you need location-based features         | Geo features, location filtering              |
| backend/api/risk.py                 | Risk calculation improvements            | Merge if risk logic is better or more robust      | More accurate risk scoring                    |
| backend/db/models.py                | Schema changes, optimizations            | Merge if compatible with your DB and features     | New fields, better relationships              |
| backend/services/alert_prioritization.py | Improved prioritization algorithms     | Merge logic improvements, test thoroughly         | More relevant alerts surfaced                 |
| backend/services/risk_scoring.py    | Enhanced scoring logic                   | Merge if scoring is more accurate or flexible     | Customizable scoring, bug fixes               |
| backend/scrapers/nws_scraper.py     | Scraper bug fixes, new data fields       | Merge for better data coverage                    | More robust NWS data                          |
| backend/scrapers/airnow_scraper.py  | Scraper improvements                     | Merge for better air quality data                 | Expanded data, error handling                 |
| backend/scrapers/epa_scraper.py     | Scraper improvements                     | Merge for better EPA data                         | New pollutants, better error handling         |
| backend/scrapers/firms_scraper.py   | Scraper improvements                     | Merge for better wildfire data                    | More accurate fire alerts                     |
| backend/scrapers/generic_api_scraper.py | API scraping improvements              | Merge if you use generic APIs                     | Broader data source support                   |
| backend/llm/summarizer.py           | Summarization pipeline updates           | Merge for better summaries                        | Improved LLM prompts, summary quality         |
| backend/config/settings.py          | New settings, bug fixes                  | Merge if settings are relevant                    | More flexible configuration                   |
| backend/config/sources.yaml         | New/updated data sources                 | Merge for more/better data                        | Additional sources, updated endpoints         |
| backend/auth/security.py            | Security patches, JWT, hashing           | Merge for improved security                       | Stronger auth, password handling              |
| backend/templates/base.html         | UI/UX improvements                       | Merge if you use web frontend                     | Better user experience                        |
| backend/templates/summaries.html    | UI/UX improvements                       | Merge if you use web frontend                     | Improved summary display                      |
| backend/schemas/user.py             | User schema updates                      | Merge if you need new user features               | More user fields, validation                  |
| backend/schemas/risk_score.py       | Risk score schema updates                | Merge if you use risk scoring                     | More detailed scoring                         |
| backend/tests/                      | New/updated tests                        | Merge to improve test coverage                    | More robust regression testing                |

---

## Step-by-Step Plan: Team6 Backend Sync & Feature Adoption

### Phase 1: Preparation & Prioritization
1. Assign team members to review specific backend areas (API, scrapers, models, services, config, templates, security, tests).
2. Commit and push all local changes to your branch.
3. Fetch latest Team6 changes and generate a fresh diff:
   - `git fetch team6`
   - `git diff HEAD team6/main -- backend/ > backend_diff.txt`
4. Use the markdown table above to prioritize files/areas with the most impactful or relevant changes.

### Phase 2: File-by-File Review & Merge
5. For each prioritized file/area:
   - Open the diff for that file (e.g., `git diff HEAD team6/main -- backend/api/alerts.py`).
   - Decide as a team whether to fully adopt, partially merge, or skip the upstream changes.
   - If adopting/merging:
     - Use `git checkout team6/main -- <file>` for full adoption.
     - For partial merges, use a visual diff tool (VS Code, meld, etc.) to manually integrate changes.
     - For single-commit bug fixes, use `git cherry-pick <commit-hash>`.
   - Resolve merge conflicts, preserving CMPS 357-specific features.
   - Document the decision and rationale for each file in a shared changelog (e.g., `docs/GIT_RELATED_DOCS/TEAM6_MERGE_LOG.md`).

### Phase 3: Testing & Validation
6. After each file or logical group of files is merged, run the backend test suite:
   - `cd backend`
   - `python -m pytest -v`
7. If tests fail, debug and resolve issues before proceeding.
8. Perform manual testing for features not covered by automated tests (e.g., UI, API endpoints).

### Phase 4: Finalization & Documentation
9. Once all desired changes are merged and tested, update project documentation to reflect new features or changes.
10. Summarize improvements adopted from Team6 in a team meeting or shared doc.
11. Push all changes to your remote branch and create a pull request for team review.
12. Plan periodic future syncs (e.g., monthly) to keep up with upstream improvements.

### Verification
- All automated tests pass after each merge step.
- Manual feature testing for new/changed endpoints, scrapers, and UI.
- Changelog is up to date and reviewed by the team.
- Team review and approval of the final merged branch.

### Further Considerations
- Assign a "merge lead" to coordinate the process and resolve disputes.
- Consider feature branches for risky merges.
- Schedule a team review meeting after major merges for shared understanding.
