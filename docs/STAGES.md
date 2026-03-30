# Staged Development Plan for RiskRadar CMPS 357 Final Project

This document provides a complete, stage-by-stage implementation plan aligned with the required extension work in `docs/INSTRUCTIONS.md`. The format and structure follow the same style used in `EXAMPLE_STAGES.md` for consistency, readability, and professional reporting.

## Navigation Quick Links

- Requirements source: [INSTRUCTIONS.md](./INSTRUCTIONS.md)
- Task tracker and weekly evidence: [TODO.md](./TODO.md)
- Status authority for stage table: [../README.md](../README.md)
- User-facing usage guide: [../USER_GUIDE.md](../USER_GUIDE.md)
- Planning timeline details: [PLANNING_DOCS/PLANNING_STAGES.md](./PLANNING_DOCS/PLANNING_STAGES.md)
- Stage 1 endpoint contract: [PLANNING_DOCS/STAGE1_DOCS/API_STAGE1_CONTRACT.md](./PLANNING_DOCS/STAGE1_DOCS/API_STAGE1_CONTRACT.md)
- Stage 1 verification evidence: [PLANNING_DOCS/STAGE1_DOCS/STAGE1_VERIFICATION_EVIDENCE.md](./PLANNING_DOCS/STAGE1_DOCS/STAGE1_VERIFICATION_EVIDENCE.md)
- Stage 2 implementation spec: [PLANNING_DOCS/STAGE2_DOCS/STAGE2_IMPLEMENTATION_SPEC.md](./PLANNING_DOCS/STAGE2_DOCS/STAGE2_IMPLEMENTATION_SPEC.md)
- Stage 2 endpoint contract: [PLANNING_DOCS/STAGE2_DOCS/API_STAGE2_CONTRACT.md](./PLANNING_DOCS/STAGE2_DOCS/API_STAGE2_CONTRACT.md)
- Stage 2 verification evidence: [PLANNING_DOCS/STAGE2_DOCS/STAGE2_VERIFICATION_EVIDENCE.md](./PLANNING_DOCS/STAGE2_DOCS/STAGE2_VERIFICATION_EVIDENCE.md)

## Stage Alignment Note

- This plan maps directly to Stages 1-4 in `docs/INSTRUCTIONS.md`.
- Each stage includes implementation tasks, deliverables, and verification expectations.
- Stage progress markers should be updated as work is completed.

---


## Team6 Backend Sync and Documentation Synchronization (2026-03-24)

Summary:
- Compared the backend of this project to Team6’s backend, generated a file-by-file breakdown of changes, summarized which Team6 improvements are beneficial to merge, and created a markdown table for team review.
- Developed a detailed, actionable plan for merging improvements and updated BACKEND_REMOTE_UPDATE.md with all findings, tables, and plans.
- Located all relevant documentation files (TRANSCRIPT, REFLECTION, AUTHORS, README, etc.) and updated them with session results, summaries, deduplication, and synchronization.
- This process ensures grading clarity, project traceability, and best practices in collaborative development and documentation governance.

## Stage 3 Documentation and Synchronization Session (2026-04-27)

Summary:
- Comprehensive documentation update and synchronization pass for Stage 3 completed.
- Verbatim transcript and session summary added to TRANSCRIPT.md and REFLECTION.md.
- AUTHORS.md updated with current contributions and roles.
- README, STAGES.md, and USER_GUIDE.md reviewed and updated for consistency and agreement.

This ensures all top-level documentation is in sync for grading, onboarding, and future development.

Recommended sync order when updating progress:
1. Update implementation evidence and task status in [TODO.md](./TODO.md)
2. Update stage narrative and completion notes in [STAGES.md](./STAGES.md)
3. Synchronize top-level stage status in [../README.md](../README.md)
4. If user workflow changed, update [../USER_GUIDE.md](../USER_GUIDE.md)

## Scope and Timeline

**Required Deliverables:**
- **Stage 1**: Web-App Extension — ✅ Completed (2026-03-13)
- **Stage 2**: Environmental Risk Assessment and Alert Prioritization Extensions — ✅ Completed (2026-03-24)
  - Step 1: Personal Risk Scoring Engine
  - Step 2: Smart Alert Prioritization System


**Optional Stretch Goals:**
- **Stage 3**: Data Visualization and User Experience Extensions — ✅ Completed (2026-03-24)
   - Interactive risk map, personalized overlays, accessibility, and responsive UX implemented.
   - Planning docs in `docs/PLANNING_DOCS/STAGE3_DOCS/`.
- **Stage 4**: Predictive Analytics and AI-Driven Insights Extensions — ⏳ Not Started

---



## Stage 4: Forecast UI & Asset Integration Session (2026-03-30)

Summary:
- Forecast UI updated to reference project-specific icons and illustrations from /assets/illustrations/.
- theme.css and app.css created/updated for consistent RiskRadar branding across all web pages.
- Asset paths and CSS references synchronized in forecast.php and related frontend files.
- Documentation synchronization and audit tasks completed for Stage 4 asset integration.
- All top-level documentation (README, STAGES.md, TODO.md, AUTHORS.md, TRANSCRIPT.md, REFLECTION.md) updated with session summary, transcript entry, and author contributions for Stage 4.

This ensures all UI and documentation changes for Stage 4 are traceable, consistent, and ready for grading.

Summary:
- Stage 4 planning documents created and cross-linked: Implementation Spec, Verification Evidence, API Contract, and Golby Icon Plan.
- Golby AI Assistant icon/visuals asset integration planned, referencing both ai-assistant.svg (SVG) and RiskRadar_Assistant_Icon.png (PNG) for use in the assistant UI.
- All Stage 4 planning docs now include navigation links for easy cross-referencing.
- Documentation synchronization and audit tasks updated for Stage 4 kickoff.
- Weekly Check-In Log and Master Task Tracker updated to reflect new planning, asset integration, and documentation sync.

**Relevant Stage 4 Planning Docs:**
- [API_STAGE4_CONTRACT.md](./PLANNING_DOCS/STAGE4_DOCS/API_STAGE4_CONTRACT.md)
- [STAGE4_IMPLEMENTATION_SPEC.md](./PLANNING_DOCS/STAGE4_DOCS/STAGE4_IMPLEMENTATION_SPEC.md)
- [STAGE4_VERIFICATION_EVIDENCE.md](./PLANNING_DOCS/STAGE4_DOCS/STAGE4_VERIFICATION_EVIDENCE.md)
- [GOLBY_ICON_PLAN.md](./PLANNING_DOCS/STAGE4_DOCS/GOLBY_ICON_PLAN.md)

**Asset References:**
- `ai-assistant.svg` (SVG icon)
- `RiskRadar_Assistant_Icon.png` (PNG icon)

**See also:** [PLANNING_STAGES.md](./PLANNING_DOCS/PLANNING_STAGES.md), [TODO.md](./TODO.md), [README.md](../README.md)

---

**Status Legend**
- **Not Started**: Requirements are defined, but implementation has not begun.
- **In Progress**: Implementation is actively underway and may be partially complete.
- **Completed**: Implementation and verification are complete, with docs/tests updated as needed.

---

## Stage 1: Web-App Extension (Completed)

**Objective**: Build a web-application extension of RiskRadar that uses the existing backend and data sources while providing a unique frontend experience. *(REQUIRED - Target Completion: Week of March 31, 2026)*

### Tasks:
1. **Define the web extension architecture**
   - Document how the PHP web app communicates with backend API routes.
   - Identify reusable backend endpoints (alerts, summaries, users) and document method, params, response shape, and fallback behavior.
   - Maintain the Stage 1 API contract matrix in `docs/PLANNING_DOCS/STAGE1_DOCS/API_STAGE1_CONTRACT.md`.
   - Define URL/environment configuration for local and deployed usage.

2. **Create web-app project structure**
   - Keep the existing Expo mobile app under `frontend/mobile/` and build the dedicated PHP web app under `frontend/web/` with organized subdirectories for views, components, services, and assets.
   - Organize views, reusable PHP components, API client helpers, and assets.
   - Add `.env.example` (or config template) for API base URL, API prefix (`/api/v1`), and timeout settings.

3. **Implement backend connectivity from PHP**
   - Create PHP service wrappers for existing backend endpoints (alerts, summaries, user data).
   - Handle authentication (if needed) and include necessary headers.
   - Implement robust HTTP error handling (timeouts, non-2xx, malformed responses) with user-safe fallback messages.
   - Normalize response objects for use by presentation templates.

4. **Design and implement unique web UI screens**
   - Build a web homepage/dashboard distinct from the mobile experience as the Stage 1 MVP vertical slice.
   - Add scaffolded core pages for alerts, summaries, and user profile/preferences (placeholder-ready if full implementation is deferred).
   - Ensure consistent navigation and responsive layout behavior.

5. **Add security and reliability essentials**
   - Validate and sanitize all user inputs in forms and query parameters using allowlists where possible.
   - Escape rendered output in PHP templates and use CSRF protection for form submissions.
   - Avoid exposing secrets in source code or client-side payloads.
   - Add defensive rendering for missing/null API fields and retry-safe timeout handling.

6. **Document setup and usage**
   - Add run instructions for local PHP server and backend startup.
   - Document required environment variables and expected API availability.
   - Include screenshots or sample flows in docs.

### Stage 1 Implementation Boundary (MVP First)
- **In Scope for Stage 1 completion**:
  - Dashboard vertical slice in `frontend/web/` with alerts summary/stats and latest summary.
  - Working API wrapper layer for alerts, summaries, and user preference/register pathways.
  - Navigation plus scaffolded alerts/summaries/profile pages.
  - Setup/run documentation and Stage 1 verification evidence.
- **Out of Scope for Stage 1 (deferred to later stages or follow-on iteration)**:
  - Personalized risk scoring logic and smart alert ranking.
  - Interactive risk map.
  - Predictive analytics and AI assistant enhancements.

### Web Distinctness Criteria (Stage 1 Definition of Done)
- Dashboard uses desktop-oriented information density (multi-card stats + latest summary context in one view).
- Navigation and layout patterns are web-native and not a direct mirror of the mobile screen flow.
- At least one comparative/overview element is included (for example: "top alerts now" with latest summary snapshot).
- Keyboard-friendly navigation and responsive behavior are verified on common viewport sizes.

### Stage 1 API Contract Snapshot
Reference: `docs/PLANNING_DOCS/STAGE1_DOCS/API_STAGE1_CONTRACT.md`

| Route | Method | Request Inputs | Response Model | Fallback Behavior |
|---|---|---|---|---|
| `/api/v1/alerts` | GET | Query: `alert_type?`, `severity?`, `source?`, `limit<=200`, `offset` | `list[AlertOut]` | Treat non-2xx/timeout/malformed payload as empty list with user-safe message. |
| `/api/v1/alerts/stats` | GET | None | `AlertStats` | Render zero-state stats card if request fails. |
| `/api/v1/alerts/{alert_id}` | GET | Path: `alert_id:int` | `AlertOut` | Handle `404` as not-found state; do not crash page rendering. |
| `/api/v1/summaries` | GET | Query: `summary_type?`, `limit?` | `list[SummaryOut]` | Render empty summaries state on failure/empty payload. |
| `/api/v1/summaries/latest` | GET | None | `SummaryOut | null` | Render "no summary available" panel when null/error. |
| `/api/v1/summaries/generate` | POST | None | `SummaryOut` | Handle `404` as "no alerts to summarize"; keep dashboard usable. |
| `/api/v1/users/register` | POST | JSON `UserCreate` | `UserOut` | Handle `400` duplicate email with inline validation message. |
| `/api/v1/users/{user_id}/preferences` | PUT | Path: `user_id:int`, JSON `UserPrefsUpdate` | `UserOut` | Handle `404` user-not-found with non-blocking UI error state. |

### Verification Checklist:
- Web app loads successfully and connects to backend APIs from local config template values.
- Dashboard renders live data and shows safe fallback UI for timeout, non-2xx, and malformed/empty payload paths.
- Stage 1 MVP pages (dashboard + scaffolded alerts/summaries/profile) route correctly.
- UI is responsive and functionally distinct from mobile interface at 360px, 768px, and 1280px viewports.
- Verification evidence includes screenshots/walkthrough notes for success and failure states.

**Deliverables**:
- Web app extension codebase (PHP frontend)
- API integration layer in PHP
- Stage 1 endpoint contract matrix (`docs/PLANNING_DOCS/STAGE1_DOCS/API_STAGE1_CONTRACT.md`)
- Setup and run documentation
- Basic usability verification evidence (screenshots and/or walkthrough)

### Progress So Far
**Completed** - Stage 1 deliverables are implemented and documented, including dashboard-first web MVP pages, API wrapper integration, security/reliability controls, setup/run guidance, and responsive/web-distinctness verification evidence. See `docs/TODO.md`, `docs/PLANNING_DOCS/STAGE1_DOCS/API_STAGE1_CONTRACT.md`, and `docs/PLANNING_DOCS/STAGE1_DOCS/STAGE1_VERIFICATION_EVIDENCE.md`.

---

## Stage 2: Environmental Risk Assessment and Alert Prioritization Extensions

**Objective**: Extend backend intelligence by introducing personalized risk scoring and smart alert prioritization for both mobile and web clients. *(REQUIRED — Completed)*

### Stage 2 Dedicated Artifacts

- Endpoint contract matrix: `docs/PLANNING_DOCS/STAGE2_DOCS/API_STAGE2_CONTRACT.md`
- Verification evidence log: `docs/PLANNING_DOCS/STAGE2_DOCS/STAGE2_VERIFICATION_EVIDENCE.md`
- Policy lock reference: `docs/PLANNING_DOCS/STAGE2_DOCS/STAGE2_IMPLEMENTATION_SPEC.md`

### Stage 2 Kickoff Policy Lock (2026-03-17)
Reference: `docs/PLANNING_DOCS/STAGE2_DOCS/STAGE2_IMPLEMENTATION_SPEC.md`

- **Scoring model locked**: 0-100 normalized weighted sum with tier labels (`Low 0-39`, `Medium 40-69`, `High 70-100`).
- **Sensitivity contract locked**: 0-5 per factor, with defaults for existing users.
- **Prioritization formula locked**: weighted risk contribution + distance + severity + sensitivity match.
- **Tie-break policy locked**: severity score, then freshness (`fetched_at`), then alert ID.
- **Compatibility strategy locked**: preserve Stage 1 `/api/v1/alerts` behavior and introduce `/api/v1/alerts/prioritized` for Stage 2 metadata.
- **Scaffolding prepared**: backend service modules, web risk view integration points, and mobile data-service hooks are now staged for implementation handoff.

### Step 1: Personal Risk Scoring Engine

#### Tasks:
1. **Define risk model inputs and scoring formula**
   - Include location, health sensitivities, and current environmental conditions.
   - Choose an interpretable scoring scale (for example 0-100 or tiered levels).
   - Document weighting and rationale.

2. **Extend data model and schemas**
   - Add user sensitivity/preferences fields where needed.
   - Add schema fields for computed risk score and component breakdown.
   - Ensure backward compatibility for existing users.

3. **Implement scoring service in backend**
   - Create reusable scoring logic module/service.
   - Calculate score from live/scraped data and user profile.
   - Return score with traceable factors for transparency.

4. **Expose scoring through API**
   - Add or extend endpoint(s) for risk score retrieval.
   - Enforce input validation and authentication rules.
   - Add API examples in documentation.

5. **Apply privacy and data-handling safeguards**
   - Limit collected health data to minimum necessary fields.
   - Protect sensitive values in logs and responses.
   - Document privacy assumptions/constraints for course scope.

### Step 2: Smart Alert Prioritization System

#### Tasks:
1. **Define ranking criteria**
   - Risk score
   - Distance from user
   - Severity
   - User sensitivity

2. **Implement prioritization algorithm**
   - Compute a normalized priority value per alert.
   - Resolve ties deterministically (time/severity/freshness).
   - Support configurable thresholds for high/medium/low urgency.

3. **Integrate prioritization into alert pipeline**
   - Apply ranking before alerts are returned to clients.
   - Include priority metadata in API responses.
   - Preserve raw alert context for auditability.

4. **Surface prioritized results in UI**
   - Show ordered alerts in both web and mobile experiences.
   - Add priority labels and concise explanation text.
   - Ensure fallback behavior if scoring data is unavailable.

### Verification Checklist:
- Risk scores are computed consistently for same inputs.
- Prioritized alerts reflect the defined ranking factors.
- API contracts for score and priority fields are documented and tested.

**Deliverables**:
- Risk scoring engine implementation
- Prioritization algorithm integrated into alert flow
- Updated API endpoints/schemas
- Test coverage for scoring and ranking behavior
- Documentation of model logic and tradeoffs

### Progress So Far
✅ **Completed** - Both steps are implemented and tested:

**Step 1 (Personal Risk Scoring Engine):**
- Scoring model defined: 0-100 scale with proximity (40%), severity (30%), health sensitivity (20%), alert density (10%) weights.
- User model extended with `health_conditions` field (backward compatible, default `[]`).
- Scoring service implemented in `backend/scoring/__init__.py` with haversine distance, severity weighting, condition-to-alert-type matching, and density thresholds.
- API endpoint: `GET /api/v1/risk/score/{user_id}?radius_km=150` returns score, level, factor breakdown, and nearby alert count.
- User preferences updated to accept `health_conditions`, `latitude`, `longitude` via PUT.
- DB migration: `backend/db/migrations/2026-03-18_add_health_conditions.sql`.
- 36 tests passing in `backend/tests/test_risk_scoring.py` (unit + integration + API).

**Step 2 (Smart Alert Prioritization System):**
- Ranking criteria defined: distance (35%), severity (30%), health sensitivity (25%), recency (10%).
- Prioritization algorithm implemented in `backend/scoring/prioritization.py` with deterministic tie-breaking (priority desc → severity rank desc → distance asc → fetched_at desc → alert_id asc).
- Urgency thresholds: high (70-100), medium (40-69), low (0-39).
- API endpoint: `GET /api/v1/alerts/prioritized/{user_id}?radius_km=150&limit=50` returns prioritized alert list with per-alert priority score, level, distance, and factor breakdown.
- Schemas added: `PrioritizedAlertOut`, `PrioritizedAlertListOut`, `PriorityFactors` in `backend/schemas/alert.py`.
- Raw alert context preserved in response (all original alert fields included alongside priority metadata).
- Web UI: Smart Alerts page (`frontend/web/public/smart_alerts.php`) shows ranked alerts with priority labels, factor breakdown, and fallback states.
- Risk page (`frontend/web/views/risk.php`) updated from scaffold to functional page with risk score display and top-5 prioritized alert preview.
- Tests in `backend/tests/test_alert_prioritization.py`: unit tests for all 4 factor calculators, integration tests for `prioritize_alerts` and `compute_alert_priority`, and API endpoint tests.

---

## Stage 3: Data Visualization and User Experience Extensions

**Objective**: Add an interactive risk map experience that helps users explore and understand environmental risk conditions spatially. *(OPTIONAL STRETCH GOAL — Completed)*

### Step 1: Interactive Risk Map (UI Extension)

#### Tasks:
1. **Define map visualization architecture**
   - Select Plotly map approach (`scatter_mapbox`/`density_mapbox`/geo layers as appropriate).
   - Define required geographic fields (lat/lon, region labels, risk metrics).
   - Specify refresh strategy for near-real-time updates.

2. **Implement map data preparation pipeline**
   - Transform backend alert/risk responses into map-friendly structures.
   - Validate coordinates and handle missing or invalid geospatial data.
   - Attach metadata for hover cards and detail views.

3. **Build interactive map component(s)**
   - Enable zoom, pan, and point/region selection.
   - Add click interactions for detailed risk info.
   - Use clear legend and risk-level visual encoding.

4. **Integrate with backend for live data**
   - Connect map view to current environmental data and risk scores.
   - Add loading and retry states for unstable network/API responses.
   - Keep map interactions performant with realistic data volumes.

5. **Ensure responsive UX across app surfaces**
   - Confirm map usability on web and mobile form factors.
   - Maintain readable labels/popups at common viewport sizes.
   - Provide accessibility-friendly text alternatives where feasible.

### Verification Checklist:
- Interactive map supports zoom/pan/click as required.
- Map reflects backend risk data accurately and updates reliably.
- UI remains responsive and usable on target screen sizes.

**Deliverables**:
- Plotly-based interactive risk map implementation
- Data transformation logic for map rendering
- Responsive UI integration (web/mobile surfaces as planned)
- Documentation of visualization design choices

### Progress So Far
✅ **Completed** - Interactive risk map implemented and all Stage 3 web-app requirements verified:

- Backend map endpoints implemented and CORS-enabled: `GET /api/v1/alerts/map`, `GET /api/v1/risk/map`, `GET /api/v1/risk/map/personalized/{user_id}`.
- Web frontend `map.php` fetches and renders live alert and risk overlay data from backend endpoints.
- Dynamic overlays with overlay toggles, region filters, legend, tooltips, and personalized user overlays.
- Keyboard/touch navigation, dark mode, and responsive layout implemented and verified.
- Accessibility improvements (ARIA, keyboard navigation, color contrast) applied.
- Fallback UI and error states handled gracefully; map remains interactive if overlays fail to load.
- All evidence organized and referenced in planning docs. Onboarding template and handoff summary completed.
See `docs/PLANNING_DOCS/STAGE3_DOCS/` for contract, verification evidence, and implementation spec.

---

## Stage 4: Predictive Analytics and AI-Driven Insights Extensions

**Objective**: Extend RiskRadar with short-horizon risk forecasting and an AI assistant that helps users interpret conditions, alerts, and travel implications. *(OPTIONAL STRETCH GOAL - Only if Stage 3 completes early)*

### Step 1: Predictive Environmental Risk (AI/Data Extension)

#### Tasks:
1. **Define forecasting scope and targets**
   - Forecast environmental risk 24-48 hours ahead.
   - Select target metrics (overall risk score and/or category-specific risks).
   - Document assumptions about data latency and freshness.

2. **Build historical feature pipeline from scraper outputs**
   - Aggregate temporal patterns from collected environmental datasets.
   - Engineer lag/trend/seasonality features for short-horizon prediction.
   - Validate data quality before model inference.

3. **Implement forecasting module/service**
   - Start with baseline forecasting approach (transparent and testable).
   - Generate predictions with confidence indicators where possible.
   - Return model outputs in API-ready schema.

4. **Create forecast visualizations**
   - Plot predicted risk trends alongside recent observed values.
   - Mark confidence/uncertainty ranges in charts.
   - Highlight actionable interpretation for users.

5. **Integrate forecast outputs into app surfaces**
   - Expose endpoints for predictive risk retrieval.
   - Add UI cards/charts for “next 24-48 hours” insights.
   - Handle no-forecast-available fallback states.

### Step 2: RiskRadar AI Assistant

#### Tasks:
1. **Define assistant scope and guardrails**
   - Focus on interpreting environmental conditions, alerts, and travel risk context.
   - Restrict to informational guidance (non-medical and not a replacement for emergency services).
   - Define safe fallback messaging when confidence is low.

2. **Implement assistant backend integration**
   - Build prompt templates that combine user context + current risk data.
   - Add response formatting for concise, actionable explanations.
   - Apply token/error handling for robust runtime behavior.

3. **Add assistant UI experience**
   - Provide input box with prompt examples.
   - Render clear responses with links to supporting app data.
   - Include loading/error states and response history as needed.

4. **Evaluate assistant quality and safety**
   - Test for relevance, clarity, and factual consistency with app data.
   - Validate behavior for empty/missing context.
   - Document limitations and future improvements.

### Verification Checklist:
- Forecast service returns 24-48 hour predictions with valid schema.
- Forecast visualizations are understandable and consistent with model output.
- AI assistant provides context-aware interpretations with appropriate safeguards.

**Deliverables**:
- Predictive risk forecasting module and API integration
- Forecast visualization components
- AI assistant implementation (backend + UI integration)
- Evaluation notes on model behavior, limitations, and safeguards
- Updated documentation for usage and interpretation

### Progress So Far
⏳ **Not Started** - Planned: 24-48 hour forecasting and RiskRadar AI Assistant integration.

---

## Final Stage Completion Checklist

- Stage 1 web extension implemented and documented
- Stage 2 risk scoring and alert prioritization implemented and verified
- Stage 3 interactive risk map integrated and user-tested
- Stage 4 predictive analytics and AI assistant delivered with safeguards
- Documentation updated across `README.md` and `docs/` with setup, usage, and limitations

## Suggested Ongoing Reporting Format

For each stage, update:
- **Progress So Far** status marker (`Not Started`, `In Progress`, `Completed`)
- Key implementation outcomes
- Validation evidence (tests, screenshots, demo notes)
- Open risks and next actions

## Web-App Security Documentation

The RiskRadar web-app implements and documents security controls in docs/SecurityDocs/. All planning and verification steps reference these docs for compliance and evidence.
