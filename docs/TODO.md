# RiskRadar CMPS 357 Execution TODO Tracker

This document tracks implementation tasks required to complete the CMPS 357 extension goals.

## Scope Alignment

**REQUIRED DELIVERABLES (Target: April 29, 2026):**
- Stage 1: Web-App Extension
- Stage 2: Environmental Risk Assessment and Alert Prioritization Extensions (Personal Risk Scoring Engine + Smart Alert Prioritization System)

**OPTIONAL STRETCH GOALS (If time permits after Stage 2):**
- Stage 3: Data Visualization and User Experience Extensions (Interactive Risk Map)
- Stage 4: Predictive Analytics and AI-Driven Insights Extensions (Forecasting + AI Assistant)

**References:**
- Requirements scope: [INSTRUCTIONS.md](./INSTRUCTIONS.md)
- Stage planning details: [STAGES.md](./STAGES.md)
- Progress status source of truth: [README.md](../README.md)

## Status Legend

- **Not Started**: Requirements are defined, but implementation has not begun.
- **In Progress**: Implementation is actively underway and may be partially complete.
- **Completed**: Implementation and verification are complete, with docs/tests updated as needed.

## Weekly Check-In Workflow

Use this process during each weekly meeting:
1. Update each active task row in **Master Task Tracker** (`Status`, `Last Updated`, `Evidence`, `Notes`).
2. Move completed checklist items from stage sections to checked (`[x]`).
3. Fill one new row in **Weekly Check-In Log** with outcomes and blockers.
4. Sync stage-level status updates into [README.md](../README.md).

## Weekly Check-In Snapshot (Template)

- **Week Of**: YYYY-MM-DD
- **Planned This Week**: Task IDs
- **Completed This Week**: Task IDs
- **Blocked / At Risk**: Task IDs + reason
- **Decisions Needed**: short list
- **Evidence Added**: links or artifact descriptions

## Weekly Check-In Log

| Week Of | Completed Tasks | In Progress Tasks | Blockers | Decisions Needed | Evidence Added | Next Week Focus |
|---|---|---|---|---|---|---|
| 2026-03-10 | TODO tracker baseline created; frontend split confirmed (`frontend/mobile/` + `frontend/web/`) | S1-02, DOC-01, DOC-02, DOC-03 | Environment config template for web app not added yet | Confirm next Stage 1 implementation slice after scaffold | `docs/TODO.md`, `README.md`, `frontend/README.md`, `frontend/mobile/README.md`, `frontend/web/README.md` | Continue S1-02 and begin S1-01/S1-03 |
| 2026-03-12 | Stage 1 PHP MVP scaffold added with dashboard, alerts, summaries, and profile pages; config template and API wrapper layer implemented | S1-03, S1-04, S1-06 | PHP CLI not installed on workspace `PATH`, so runtime lint/server verification is blocked locally | Decide whether to install PHP locally now or validate on a teammate machine with PHP available | `frontend/web/public/index.php`, `frontend/web/public/alerts.php`, `frontend/web/public/summaries.php`, `frontend/web/public/profile.php`, `frontend/web/services/api_client.php`, `frontend/web/README.md` | Run end-to-end verification once PHP is available |

## Master Task Tracker

| Stage | Task ID | Task | Priority | Status | Owner | Target Week | Last Updated | Dependencies | Evidence | Notes |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | S1-00 | Confirm Stage 1 frontend stack decision and target directories | High | Completed | Rebecca | Week of 2026-03-10 | 2026-03-11 | Team planning alignment | `README.md`, `docs/STAGES.md`, `docs/PLANNING_STAGES.md`, `frontend/README.md` | Confirmed PHP web-app work targets `frontend/web/` and the existing mobile client remains in `frontend/mobile/`. |
| 1 | S1-01 | Define web extension architecture and backend API integration flow | High | In Progress | Rebecca | Week of 2026-03-17 | 2026-03-12 | S1-00 | `docs/API_STAGE1_CONTRACT.md` | Include alerts, summaries, and users endpoint contract details (method, params, response shape, fallback behavior). |
| 1 | S1-02 | Create frontend project structure and environment config template | High | Completed | Rebecca | Week of 2026-03-17 | 2026-03-12 | S1-00 | `frontend/web/config/app.php`, `frontend/web/config/config.local.example.php`, `frontend/web/README.md` | PHP web scaffold now includes local override config template and documented runtime settings. |
| 1 | S1-03 | Implement backend connectivity wrappers with error handling and response normalization | High | In Progress | Max | Week of 2026-03-24 | 2026-03-12 | S1-01, S1-02 | `frontend/web/services/api_client.php` | Wrappers now cover alerts, summaries, and user register/preferences paths with safe fallback behavior; end-to-end runtime verification remains pending until PHP is available locally. |
| 1 | S1-04 | Build web UI screens for dashboard, alerts, summaries, and user profile/preferences | High | In Progress | Rebecca | Week of 2026-03-24 | 2026-03-12 | S1-03 | `frontend/web/public/index.php`, `frontend/web/public/alerts.php`, `frontend/web/public/summaries.php`, `frontend/web/public/profile.php`, `frontend/web/public/assets/app.css` | Dashboard-first MVP and scaffolded core pages are now in place; responsive/runtime verification still needs PHP-backed manual QA. |
| 1 | S1-05 | Add input validation, sanitization, and defensive rendering for missing API fields | Medium | Not Started | Max | Week of 2026-03-31 | 2026-03-10 | S1-03, S1-04 | TBD | Avoid exposing secrets in source/client payloads. |
| 1 | S1-06 | Document setup and usage for backend + web app local run | High | In Progress | Rebecca | Week of 2026-03-31 | 2026-03-12 | S1-02, S1-04 | `frontend/web/README.md` | Startup/config notes are added; screenshots and full walkthrough evidence still need capture after runtime validation. |
| 2 | S2-01 | Define personal risk scoring model inputs, formula, and weighting rationale | High | Not Started | Max | Week of 2026-04-07 | 2026-03-10 | Stage 1 baseline | TBD | Use interpretable scale and document tradeoffs. |
| 2 | S2-02 | Extend data model/schemas for user sensitivity and risk score output fields | High | Not Started | Rebecca | Week of 2026-04-07 | 2026-03-10 | S2-01 | TBD | Preserve backward compatibility. |
| 2 | S2-03 | Implement backend risk scoring service and factor transparency output | High | Not Started | Max | Week of 2026-04-14 | 2026-03-10 | S2-02 | TBD | Return component breakdown for explainability. |
| 2 | S2-04 | Expose risk score endpoint(s) with validation and auth handling | High | Not Started | Max | Week of 2026-04-14 | 2026-03-10 | S2-03 | TBD | Add API examples to docs. |
| 2 | S2-05 | Define alert prioritization ranking criteria and normalization strategy | High | Not Started | Max | Week of 2026-04-14 | 2026-03-10 | S2-01 | TBD | Include risk score, distance, severity, sensitivity. |
| 2 | S2-06 | Implement prioritization algorithm with deterministic tie handling | High | Not Started | Max | Week of 2026-04-21 | 2026-03-10 | S2-05 | TBD | Add thresholds for high/medium/low urgency. |
| 2 | S2-07 | Integrate prioritized output into alert pipeline and API metadata | High | Not Started | Max | Week of 2026-04-21 | 2026-03-10 | S2-06 | TBD | Preserve raw alert context for auditability. |
| 2 | S2-08 | Surface prioritized alerts and score context in web/mobile UI | High | Not Started | Rebecca | Week of 2026-04-21 | 2026-03-10 | S2-04, S2-07 | TBD | Add fallback behavior if score unavailable. |
| 2 | S2-09 | Add tests for scoring consistency and prioritization behavior | High | Not Started | Max | Week of 2026-04-28 | 2026-03-10 | S2-03, S2-07 | TBD | Include repeat-input consistency checks. |
| 3 | S3-01 | Define Plotly risk map architecture and required geospatial fields | High | Not Started | Rebecca | Week of 2026-04-28 | 2026-03-10 | Stage 2 data outputs | TBD | **OPTIONAL/STRETCH**: Only if Stage 2 completes early. Select map approach and refresh strategy. |
| 3 | S3-02 | Implement data transformation pipeline for map-friendly structures | High | Not Started | Max | Week of 2026-05-05 | 2026-03-10 | S3-01 | TBD | **OPTIONAL/STRETCH**: Validate coordinates and attach hover metadata. |
| 3 | S3-03 | Build interactive map components (zoom/pan/click detail interactions) | High | Not Started | Rebecca | Week of 2026-05-05 | 2026-03-10 | S3-02 | TBD | **OPTIONAL/STRETCH**: Include legend and risk-level visual encoding. |
| 3 | S3-04 | Integrate map with live backend risk/environmental data | High | Not Started | Max | Week of 2026-05-12 | 2026-03-10 | S3-03 | TBD | **OPTIONAL/STRETCH**: Add loading/retry behavior for unstable API/network. |
| 3 | S3-05 | Verify responsive UX and accessibility-friendly behavior | Medium | Not Started | Rebecca | Week of 2026-05-12 | 2026-03-10 | S3-03, S3-04 | TBD | **OPTIONAL/STRETCH**: Validate viewport readability and alternatives. |
| 3 | S3-06 | Add map-related tests/manual verification evidence | High | Not Started | Rebecca | Week of 2026-05-12 | 2026-03-10 | S3-04, S3-05 | TBD | **OPTIONAL/STRETCH**: Capture screenshots/demo notes for checkpoints. |
| 4 | S4-01 | Define forecasting targets, horizon (24-48h), and assumptions | High | Not Started | Max | Week of 2026-05-19 | 2026-03-10 | Stage 2 baseline | TBD | **OPTIONAL/STRETCH**: Only if Stage 3 completes early. Document latency/freshness assumptions. |
| 4 | S4-02 | Build historical feature pipeline from scraper outputs | High | Not Started | Max | Week of 2026-05-19 | 2026-03-10 | S4-01 | TBD | **OPTIONAL/STRETCH**: Include lag/trend/seasonality features. |
| 4 | S4-03 | Implement baseline forecasting module/service with confidence indicators | High | Not Started | Max | Week of 2026-05-26 | 2026-03-10 | S4-02 | TBD | **OPTIONAL/STRETCH**: Keep model transparent and testable. |
| 4 | S4-04 | Expose forecast API endpoint(s) and integrate forecast visualizations | High | Not Started | Rebecca + Max | Week of 2026-05-26 | 2026-03-10 | S4-03 | TBD | **OPTIONAL/STRETCH**: Plot observed vs predicted with uncertainty range. |
| 4 | S4-05 | Define assistant scope, guardrails, and fallback policy | High | Not Started | Rebecca + Max | Week of 2026-05-26 | 2026-03-10 | S4-01 | TBD | **OPTIONAL/STRETCH**: Informational guidance only; no emergency replacement. |
| 4 | S4-06 | Implement AI assistant backend prompt integration and response formatting | High | Not Started | Max | Week of 2026-06-02 | 2026-03-10 | S4-05 | TBD | **OPTIONAL/STRETCH**: Add token/error handling and robust fallbacks. |
| 4 | S4-07 | Integrate assistant UI experience and evaluate quality/safety behavior | High | Not Started | Rebecca | Week of 2026-06-02 | 2026-03-10 | S4-06 | TBD | **OPTIONAL/STRETCH**: Test relevance, clarity, and missing-context behavior. |
| 4 | S4-08 | Document predictive/assistant limitations and future improvements | High | Not Started | Rebecca | Week of 2026-06-02 | 2026-03-10 | S4-04, S4-07 | TBD | **OPTIONAL/STRETCH**: Include interpretation guidance for users. |
| X | DOC-01 | Keep README stage-status table synchronized with completed tasks | High | In Progress | Rebecca | Weekly | 2026-03-10 | Ongoing | README commits | README remains status authority. |
| X | DOC-02 | Update STAGES/PROJECT docs when scope or stage progress changes | High | In Progress | Rebecca | Weekly | 2026-03-10 | Ongoing | Docs commits | Keep naming and status terms consistent. |
| X | DOC-03 | Log AI-assisted sessions in TRANSCRIPT and reflect in REFLECTION | High | In Progress | Rebecca | Weekly | 2026-03-10 | Ongoing | Transcript/Reflection entries | Maintain continuity and auditability. |

## Stage 1 TODOs: Web-App Extension

### Objective
Build a distinct web-facing extension connected to existing backend APIs.

### Execution Checklist
- [x] S1-00: Finalize frontend stack decision and document decision rationale.
- [ ] S1-01: Document architecture and backend route usage with endpoint contract details.
- [x] S1-02: Create frontend directory structure and environment config template.
- [ ] S1-03: Build API service wrappers with standardized error handling.
- [ ] S1-04: Implement dashboard-first MVP and scaffold alerts/summaries/user screens.
- [ ] S1-05: Add security/reliability controls (validation/sanitization/output escaping/CSRF/defensive rendering).
- [ ] S1-06: Add setup, run, and usage documentation.

### Verification Evidence
- [ ] Web app runs locally and connects to backend endpoints.
- [ ] Dashboard and scaffolded pages route correctly and render expected data.
- [ ] API timeout, non-2xx, and malformed/empty payload behavior is captured in notes/screenshots.
- [ ] Responsive behavior validated at 360px, 768px, and 1280px with screenshots and/or demo notes.
- [ ] Evidence demonstrates web UI distinctness from mobile flow/layout.

## Stage 2 TODOs: Risk Assessment and Alert Prioritization

### Objective
Implement personalized risk scoring and smart alert prioritization.

### Personal Risk Scoring Checklist
- [ ] S2-01: Define scoring factors, scale, and weighting rationale.
- [ ] S2-02: Update models/schemas for sensitivity and score outputs.
- [ ] S2-03: Implement risk scoring service with factor breakdown.
- [ ] S2-04: Add score endpoint(s) with validation/auth handling.

### Alert Prioritization Checklist
- [ ] S2-05: Define ranking formula and urgency thresholds.
- [ ] S2-06: Implement deterministic prioritization logic.
- [ ] S2-07: Integrate ranking into alert pipeline and API metadata.
- [ ] S2-08: Present prioritized results in web/mobile UI.
- [ ] S2-09: Add tests for scoring and prioritization consistency.

### Verification Evidence
- [ ] Identical inputs produce consistent risk score outputs.
- [ ] Alert ordering matches documented ranking factors.
- [ ] API docs include new score/priority fields and examples.

## Stage 3 TODOs: Data Visualization and UX Extension

### Objective
Add an interactive Plotly risk map for spatial understanding of risk conditions.

**OPTIONAL STRETCH GOAL - Only pursue if Stage 2 completes by end of Week of 2026-04-28.**

### Execution Checklist
- [ ] S3-01: Define map architecture and required geospatial fields.
- [ ] S3-02: Implement map data transformation and coordinate validation.
- [ ] S3-03: Build interactive map component(s) with detail interactions.
- [ ] S3-04: Integrate map with live backend risk/environment data.
- [ ] S3-05: Verify responsiveness and accessibility-friendly behavior.
- [ ] S3-06: Collect test/demo evidence for map interactions.

### Verification Evidence
- [ ] Zoom/pan/click behaviors work as expected.
- [ ] Map reflects current backend risk data reliably.
- [ ] UI remains usable on target screen sizes.

## Stage 4 TODOs: Predictive Analytics and AI-Driven Insights

### Objective
Deliver 24-48 hour forecasting and a RiskRadar AI Assistant with clear safeguards.

**OPTIONAL STRETCH GOAL - Only pursue if Stage 3 completes and time remains.**

### Predictive Risk Checklist
- [ ] S4-01: Define forecast targets, horizon, and assumptions.
- [ ] S4-02: Build historical feature pipeline.
- [ ] S4-03: Implement baseline forecast service with confidence indicator output.
- [ ] S4-04: Add forecast API endpoint(s) and trend visualization integration.

### AI Assistant Checklist
- [ ] S4-05: Define assistant scope, guardrails, and safe fallback behavior.
- [ ] S4-06: Implement assistant backend prompt/data integration.
- [ ] S4-07: Add assistant UI and evaluate quality/safety behavior.
- [ ] S4-08: Document limitations and next-step improvements.

### Verification Evidence
- [ ] Forecast API returns valid 24-48 hour schema outputs.
- [ ] Forecast visualizations are understandable and consistent with model output.
- [ ] Assistant responses remain context-aware and within guardrails.

## Execution Hygiene and Reporting

- During each weekly check-in, update `Status`, `Target Week`, `Last Updated`, and `Evidence` for all active tasks.
- Keep stage naming and status vocabulary synchronized with `README.md` and `docs/STAGES.md`.
- For completed tasks, include one concrete evidence artifact (test output, screenshot, demo note, or commit reference).
- If any task slips by more than one target week, mark it in `Notes` with blocker reason and revised target week.