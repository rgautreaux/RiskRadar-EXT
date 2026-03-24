
# Major Developments: Implementation, Functionality, Execution, and Importance

## Stage 3: Data Visualization and User Experience Extensions

### Implementation
Stage 3 introduced an interactive risk map and enhanced user experience features. The backend and frontend were prepared for new geoJSON endpoints, map rendering logic, and responsive UX improvements. Planning documents (API contract, verification evidence, implementation spec) were created to lock requirements and guide development.

**Phase 1 (Dynamic Data Integration for the web map) is complete and verified. The map page now fetches and renders live alert and risk data from backend endpoints.**

### Functionality
- **Interactive Risk Map:** Users can view environmental risks on a map, with real-time overlays for AQI, wildfires, and weather alerts.
- **Responsive UX Enhancements:** Improved mobile and web interfaces for better accessibility and usability.
- **Dark Mode:** Toggle-able dark mode for improved accessibility and user preference.
- **Keyboard/Touch Navigation:** Full support for keyboard and touch-based map interaction.

### Execution
All documentation files were updated to reflect the Stage 3 sync process, session summaries, and deduplication as described in the plan. This ensures grading clarity and project traceability. Implementation of interactive features follows the locked contract and verification evidence. All planning artifacts are synchronized across top-level documentation for grading and onboarding clarity.

### Importance
Stage 3 elevates RiskRadar by providing spatial context and visual decision support, making risk information more actionable and accessible for all users. The documentation synchronization ensures that all contributors and reviewers have a single source of truth for project status and history.
# Major Developments: Implementation, Functionality, Execution, and Importance

## Stage 3: Data Visualization and User Experience Extensions

### Implementation
Stage 3 planning introduced an interactive risk map and enhanced user experience features. The backend and frontend were prepared for new geoJSON endpoints, map rendering logic, and responsive UX improvements. Planning documents (API contract, verification evidence, implementation spec) were created to lock requirements and guide development.

**Phase 1 (Dynamic Data Integration for the web map) is complete and verified. The map page now fetches and renders live alert and risk data from backend endpoints.**

---

## Team6 Backend Sync and Documentation Synchronization (2026-03-24)

### Implementation
Compared the backend of this project to Team6’s backend, generated a file-by-file breakdown of changes, summarized which Team6 improvements are beneficial to merge, and created a markdown table for team review. Developed a detailed, actionable plan for merging improvements and updated BACKEND_REMOTE_UPDATE.md with all findings, tables, and plans. Located all relevant documentation files (TRANSCRIPT, REFLECTION, AUTHORS, README, etc.) and updated them with session results, summaries, deduplication, and synchronization.

### Functionality
- Provided a clear, actionable plan for syncing with Team6’s backend and identified which improvements to merge.
- Ensured all documentation files reflect the Team6 sync process and session results.
- Maintained a verbatim transcript and summary for audit and grading purposes.

### Execution
All documentation files were updated to reflect the Team6 sync process, session summaries, and deduplication as described in the plan. This ensures grading clarity and project traceability.

### Importance
This synchronization process ensures that the project benefits from Team6’s improvements while maintaining custom work and documentation integrity. It demonstrates best practices in collaborative development, documentation governance, and project traceability.

### Functionality
- **Interactive Risk Map:** Users will be able to view environmental risks on a map, with real-time overlays for AQI, wildfires, and weather alerts.
- **Responsive UX Enhancements:** Improved mobile and web interfaces for better accessibility and usability.

### Execution
Stage 3 deliverables are planned and documented. **Phase 1 (dynamic data integration for the web map) is fully implemented and live data is rendered on the map page.** Implementation of interactive features will follow the locked contract and verification evidence. All planning artifacts are synchronized across top-level documentation for grading and onboarding clarity.

### Importance
Stage 3 will further elevate RiskRadar by providing spatial context and visual decision support, making risk information more actionable and accessible for all users.

---

# Stage 3: Data Visualization and User Experience Extensions (Expanded)

## Implementation
Stage 3 focuses on adding an interactive risk map and user experience improvements. The backend and frontend are prepared for new geoJSON endpoints, map rendering logic, and responsive UX. Planning documents (API contract, verification evidence, implementation spec) are created and synchronized across all top-level documentation.

## Functionality
- **Interactive Risk Map:** Enables users to explore environmental risks spatially, with overlays for AQI, wildfires, and weather alerts.
- **Responsive UX Enhancements:** Improves accessibility and usability for both web and mobile users.

## Execution
Implementation will follow the locked contract and verification evidence, ensuring geospatial accuracy, responsive design, and accessibility. All planning artifacts are kept in sync for grading and onboarding clarity.

## Importance
This extension provides spatial context and visual decision support, making risk information more actionable and accessible. It demonstrates advanced data visualization, geospatial API design, and user experience engineering, further differentiating the web extension from the mobile app.
---

# Major Developments: Implementation, Functionality, Execution, and Importance

## Stage 2: Environmental Risk Assessment and Alert Prioritization Extensions

### Implementation
Stage 2 introduced a deterministic personal risk scoring engine and a smart alert prioritization system. The backend was extended with new service modules for risk scoring and alert prioritization, new API endpoints for risk score and prioritized alerts, and updated schemas to support sensitivity and priority metadata. Web and mobile clients were updated to surface these new outputs, with fallback-safe integration and robust error handling.

### Functionality
- **Personal Risk Scoring:** Computes a 0-100 risk score for each user based on air quality, weather, wildfire, and pollution risks, weighted by user sensitivity factors.
- **Smart Alert Prioritization:** Ranks alerts for each user using risk contribution, distance, severity, and sensitivity match, with urgency labels and deterministic tie-breaks.
- **API Exposure:** New endpoints allow clients to fetch risk scores and prioritized alerts, while preserving Stage 1 contract stability.
- **Cross-Client Parity:** Both web and mobile clients consume backend-prioritized ordering, ensuring consistent user experience.

### Execution
The implementation followed a locked policy and contract specification, with all formulas, thresholds, and normalization rules documented in the Stage 2 implementation spec. Verification included deterministic output tests, contract stability checks, and fallback behavior validation. Documentation, planning, and evidence artifacts were updated and synchronized across all top-level files.

### Importance
These developments transform RiskRadar from a simple alert aggregator into a personalized decision-support platform. Users now receive risk scores and prioritized alerts tailored to their sensitivities and context, improving relevance and actionability. The robust, deterministic backend logic and clear API contracts set a foundation for future extensions (e.g., interactive maps, predictive analytics, AI assistant) and ensure maintainability and grading clarity.

## Stage 3: Data Visualization and User Experience Extensions

### Implementation
Stage 3 planning introduced an interactive risk map and enhanced user experience features. The backend and frontend were prepared for new geoJSON endpoints, map rendering logic, and responsive UX improvements. Planning documents (API contract, verification evidence, implementation spec) were created to lock requirements and guide development.

### Functionality
- **Interactive Risk Map:** Users will be able to view environmental risks on a map, with real-time overlays for AQI, wildfires, and weather alerts.
- **Responsive UX Enhancements:** Improved mobile and web interfaces for better accessibility and usability.

### Execution
Stage 3 deliverables are planned and documented, with implementation to follow the locked contract and verification evidence. All planning artifacts are synchronized across top-level documentation for grading and onboarding clarity.

### Importance
Stage 3 will further elevate RiskRadar by providing spatial context and visual decision support, making risk information more actionable and accessible for all users.
# CMPS 357 - Final Project - Group 3

Due Date: May 6, 2026, 12:55 CST

This repository contains the code and documentation for Group 3's CMPS 357 final project. The primary objective is to build a meaningful extension of our CMPS 490 RiskRadar senior project with new web-facing capabilities and advanced decision-support features.

Our senior project focuses on developing **RiskRadar**, an environmental risk awareness platform that helps residents and travelers identify and manage potential environmental risks using data analytics.

Our goal for the CMPS 357 final project is to build a unique web-app extension with a distinct frontend interface while extending the platform with features such as personalized risk assessment, interactive mapping, and predictive/AI-supported insights.

## Documentation Quick Links (Grading + Navigation)

**Navigation hubs**

- Scope and requirements: [docs/INSTRUCTIONS.md](./docs/INSTRUCTIONS.md), [docs/PROJECT_DESCRIPTION.md](./docs/PROJECT_DESCRIPTION.md)
- Planning and stage narrative: [docs/STAGES.md](./docs/STAGES.md), [docs/PLANNING_DOCS/PLANNING_STAGES.md](./docs/PLANNING_DOCS/PLANNING_STAGES.md)
- Execution tracker and weekly status: [docs/TODO.md](./docs/TODO.md)
- Status authority and summary snapshot: [README.md](./README.md)
- Stage 1 evidence and contract: [docs/PLANNING_DOCS/STAGE1_DOCS/API_STAGE1_CONTRACT.md](./docs/PLANNING_DOCS/STAGE1_DOCS/API_STAGE1_CONTRACT.md), [docs/PLANNING_DOCS/STAGE1_DOCS/STAGE1_VERIFICATION_EVIDENCE.md](./docs/PLANNING_DOCS/STAGE1_DOCS/STAGE1_VERIFICATION_EVIDENCE.md)
- Stage 2 implementation spec: [docs/PLANNING_DOCS/STAGE2_DOCS/STAGE2_IMPLEMENTATION_SPEC.md](./docs/PLANNING_DOCS/STAGE2_DOCS/STAGE2_IMPLEMENTATION_SPEC.md)
- User walkthrough and demo flow: [USER_GUIDE.md](./USER_GUIDE.md)
- Historical/reference docs index: [docs/PLANNING_DOCS/](./docs/PLANNING_DOCS/)

**Documentation update order (required for sync):**
1. Update implementation tasks/evidence in [docs/TODO.md](./docs/TODO.md)
2. Update stage narrative and deliverables in [docs/STAGES.md](./docs/STAGES.md)
3. Update summary status table in [README.md](./README.md)
4. If workflow changes, update [USER_GUIDE.md](./USER_GUIDE.md)


---

# CMPS 357 Extension Project Proposal


## Initial Plan:

**Web-App Extension of our RiskRadar Mobile App**
Our initial idea was to create a web-app extension of our RiskRadar mobile app. This is because we thought a web extension would be a more straightforward extension of our mobile app, and would allow us to leverage the same backend we constructed and utilize the same data sources. 

However, our professor suggested we go the web extension route *only* if we do **NOT** pivot to a web app in CMPS490. If we *do* create a web app extension, then it was recommended that we implement an entirely new and unique frontend from the mobile app so that we do not have to rely on the CMPS490 frontend or wait for that frontend work to be completed before starting this project. This ensures a level of independence between the two projects and allows us to progress without depending on CMPS490 frontend timelines.

However, if issues arise and we must pivot in CMPS490, we are discussing additional extensions we can implement to further differentiate the two projects and ensure that we are not relying too heavily on CMPS490 for this project.

## Further Extensions (if we pivot to Web-App in CMPS490):

### Environmental Risk Assessment and Alert Prioritization Extensions

**Personal Risk Scoring Engine (Best Overall Option)**: Create a personalized environmental risk score for each user based on location, health sensitivities, and environmental data

**Smart Alert Prioritization System (Potential Extension of Personal Risk Scoring Engine)**:  Extend alerts into a priority ranking system by:
- Risk Score
- Distance from user
- Severity
- User sensitivity

### Predictive Analytics and AI-Driven Insights Extensions
**Predictive Environmental Risk (AI/Data Extension)**: Predict environmental risk 24–48 hours ahead by referencing the patterns from data obtained by scrapers

**RiskRadar AI Assistant**- AI assistant or guide integrated into the application that helps users interpret environmental conditions, alerts, or travel risks


### Data Visualization and User Experience Extensions
**Interactive Risk Map (Great UI Extension)**- Add a map visualization to the mobile/web app , similar to PA2 as to make the data presented even more user-friendly and accessible

**RiskRadar AI Assistant**- AI assistant or guide integrated into the application that helps users interpret environmental conditions, alerts, or travel risks


## Project Purpose
The goal of this project is to transform RiskRadar into a broader full-stack system by introducing a web application experience that is distinct from the mobile app while reusing the existing backend and data-ingestion foundation. This extension improves how users interpret environmental conditions by combining real-time alerts, AI-generated summaries, staged personalization features, and planned interactive/predictive capabilities.

---

## Team Members, Roles, Responsibilities, and Contributions

| Max                           | (Contributions) |


| Rebecca                           |  (Contributions) |

---

# CMPS 490 Senior Project Contents

## Project Content

### CMPS 490 RiskRadar Mobile App

[RiskRadar Mobile App Repository](https://github.com/QuiHu/Team6Project.git)
[RiskRadar README](./CMPS490_README.md)

**RiskRadar** is a mobile app designed to help users identify and manage potential environmental conditions and risks they may encounter while traveling or in day-to-day activities. The app provides features such as real-time alerts, climate data statistics, and user-friendly 5-minute summaries.

As an extension of our RiskRadar mobile app, this repository contains code from the mobile app to provide a foundation for our web-app extension.

### RiskRadar Web-App Extension

The frontend workspace is now explicitly split so the mobile and web clients can evolve independently while both are intended to use the same backend API service in `backend/`.

**Frontend surfaces:**
- `frontend/mobile/` — existing Expo/React Native mobile frontend workspace
- `frontend/mobile/RiskRadar/` — current RiskRadar mobile application files
- `frontend/web/` — designated CMPS 357 PHP web-app extension workspace

**Web frontend scaffold:**
- `frontend/web/views/` — page templates and routed screens
- `frontend/web/components/` — reusable PHP/UI fragments
- `frontend/web/services/` — backend API wrappers and response helpers
- `frontend/web/public/` — public-facing assets and entry files
- `frontend/web/config/` — environment and runtime configuration templates

**Mobile frontend note:**
- The existing Expo mobile app remains under `frontend/mobile/RiskRadar/`.
- Mobile setup instructions are in [`frontend/mobile/RiskRadar/README.md`](./frontend/mobile/RiskRadar/README.md).

**Web frontend note:**
- Stage 1 web-app development should be placed in `frontend/web/`.
- Web scaffold details are in [`frontend/web/README.md`](./frontend/web/README.md).
- Frontend workspace guidance is in [`frontend/README.md`](./frontend/README.md).

### Stage 1: Web-App Extension (Completed)

Stage 1 (Web-App Extension) is complete as of **2026-03-13** and includes the following implemented web features, structures, and supporting details.

#### Major Stage 1 Developments

1. **Web architecture and API contract formalization**
	- Finalized page-to-endpoint request flow and wrapper responsibilities for PHP entrypoints.
	- Documented Stage 1 endpoint matrix, schema snapshots, fallback behaviors, and URL composition rules.
	- Captured local and deployed environment configuration expectations for stable route targeting.

2. **Dedicated PHP web-app scaffold under `frontend/web/`**
	- Established web-native directory boundaries for entrypoints, templates, components, services, and config.
	- Preserved mobile/web separation by keeping Expo client work under `frontend/mobile/`.
	- Added local override configuration template for backend URL/prefix/timeout settings.

3. **Backend integration and normalization layer**
	- Implemented wrappers for alerts, summaries, register, and preferences write paths.
	- Standardized handling for timeout/non-2xx/malformed payload outcomes to prevent fatal page failures.
	- Added presentation-safe defaults so views can render resilient zero/empty states.

4. **Dashboard-first web UI with scaffolded core views**
	- Delivered a desktop-oriented dashboard with alert statistics, top-alert snapshot, and latest summary context.
	- Added Stage 1 scaffold pages for alerts, summaries, and profile/preferences updates.
	- Implemented responsive behavior for required viewport checkpoints (360px, 768px, 1280px).

5. **Security and reliability hardening for web write paths**
	- Added CSRF token protection for profile/register preference workflows.
	- Added allowlist-based validation/sanitization for key query and form inputs.
	- Ensured escaped output rendering and defensive handling of missing/null fields.

6. **Stage 1 setup and verification documentation**
	- Documented backend + PHP local run flow and configuration options.
	- Added Stage 1 verification evidence notes for responsive behavior and web-distinctness criteria.
	- Synchronized Stage 1 completion state across planning/tracker/summary docs.

#### Stage 1 Deliverables (Detailed)

| Deliverable | Description | Primary Artifacts |
|---|---|---|
| Web app extension codebase | PHP web MVP with dashboard plus scaffolded alerts/summaries/profile views | `frontend/web/public/index.php`, `frontend/web/public/alerts.php`, `frontend/web/public/summaries.php`, `frontend/web/public/profile.php` |
| API integration layer in PHP | Service wrappers, normalization, validation, and presentation/security helpers | `frontend/web/services/api_client.php`, `frontend/web/services/validators.php`, `frontend/web/services/presentation.php`, `frontend/web/services/bootstrap.php` |
| Stage 1 endpoint contract matrix | Route/method/input/output/fallback definitions and schema snapshots | `docs/PLANNING_DOCS/STAGE1_DOCS/API_STAGE1_CONTRACT.md` |
| Setup and run documentation | Configuration and local execution instructions for backend + PHP app | `frontend/web/README.md` |
| Verification evidence | Responsive and web-distinctness checkpoints with implementation signals | `docs/PLANNING_DOCS/STAGE1_DOCS/STAGE1_VERIFICATION_EVIDENCE.md`, `docs/TODO.md` |

**Implemented web feature set:**
- Dashboard (`frontend/web/public/index.php`) with alert stats, top alerts snapshot, and latest summary panel.
- Alerts explorer (`frontend/web/public/alerts.php`) with filter controls and safe empty-state behavior.
- Summaries archive (`frontend/web/public/summaries.php`) with summary-type/limit filtering and defensive rendering.
- Profile write-path scaffolding (`frontend/web/public/profile.php`) for register and preference updates.

**Web architecture and structure:**
- Public entrypoints: `frontend/web/public/`
- Templates: `frontend/web/views/`
- Shared layout/components: `frontend/web/components/`
- API wrappers, presentation, validation, and security helpers: `frontend/web/services/`
- Runtime/env configuration: `frontend/web/config/`

**API contract and backend integration details:**
- Endpoint matrix and schema snapshots: [`docs/PLANNING_DOCS/STAGE1_DOCS/API_STAGE1_CONTRACT.md`](./docs/PLANNING_DOCS/STAGE1_DOCS/API_STAGE1_CONTRACT.md)
- Architecture flow and page-to-endpoint route mapping: [`docs/PLANNING_DOCS/STAGE1_DOCS/API_STAGE1_CONTRACT.md`](./docs/PLANNING_DOCS/STAGE1_DOCS/API_STAGE1_CONTRACT.md)
- Local/deployed URL and API-prefix configuration guidance: [`docs/PLANNING_DOCS/STAGE1_DOCS/API_STAGE1_CONTRACT.md`](./docs/PLANNING_DOCS/STAGE1_DOCS/API_STAGE1_CONTRACT.md)

**Security/reliability controls implemented in Stage 1:**
- CSRF token verification on profile write paths.
- Allowlist-based validation/sanitization for filters and forms.
- Defensive response normalization for malformed/null backend fields.
- Safe fallback behavior for timeout, non-2xx, and malformed JSON responses.

**Verification evidence:**
- Stage 1 responsive and web-distinctness validation notes: [`docs/PLANNING_DOCS/STAGE1_DOCS/STAGE1_VERIFICATION_EVIDENCE.md`](./docs/PLANNING_DOCS/STAGE1_DOCS/STAGE1_VERIFICATION_EVIDENCE.md)
- Stage execution tracker and checklist completion: [`docs/TODO.md`](./docs/TODO.md)

#### Live Runtime Re-Validation (2026-03-17)

- **Web + backend integration sanity checks (live):**
	- `GET /api/v1/alerts/stats` returned `200 OK`
	- `GET /api/v1/summaries/latest` returned `200 OK`
	- `index.php`, `alerts.php`, `summaries.php`, and `profile.php` all returned `200 OK` from local PHP server (`127.0.0.1:8081`)
- **Backend test suite status (live run):**
	- Initial run: `71 passed, 5 failed, 3 errors` (all failures concentrated in `tests/test_api_users.py` due to bcrypt/passlib backend mismatch on password hashing)
	- Remediation applied: switched passlib context scheme from `bcrypt` to `pbkdf2_sha256` consistently in app and tests (`backend/api/users.py`, `backend/tests/test_api_users.py`, `backend/tests/conftest.py`)
	- Verification rerun: `79 passed, 0 failed, 0 errors`
	- Current status: backend suite is fully clean and Stage 1 runtime validation is complete.

### Additional Features and Extensions

As of 2026-03-17, the web extension has progressed beyond the initial Stage 1 baseline and now includes additional implemented features plus scaffolded extension surfaces:

- New web account flows:
	- `frontend/web/public/register.php`
	- `frontend/web/public/login.php`
- New detail views for read-path depth:
	- `frontend/web/public/alert_detail.php`
	- `frontend/web/public/summary_detail.php`
- Stage 2 kickoff integration page:
	- `frontend/web/public/risk.php` (wired to planned risk-score and prioritized-alert routes)
- Stage 3/4 scaffold pages for optional stretch work:
	- `frontend/web/public/map.php`
	- `frontend/web/public/forecast.php`
	- `frontend/web/public/assistant.php`

The web frontend setup and implementation details are maintained in `frontend/web/README.md`, which now documents:

- all current public routes and their behavior,
- service-layer request/normalization flow,
- configuration and local runtime guidance,
- security/validation controls,
- stage-status snapshot across implemented and scaffolded pages.


---


## Project Progress

### Certification of Original Work
The required Certification of Original Work is included in the [docs/CERTIFICATION.md](./docs/CERTIFICATION.md) file.

### Stages and Steps

See the full staged implementation plan here: [Project Stages](./docs/STAGES.md)
Track execution tasks here: [Project TODO Tracker](./docs/TODO.md)

Recommended update order when progress changes:
1. Update task/evidence rows in [docs/TODO.md](./docs/TODO.md)
2. Update stage narrative and deliverables in [docs/STAGES.md](./docs/STAGES.md)
3. Sync status table and summary notes in [README.md](./README.md)

`README.md` remains the source of truth for current stage status values.

### Current Stage Status

**Scope:** Stages 1-2 are **required** deliverables (target completion: April 29, 2026). Stages 3-4 are **optional stretch goals** if timeline permits.

| Stage | Title | Status | Last Updated | Scope | Notes |
|---|---|---|---|---|---|
| 1 | Web-App Extension | Completed | 2026-03-13 | **Required** | Stage 1 dashboard MVP, API integration layer, security/reliability controls, setup docs, and responsive/web-distinctness verification evidence are complete. See `docs/TODO.md`, `docs/PLANNING_DOCS/STAGE1_DOCS/API_STAGE1_CONTRACT.md`, and `docs/PLANNING_DOCS/STAGE1_DOCS/STAGE1_VERIFICATION_EVIDENCE.md`. |
| 2 | Environmental Risk Assessment and Alert Prioritization Extensions | In Progress | 2026-03-17 | **Required** | Kickoff plan + policy lock are documented in `docs/PLANNING_DOCS/PLANNING_STAGES.md` and `docs/PLANNING_DOCS/STAGE2_DOCS/STAGE2_IMPLEMENTATION_SPEC.md`; backend/web/mobile scaffolding is in place and S2-01/S2-05 are active. Target: Week of 2026-04-28. |
| 3 | Data Visualization and User Experience Extensions | Not Started | 2026-03-23 | Optional/Stretch | Stage 3 planning documents (API contract, verification evidence, implementation spec) created. Interactive Plotly-based risk map planned for web/mobile. |
| 4 | Predictive Analytics and AI-Driven Insights Extensions | Not Started | 2026-03-23 | Optional/Stretch | 24-48 hour forecasting + RiskRadar AI Assistant. Planned only if time permits after Stage 3. |
---

## Stage 3: Data Visualization and User Experience Extensions

**Objective:** Add an interactive risk map experience to help users explore and understand environmental risk conditions spatially.

**Implementation:**
- Stage 3 planning documents have been created in `docs/PLANNING_DOCS/STAGE3_DOCS/`:
	- `API_STAGE3_CONTRACT.md`: Defines the API contract for map and risk visualization endpoints, request/response schemas, and error handling.
	- `STAGE3_VERIFICATION_EVIDENCE.md`: Outlines verification checkpoints for map rendering, geospatial accuracy, responsive UX, and fallback/performance validation.
	- `STAGE3_IMPLEMENTATION_SPEC.md`: Details the implementation plan, policy lock, and step-by-step requirements for interactive risk map and user experience enhancements.

**Functionality:**
- New backend endpoints will provide geospatial alert and risk data for map rendering.
- Web and mobile clients will display interactive maps with overlays, clustering, and risk-level visual encoding.
- Fallbacks and error handling will keep the map UI interactive even if overlays fail to load.

**Execution:**
- The implementation will follow the contract and verification evidence, ensuring geospatial accuracy, responsive design, and accessibility.
- Performance and payload validation will be performed for map data endpoints.

**Importance:**
- This extension will make environmental risk data more accessible and actionable for users by providing spatial context and interactive exploration.
- It demonstrates advanced data visualization, geospatial API design, and user experience engineering, further differentiating the web extension from the mobile app.

**Status Legend**
- **Not Started**: Requirements are defined, but implementation has not begun.
- **In Progress**: Implementation is actively underway and may be partially complete.
- **Completed**: Implementation and verification are complete, with docs/tests updated as needed.
