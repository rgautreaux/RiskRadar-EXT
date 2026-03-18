# Wireframe Style Implementation Plan

This document defines a role-based execution order to make the web app structurally and visually accurate to the RiskRadar web wireframes while using a hybrid icon strategy from the wireframe_icons directory.

## Standup Progress Tracker

Use this table for daily check-ins and updates.

| Workstream | Lane Owner | Secondary Owner | Start Date | Target Due Date | Status | Notes |
|---|---|---|---|---|---|---|
| Phase 0: Kickoff and Mapping | Rebecca | Max | 2026-03-17 | TBD | In Review | Rebecca tasks complete; awaiting Max co-review |
| Phase 1: Shared Foundation | Rebecca | Max | TBD | TBD | Not Started | Shared layout, global CSS patterns, hybrid icon foundation |
| Phase 2: Core Functional Page Parity | Max | Rebecca | TBD | TBD | Not Started | Dashboard, Alerts, Summaries, Profile, Login, Register, Risk |
| Phase 3: Scaffold and Detail Shell Parity | Max | Rebecca | TBD | TBD | Not Started | Map, Forecast, Assistant, Alert Detail, Summary Detail |
| Phase 4: Global Consistency and Signoff | Max | Rebecca | TBD | TBD | Not Started | QA/docs lead with rapid shared/layout fix support |

Recommended status values: Not Started, In Progress, Blocked, In Review, Completed.

## Objective

Achieve structural and visual cohesion across all web pages with:
- Wireframe-accurate section hierarchy and spacing rhythm
- Consistent icon usage from wireframe_icons
- Responsive behavior across desktop, tablet, and mobile
- No regression of existing Stage 1 working functionality

## Scope

In scope pages:
- Home Dashboard
- Alerts
- Summaries
- Profile
- Login
- Register
- Risk
- Map
- Forecast
- Assistant
- Alert Detail
- Summary Detail

Primary implementation files:
- frontend/web/components/layout.php
- frontend/web/public/assets/app.css
- frontend/web/views/dashboard.php
- frontend/web/views/alerts.php
- frontend/web/views/summaries.php
- frontend/web/views/profile.php
- frontend/web/views/login.php
- frontend/web/views/register.php
- frontend/web/views/risk.php
- frontend/web/views/map.php
- frontend/web/views/forecast.php
- frontend/web/views/assistant.php
- frontend/web/views/alert_detail.php
- frontend/web/views/summary_detail.php

Reference assets:
- wireframe_icons/RiskRadar_Web_Wireframes.png
- wireframe_icons/*

## Team Roles

Three parallel lanes are used:
1. Layout Lane
2. Page Templates Lane
3. QA and Docs Lane

## Role Descriptions, Explanations, and Contributions

### Layout Lane

Responsibilities:
1. Own shared shell and navigation updates in frontend/web/components/layout.php.
2. Own reusable design-system and global styling updates in frontend/web/public/assets/app.css.
3. Define and enforce spacing rhythm, breakpoint behavior, and global icon-treatment conventions.
4. Provide shared class refinements requested by repeated template needs.

Why this role exists:
- The layout/CSS foundation is the highest merge-conflict surface.
- Single-lane ownership keeps global changes coherent and prevents style drift.

Contribution to this plan:
- Unblocks Gate B by stabilizing the shared baseline.
- Makes page-by-page parity faster and safer for template work.
- Preserves cross-page consistency for final signoff.

### Page Templates Lane

Responsibilities:
1. Implement page-level wireframe parity in frontend/web/views/*.php.
2. Apply shared classes from the foundation without rewriting global structure.
3. Keep existing Stage 1 and staged scaffold boundaries intact while improving structure/visual parity.

Why this role exists:
- Most implementation volume is page-level template work.
- Isolating template ownership maximizes throughput and limits overlap with global CSS ownership.

Contribution to this plan:
- Delivers most of the visible Phase 2 and Phase 3 outputs.
- Drives Gate C and Gate D completion.
- Converts shared design rules into route-level parity.

### QA and Docs Lane

Responsibilities:
1. Run route smoke tests and parity checks after merge batches.
2. Validate responsiveness and accessibility spot checks.
3. Capture screenshot/evidence artifacts and maintain implementation records.
4. Keep transcript/reflection and phase-tracking documentation synchronized.

Why this role exists:
- Verification and evidence must run continuously, not only at the end.
- Dedicated ownership improves auditability and reduces missed signoff criteria.

Contribution to this plan:
- Protects regression safety while implementation proceeds.
- Provides objective gate evidence for parity and quality.
- Ensures final documentation/signoff completeness.

## Two-Person Assignment (Rebecca and Max)

To minimize merge conflicts and maintain delivery speed:
1. Rebecca is primary Layout Lane owner and integration support owner.
2. Max is primary Page Templates Lane owner and QA and Docs execution lead.
3. Cross-coverage is maintained by assigning each member as secondary owner on the other member's lead phases.

Phase-level assignment:
1. Phase 0: Lane Owner Rebecca, Secondary Max.
2. Phase 1: Lane Owner Rebecca, Secondary Max.
3. Phase 2: Lane Owner Max, Secondary Rebecca.
4. Phase 3: Lane Owner Max, Secondary Rebecca.
5. Phase 4: Lane Owner Max, Secondary Rebecca.

Lane-level ownership map:
1. Layout Lane: Rebecca (primary), Max (secondary).
2. Page Templates Lane: Max (primary), Rebecca (secondary).
3. QA and Docs Lane: Max (primary), Rebecca (secondary).

## Dependency Gates

Gate A: Wireframe Mapping Baseline
- Must be complete before any major template rewrites.

Gate B: Shared Layout and CSS Foundation
- Must be complete before broad page-level styling changes.

Gate C: Core Functional Pages Parity
- Must be complete before final cross-page consistency signoff.

Gate D: Scaffold Page Shell Parity
- Must be complete before final documentation closeout.

## Gate A Completion Plan

Purpose:
- Complete the Wireframe Mapping Baseline with low-risk documentation work that unblocks Phase 1 without code changes.

Required Gate A artifacts:
1. Page-by-page wireframe mapping matrix.
2. Icon placement matrix by page and component region.
3. Acceptance checklist template for structure, visuals, responsiveness, and accessibility.

Execution sequence:
1. Confirm page scope and route inventory from existing web views.
2. Build a canonical wireframe reference index from RiskRadar_Web_Wireframes.png.
3. Produce mapping matrix draft for all in-scope pages.
4. Produce icon placement matrix draft using wireframe_icons assets.
5. Produce acceptance checklist template aligned to matrix fields.
6. Run naming consistency pass across all three artifacts.
7. Move Gate A to In Review and request Rebecca and Max approval.

Parallelization rules for Gate A:
1. Scope confirmation and wireframe indexing can run in parallel.
2. Mapping matrix and icon matrix can run in parallel after scope is fixed.
3. Checklist template should follow early matrix drafts so criteria remain traceable.

Owner assignments:
1. Rebecca (Layout Lane):
   - Lead scope confirmation and global section taxonomy.
   - Lead mapping matrix and icon matrix creation.
   - Run final consistency pass and submit Gate A for review.
2. Max (Template and QA/Docs support):
   - Support current page structure inventory verification.
   - Support acceptance checklist evidence structure.
   - Co-review Gate A artifact completeness.

Gate A artifact locations:
- docs/PLANNING_DOCS/STAGE2_DOCS/GATEA_WIREFRAME_MAPPING_MATRIX.md
- docs/PLANNING_DOCS/STAGE2_DOCS/GATEA_ICON_PLACEMENT_MATRIX.md
- docs/PLANNING_DOCS/STAGE2_DOCS/GATEA_ACCEPTANCE_CHECKLIST_TEMPLATE.md

Gate A completion definition:
1. All three artifacts exist and include all in-scope pages.
2. Page names, view names, and icon labels are consistent across artifacts.
3. Checklist items map to at least one field in a matrix artifact.
4. Rebecca and Max approve Gate A and status is marked Completed.

### Gate A Decision Log

| Date | Decision | Owner | Status | Notes |
|---|---|---|---|---|
| 2026-03-17 | Gate A artifact drafting started and consistency pass initiated | Rebecca | Open | Awaiting Max co-review and final approval |
| 2026-03-17 | Rebecca completed Gate A assigned work and submitted review package | Rebecca | In Review | Ready-to-send review note prepared for Max |

## Execution Order by Role

## Phase 0: Kickoff and Mapping (All Roles)

Duration: 0.5 to 1 day

Shared outputs:
- Page-by-page wireframe mapping matrix
- Icon placement matrix by page and component region
- Acceptance checklist template for structure, visuals, responsiveness, accessibility

Parallelization:
- Layout role prepares global section taxonomy.
- Template role captures current page structure inventory.
- QA and Docs role builds verification checklist and evidence template.

Exit criteria:
- Gate A approved by all roles.

## Phase 1: Shared Foundation (Layout Lane Leads)

Duration: 1 to 2 days

Layout Lane tasks:
1. Update shared shell and navigation in frontend/web/components/layout.php to match wireframe framing and hierarchy.
2. Expand reusable design system classes in frontend/web/public/assets/app.css for headings, panels, cards, icon slots, metadata rows, and form grids.
3. Implement hybrid icon foundation rules:
   - PNG icon classes for explicit branded and illustrative elements
   - CSS-native repeated badge treatments where consistent with wireframe intent
4. Standardize responsive breakpoints and spacing rhythm tokens.

Template Lane tasks (limited, non-blocking):
1. Prepare page-level placeholder hooks only, without deep restyling.

QA and Docs Lane tasks:
1. Validate no route regressions from shared changes.
2. Start before and after screenshot matrix for impacted global elements.

Exit criteria:
- Gate B approved.
- Shared CSS and layout conventions stable.

## Phase 2: Core Functional Page Parity (Template Lane Leads)

Duration: 2 to 3 days

Template Lane tasks:
1. Dashboard parity in frontend/web/views/dashboard.php.
2. Alerts parity in frontend/web/views/alerts.php.
3. Summaries parity in frontend/web/views/summaries.php.
4. Profile parity in frontend/web/views/profile.php.
5. Login and Register parity in frontend/web/views/login.php and frontend/web/views/register.php.
6. Risk page shell parity in frontend/web/views/risk.php while preserving Stage 2 scaffold boundary.

Layout Lane tasks (parallel support):
1. Add only shared class refinements requested by repeated template needs.
2. Avoid one-off CSS that belongs inside a single template unless approved.

QA and Docs Lane tasks:
1. Run route smoke checks after each page merge batch.
2. Execute parity checklist on structure and visuals for each completed page.
3. Capture screenshot evidence at desktop, tablet, and mobile.

Exit criteria:
- Gate C approved for all core pages.

## Phase 3: Scaffold and Detail Shell Parity (Template Lane Leads)

Duration: 1 to 2 days

Template Lane tasks:
1. Map shell parity in frontend/web/views/map.php.
2. Forecast shell parity in frontend/web/views/forecast.php.
3. Assistant shell parity in frontend/web/views/assistant.php.
4. Alert detail shell parity in frontend/web/views/alert_detail.php.
5. Summary detail shell parity in frontend/web/views/summary_detail.php.

Layout Lane tasks:
1. Provide shared shell utilities for scaffold pages if a repeated pattern appears.

QA and Docs Lane tasks:
1. Validate scaffold pages remain non-functional placeholders where functionality is deferred, but are visually wireframe-accurate.
2. Confirm detail shell hierarchy and icon consistency.

Exit criteria:
- Gate D approved.

## Phase 4: Global Consistency and Signoff (QA and Docs Lane Leads)

Duration: 1 day

QA and Docs Lane tasks:
1. Run full cross-page consistency sweep:
   - Typography hierarchy
   - Spacing rhythm
   - Icon sizing and placement
   - Card and panel alignment
2. Run responsiveness checks at agreed breakpoints.
3. Run keyboard and accessibility spot checks.
4. Document final pass and remaining known gaps.

Layout Lane and Template Lane tasks:
1. Fix only verified issues found in sweep.
2. Avoid introducing new visual patterns during bug-fix stage.

Exit criteria:
- Final signoff checklist complete.
- Evidence and implementation notes committed.

## Parallel Work Rules

To keep work clean and avoid merge conflicts:
1. Layout Lane owns frontend/web/components/layout.php and global sections of frontend/web/public/assets/app.css.
2. Template Lane owns frontend/web/views/*.php page structures.
3. QA and Docs Lane owns docs updates and verification evidence docs.
4. If Template Lane needs shared class changes, raise a request batch to Layout Lane once per day.
5. Do not modify shared layout structure from template branches unless explicitly coordinated.

## Suggested Branch Strategy

1. One integration branch for wireframe implementation.
2. One feature branch per lane:
   - wireframe-layout-foundation
   - wireframe-template-parity
   - wireframe-qa-docs
3. Merge order:
   - Layout foundation first
   - Template parity batches second
   - QA and Docs updates throughout, then final pass

## Page Assignment Matrix

Layout Lane high ownership impact:
- frontend/web/components/layout.php
- frontend/web/public/assets/app.css

Template Lane high ownership impact:
- frontend/web/views/dashboard.php
- frontend/web/views/alerts.php
- frontend/web/views/summaries.php
- frontend/web/views/profile.php
- frontend/web/views/login.php
- frontend/web/views/register.php
- frontend/web/views/risk.php
- frontend/web/views/map.php
- frontend/web/views/forecast.php
- frontend/web/views/assistant.php
- frontend/web/views/alert_detail.php
- frontend/web/views/summary_detail.php

QA and Docs Lane high ownership impact:
- docs/STAGE1_VERIFICATION_EVIDENCE.md for additional validation references
- docs/TRANSCRIPT.md for implementation milestone notes
- This document for status updates and phase completion checkmarks

## Acceptance Criteria

A page is considered complete only if all pass:
1. Structural parity: section order and major regions match wireframe intent.
2. Visual parity: spacing, alignment, and hierarchy are cohesive and consistent.
3. Icon parity: mapped icons appear in intended regions using hybrid strategy.
4. Responsive parity: no broken layouts at target breakpoints.
5. Accessibility baseline: keyboard navigation and visible focus behavior remain intact.
6. Regression safety: page still loads and existing API-backed content behaves safely in fallback states.

## Implementation Checklist by Phase

Phase 0:
- [x] Mapping matrix created
- [x] Icon matrix created
- [x] Checklist template created

Phase 1:
- [ ] Shared layout updated
- [ ] Global CSS foundation updated
- [ ] Hybrid icon classes implemented
- [ ] Route smoke test passed

Phase 2:
- [ ] Dashboard parity
- [ ] Alerts parity
- [ ] Summaries parity
- [ ] Profile parity
- [ ] Login parity
- [ ] Register parity
- [ ] Risk parity shell

Phase 3:
- [ ] Map shell parity
- [ ] Forecast shell parity
- [ ] Assistant shell parity
- [ ] Alert detail shell parity
- [ ] Summary detail shell parity

Phase 4:
- [ ] Global consistency sweep complete
- [ ] Responsive checks complete
- [ ] Accessibility spot checks complete
- [ ] Final signoff notes documented

## Notes

- This effort intentionally preserves existing backend and API contracts.
- Future functional upgrades for Stage 2 to Stage 4 should build on these wireframe-accurate page shells rather than replacing them.
