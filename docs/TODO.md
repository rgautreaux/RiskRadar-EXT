# RiskRadar CMPS 357 Execution TODO Tracker

This document tracks implementation tasks, verification, and stage-specific follow-up in chronological order.

## Scope Alignment

Required deliverables:
- Stage 1: Web-App Extension
- Stage 2: Environmental Risk Assessment and Alert Prioritization Extensions

Optional stretch goals:
- Stage 3: Data Visualization and UX Extension
- Stage 4: Predictive Analytics and AI-Driven Insights
- Stage 5: Ongoing Maintenance, Advanced Features, and Review

## Documentation Sync Checklist

When closing or advancing work, update docs in this order:
1. Update task status, blockers, and evidence in [TODO.md](./TODO.md)
2. Update stage implementation narrative in [STAGES.md](./STAGES.md)
3. Update stage status summary in [../README.md](../README.md)
4. If workflow changed, update [../USER_GUIDE.md](../USER_GUIDE.md)

---

## Stage 1: Web-App Extension (Completed)

### Objective
Build a distinct web-facing extension connected to existing backend APIs.

### Execution Checklist
- [x] S1-00: Finalize frontend stack decision and document decision rationale.
- [x] S1-01: Document architecture and backend route usage with endpoint contract details.
- [x] S1-02: Create frontend directory structure and environment config template.
- [x] S1-03: Build API service wrappers with standardized error handling.
- [x] S1-04: Implement dashboard-first MVP and scaffold alerts/summaries/user screens.
- [x] S1-05: Add security and reliability controls (validation, sanitization, output escaping, CSRF, defensive rendering).
- [x] S1-06: Add setup, run, and usage documentation.

### Verification Evidence
- [x] Web app runs locally and connects to backend endpoints.
- [x] Dashboard and scaffolded pages route correctly and render expected data.
- [x] Timeout, non-2xx, and malformed/empty payload behavior documented.
- [x] Responsive behavior validated at 360px, 768px, and 1280px.
- [x] Evidence demonstrates web UI distinctness from mobile flow/layout.

### Stage 1 Session Entries (After Checklist)

#### Runtime Validation, Backend Fix, and Documentation Synchronization Session (2026-03-17)
Summary:
- Re-ran backend tests and web runtime checks to validate Stage 1 completion claims.
- Diagnosed bcrypt/passlib compatibility failures in user-auth tests.
- Switched auth hashing path to pbkdf2_sha256 in code and test fixtures.
- Re-ran backend tests cleanly after the fix.

---

## Stage 2 TODOs: Environmental Risk Assessment and Alert Prioritization Extensions (Completed)

### Objective
Implement personalized risk scoring and smart alert prioritization.

### Stage 2 Kickoff Lock Checklist (2026-03-17)
- [x] Scoring formula and 0-100 normalization policy documented.
- [x] Sensitivity 0-5 contract and fallback defaults documented.
- [x] Prioritization formula and urgency thresholds documented.
- [x] Deterministic tie-break order documented.
- [x] Stage 2 implementation scaffolding created (backend, web, mobile prep modules).

### Personal Risk Scoring Checklist
- [x] S2-01: Define scoring factors, scale, and weighting rationale.
- [x] S2-02: Update models and schemas for sensitivity and score outputs.
- [x] S2-03: Implement risk scoring service with factor breakdown.
- [x] S2-04: Add score endpoint(s) with validation and auth handling.

### Alert Prioritization Checklist
- [x] S2-05: Define ranking formula and urgency thresholds.
- [x] S2-06: Implement deterministic prioritization logic.
- [x] S2-07: Integrate ranking into alert pipeline and API metadata.
- [x] S2-08: Present prioritized results in web and mobile UI.
- [x] S2-09: Add tests for scoring and prioritization consistency.

### Verification Evidence
- [x] Identical inputs produce consistent risk-score outputs.
- [x] Alert ordering matches documented ranking factors.
- [x] API docs include new score and priority fields and examples.

### Stage 2 Session Entries (After Checklist)

#### Stage 2 Documentation and Synchronization Session (2026-03-23)
Summary:
- Synced tracker, stages, readme, transcript, reflection, and authors documentation.
- Captured the Stage 2 completion state and evidence links in project docs.

---

## Stage 3 TODOs: Data Visualization and UX Extension (Completed)

### Objective
Add an interactive risk map for spatial understanding of risk conditions.

### Execution Checklist
- [x] S3-00: Create Stage 3 planning docs (contract, verification evidence, implementation spec).
- [x] S3-01: Define map architecture and required geospatial fields.
- [x] S3-02: Implement map data transformation and coordinate validation.
- [x] S3-03: Build interactive map components (zoom, pan, click, overlays, legend).
- [x] S3-04: Integrate map with live backend risk and environmental data.
- [x] S3-05: Verify responsive and accessibility-friendly behavior.
- [ ] S3-06: Collect final manual evidence bundle (screenshots and recordings).

### Verification Evidence
- [x] Zoom, pan, and click behaviors work as expected.
- [x] Map reflects current backend risk data reliably.
- [x] UI remains usable on target screen sizes.
- [x] Accessibility features are present and verified.
- [ ] Final manual screenshot and recording bundle complete.

### Stage 3 Session Entries (After Checklist)

#### Stage 3 Phase 5 Completion Session (2026-03-24)
Summary:
- Progress summaries and phase-by-phase completion notes added to Stage 3 evidence docs.

#### Stage 3 Documentation and Synchronization Session (2026-03-31)
Summary:
- Performed a comprehensive Stage 3 doc synchronization pass across top-level files.

#### Stage 3 Documentation and Synchronization Session (2026-04-27)
Summary:
- Conducted another full synchronization pass and aligned top-level artifacts.

---

## Stage 4 TODOs: Predictive Analytics and AI-Driven Insights (In Progress)

### Objective
Deliver 24-48 hour forecasting and a RiskRadar AI Assistant with safeguards.

### Predictive Risk Checklist
- [ ] S4-01: Define forecast targets, horizon, and assumptions.
- [ ] S4-02: Build historical feature pipeline.
- [ ] S4-03: Implement baseline forecast service with confidence indicators.
- [ ] S4-04: Add forecast API endpoint(s) and trend visualization integration.

### AI Assistant Checklist
- [x] S4-04a: Integrate assistant icon and visual assets into assistant UI and planning docs.
- [ ] S4-05: Define assistant scope, guardrails, and safe fallback behavior.
- [ ] S4-06: Implement assistant backend prompt and data integration.
- [x] S4-07: Integrate assistant UI and evaluate quality and safety behavior.
- [x] S4-08: Document predictive and assistant limitations and future improvements.

### Verification Evidence
- [ ] Forecast API returns valid 24-48 hour schema outputs.
- [ ] Forecast visualizations are understandable and aligned with model output.
- [x] Assistant UI integration and guardrail documentation completed.

### Stage 4 Session Entries (After Checklist)

#### Stage 4 Planning and Asset Integration Session (2026-03-26)
Summary:
- Created Stage 4 planning artifacts and linked assistant visual asset planning.

#### Stage 4 Forecast UI and Asset Integration Session (2026-03-30)
Summary:
- Updated forecast UI to use project icons, illustrations, and shared theme styles.

#### Stage 4 Forecast UI Completion and Documentation Update Session (2026-03-31)
Summary:
- Forecast UI completion verified and synchronized across documentation.

#### Stage 4 AI Assistant Widget Integration and Documentation Sync Session (2026-03-31)
Summary:
- Integrated React-based assistant widget into the PHP web frontend and synchronized docs.

#### Stage 4 Context-Aware Golby, Backend Data Integration, and Documentation Sync Session (2026-04-02)
Summary:
- Added context-aware assistant behavior with backend data integration.

#### Stage 4 Documentation Synchronization and Forecast UI Session (2026-04-02)
Summary:
- Performed full top-level documentation synchronization for completed forecast features.

#### Stage 4 Forecast UI and Asset Integration Session (2026-04-28)
Summary:
- Finalized asset-path and CSS synchronization work for forecast and related UI files.

---

## Stage 5 TODOs: Ongoing Maintenance, Advanced Features, and Review (Completed)

### Objective
Maintain delivered features, harden security, and keep documentation and verification synchronized.

### Execution Checklist
- [x] S5-01: Maintain map reliability and accessibility quality gates.
- [x] S5-02: Keep top-level docs synchronized after major changes.
- [x] S5-03: Implement user-data security hardening and migration support.
- [x] S5-04: Re-run full backend verification and resolve blocking regressions.

### Verification Evidence
- [x] Ongoing map and accessibility checks documented.
- [x] Security and migration rollout documented.
- [x] Full backend suite passed after regression fixes.

### Stage 5 Session Entries (After Checklist)

#### Stage 5 Ongoing Maintenance, Advanced Features, and Review Session (2026-04-02)
Summary:
- Transitioned to ongoing maintenance mode and documented next-step roadmap.

#### Stage 5 User Data Security, Migration, and Full-Suite Verification Session (2026-04-02)
Summary:
- Implemented encrypted email storage, deterministic lookup hashing, stronger password validation, and schema-aware migration.
- Revalidated backend with full-suite pass and synchronized top-level docs.

---

## Team6 Backend Sync Session (Cross-Stage)

### Team6 Backend Sync and Documentation Synchronization Session (2026-03-24)
Summary:
- Compared backend changes with Team6, produced merge guidance, and synchronized documentation records.

## Execution Hygiene and Reporting

- During each weekly check-in, update Status, Target Week, Last Updated, and Evidence for active tasks.
- Keep stage naming and status vocabulary synchronized with README.md and docs/STAGES.md.
- For completed tasks, include one concrete evidence artifact (test output, screenshot, demo note, or commit reference).
- If any task slips by more than one target week, record blocker reason and revised target week.

## Status Legend

- Not Started: Requirements are defined, but implementation has not begun.
- In Progress: Implementation is actively underway and may be partially complete.
- Completed: Implementation and verification are complete, with docs and tests updated as needed.
