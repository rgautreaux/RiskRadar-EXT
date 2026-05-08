# Student Contributors

## Contributor Breakdown (grading branch)
| Name | Commit Count | Average Changes Per Commit | Estimated Contribution | Major Areas |
|---|---:|---:|---:|---|
| Rebecca Gautreaux | 448 | 653.9 | 94.3% | frontend/web + integration assets, documentation/transcripts, backend API/scoring updates |
| Max Compeaux | 50 | 357.2 | 5.7% | frontend UX (map/auth/profile/alerts), map styling/interactivity, packing/assistant-adjacent backend and docs |

## Notes on Attribution
- Scope: full `grading` branch history.
- Instructor identities were excluded from all calculations (`Nicholas Lipari, PhD`, `nicholas-g-lipari-phd`).
- Non-student automation accounts were also excluded from student attribution percentages.
- Alias normalization applied from commit metadata:
  - `rgautreaux` + `Rebecca Gautreaux` merged as **Rebecca Gautreaux**.
  - Max Compeaux commits from both personal and GitHub noreply emails merged as **Max Compeaux**.
- `Estimated Contribution` uses commit-history weighting: `commit_count × average_lines_changed_per_commit` (equivalent to each contributor's total lines changed), normalized across included students.

## Surviving-Code Proxy (commit-history only)
Because blame-level surviving-line attribution is unavailable, the table below uses a conservative proxy from commit history only.

| Name | Proxy Net Added Lines (Adds − Deletes, floored at 0) | Estimated Surviving-Code Share |
|---|---:|---:|
| Rebecca Gautreaux | 105,703 | 89.1% |
| Max Compeaux | 12,952 | 10.9% |

### Proxy Method
- For each contributor: sum all historical additions and deletions on `grading`.
- Compute `max(additions - deletions, 0)` as a rough surviving-code proxy (negative values imply a contributor removed more code than they added in this history window; we treat that as 0 surviving-line ownership instead of a negative share so normalization remains interpretable).
- Normalize proxy totals across included student contributors.
- This is an approximation for final attribution context; it is not equivalent to git-blame ownership.
