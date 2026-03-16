# Wireframe Style Implementation Plan

This document defines a role-based execution order to make the web app structurally and visually accurate to the RiskRadar web wireframes while using a hybrid icon strategy from the wireframe_icons directory.

## Standup Progress Tracker

Use this table for daily check-ins and updates.

| Workstream | Lane Owner | Secondary Owner | Start Date | Target Due Date | Status | Notes |
|---|---|---|---|---|---|---|
| Phase 0: Kickoff and Mapping | TBD | TBD | TBD | TBD | Not Started | Mapping matrix, icon matrix, and acceptance checklist |
| Phase 1: Shared Foundation | TBD | TBD | TBD | TBD | Not Started | Shared layout, global CSS patterns, hybrid icon foundation |
| Phase 2: Core Functional Page Parity | TBD | TBD | TBD | TBD | Not Started | Dashboard, Alerts, Summaries, Profile, Login, Register, Risk |
| Phase 3: Scaffold and Detail Shell Parity | TBD | TBD | TBD | TBD | Not Started | Map, Forecast, Assistant, Alert Detail, Summary Detail |
| Phase 4: Global Consistency and Signoff | TBD | TBD | TBD | TBD | Not Started | Consistency sweep, responsive checks, accessibility spot checks |

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

## Dependency Gates

Gate A: Wireframe Mapping Baseline
- Must be complete before any major template rewrites.

Gate B: Shared Layout and CSS Foundation
- Must be complete before broad page-level styling changes.

Gate C: Core Functional Pages Parity
- Must be complete before final cross-page consistency signoff.

Gate D: Scaffold Page Shell Parity
- Must be complete before final documentation closeout.

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
- [ ] Mapping matrix created
- [ ] Icon matrix created
- [ ] Checklist template created

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
