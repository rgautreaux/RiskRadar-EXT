# CMPS 357 - Final Project - Group 3

Due Date: May 6, 2026, 12:55 CST

This repository contains the code and documentation for Group 3's CMPS 357 final project. The primary objective is to build a meaningful extension of our CMPS 490 RiskRadar senior project with new web-facing capabilities and advanced decision-support features.

Our senior project focuses on developing **RiskRadar**, an environmental risk awareness platform that helps residents and travelers identify and manage potential environmental risks using data analytics.

Our goal for the CMPS 357 final project is to build a unique web-app extension with a distinct frontend interface while extending the platform with features such as personalized risk assessment, interactive mapping, and predictive/AI-supported insights.

## Documentation Quick Links (Grading + Navigation)

- Requirements and scope: [docs/INSTRUCTIONS.md](./docs/INSTRUCTIONS.md)
- Stage-by-stage implementation plan: [docs/STAGES.md](./docs/STAGES.md)
- Execution tracker and evidence log: [docs/TODO.md](./docs/TODO.md)
- User walkthrough for web extension: [USER_GUIDE.md](./USER_GUIDE.md)
- Stage 1 API contract: [docs/API_STAGE1_CONTRACT.md](./docs/API_STAGE1_CONTRACT.md)
- Stage 1 verification evidence: [docs/STAGE1_VERIFICATION_EVIDENCE.md](./docs/STAGE1_VERIFICATION_EVIDENCE.md)
- Web app local setup: [frontend/web/README.md](./frontend/web/README.md)

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
| Stage 1 endpoint contract matrix | Route/method/input/output/fallback definitions and schema snapshots | `docs/API_STAGE1_CONTRACT.md` |
| Setup and run documentation | Configuration and local execution instructions for backend + PHP app | `frontend/web/README.md` |
| Verification evidence | Responsive and web-distinctness checkpoints with implementation signals | `docs/STAGE1_VERIFICATION_EVIDENCE.md`, `docs/TODO.md` |

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
- Endpoint matrix and schema snapshots: [`docs/API_STAGE1_CONTRACT.md`](./docs/API_STAGE1_CONTRACT.md)
- Architecture flow and page-to-endpoint route mapping: [`docs/API_STAGE1_CONTRACT.md`](./docs/API_STAGE1_CONTRACT.md)
- Local/deployed URL and API-prefix configuration guidance: [`docs/API_STAGE1_CONTRACT.md`](./docs/API_STAGE1_CONTRACT.md)

**Security/reliability controls implemented in Stage 1:**
- CSRF token verification on profile write paths.
- Allowlist-based validation/sanitization for filters and forms.
- Defensive response normalization for malformed/null backend fields.
- Safe fallback behavior for timeout, non-2xx, and malformed JSON responses.

**Verification evidence:**
- Stage 1 responsive and web-distinctness validation notes: [`docs/STAGE1_VERIFICATION_EVIDENCE.md`](./docs/STAGE1_VERIFICATION_EVIDENCE.md)
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


---


## Project Progress

### Certification of Original Work
The required Certification of Original Work is included in the [CERTIFICATION.md](./CERTIFICATION.md) file.

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
| 1 | Web-App Extension | Completed | 2026-03-13 | **Required** | Stage 1 dashboard MVP, API integration layer, security/reliability controls, setup docs, and responsive/web-distinctness verification evidence are complete. See `docs/TODO.md`, `docs/API_STAGE1_CONTRACT.md`, and `docs/STAGE1_VERIFICATION_EVIDENCE.md`. |
| 2 | Environmental Risk Assessment and Alert Prioritization Extensions | Not Started | 2026-03-17 | **Required** | Kickoff planning calendar is finalized in `docs/PLANNING_STAGES.md`; implementation remains not started. Target: Week of 2026-04-28. |
| 3 | Data Visualization and User Experience Extensions | Not Started | 2026-03-10 | Optional/Stretch | Interactive Plotly-based risk map. Planned only if Stage 2 completes early. |
| 4 | Predictive Analytics and AI-Driven Insights Extensions | Not Started | 2026-03-10 | Optional/Stretch | 24-48 hour forecasting + RiskRadar AI Assistant. Planned only if time permits after Stage 3. |

**Status Legend**
- **Not Started**: Requirements are defined, but implementation has not begun.
- **In Progress**: Implementation is actively underway and may be partially complete.
- **Completed**: Implementation and verification are complete, with docs/tests updated as needed.
