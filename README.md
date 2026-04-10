# Project Progress and Stage Summaries

## Stage 5: Golby Personality Learning, Communication Controls, and Cross-Device Sync Session (2026-04-10)

### Implementation
Implemented a complete Golby soft-learning loop by extending the existing assistant and feedback APIs with persistent communication profiles, bounded profile updates, explicit style controls, and frontend-to-backend sync.

### Functionality
- Added persistent `assistant_style_profile` per user for warmth, calmness, humor, conciseness, detail, and expandability.
- Updated feedback recording to convert reaction/rating/comment signals into deterministic profile updates.
- Updated assistant replies to use learned profiles for non-guardrail response shaping while keeping guardrail responses fixed.
- Added style command handling in assistant flow (for example: be shorter, more detailed, warmer, goofier, calmer).
- Synced frontend local Golby learning state to backend user preferences for cross-device continuity.

### Execution
- Backend updates: `backend/services/assistant_personality.py`, `backend/db/models.py`, `backend/api/assistant.py`, `backend/api/feedback.py`, `backend/api/users.py`, `backend/schemas/user.py`.
- Frontend updates: `frontend/web/components/golby/ChatInterface.tsx`, `frontend/web/components/golby/apiClient.ts`.
- Migration: `backend/db/migrations/2026-04-10_add_assistant_style_profile.sql`.
- Tests: extended assistant/feedback/users coverage for profile learning and style command persistence.

### Verification Evidence
- ✅ Targeted suites: **27 passed**.
- ✅ Full backend suite: **196 passed, 0 failed**.

### Importance
- Improved assistant friendliness and communication control without sacrificing accuracy, guardrails, or deterministic behavior.
- Enabled preference persistence and cross-device consistency for a better long-term user experience.

## Stage 5: Session-Based Authentication and Admin Gating Session (2026-04-10)

### Implementation
This session replaced the hardcoded admin gate on feedback analytics (which accepted arbitrary `admin_user_id` from the browser) with a real, cryptographically-signed session-based authentication system. Implemented HMAC-SHA256 signed session tokens stored in HttpOnly cookies, three auth endpoints (login/me/logout), and wired the PHP login form and Golby widget to use the new session flow.

### Functionality
- Users can log in via the PHP login form; backend issues a signed session token stored in an HttpOnly, SameSite=Lax cookie.
- Session tokens are HMAC-SHA256 signed with a base64url-encoded JSON payload, bound by expiration timestamp (configured via `ACCESS_TOKEN_EXPIRE_MINUTES`).
- Three auth endpoints: POST /auth/login (email+password → session token + user), GET /auth/me (session token → authenticated user), POST /auth/logout (delete session cookie).
- Dependency injection for session validation: `require_admin_user()` (enforces admin role, returns 403 if non-admin), `get_current_user()` (enforces authentication, returns 401 if missing), `get_optional_current_user()` (returns user or None).
- Feedback analytics endpoint now derives admin status from the session cookie; arbitrary `admin_user_id` query parameters are no longer accepted.
- Golby widget fetches `/auth/me` on mount and derives authenticated user state from the response, displaying current user ID and access level (Admin/Standard User) in diagnostics panel.
- All widget API calls carry the session cookie via `credentials: 'include'`; no hardcoded admin IDs are passed from the browser.

### Execution
- Added `backend/auth/dependencies.py` for session extraction and role-checking middleware.
- Added `backend/schemas/auth.py` for login request/response models.
- Added `backend/api/auth.py` with three auth endpoints and inline, scheme-aware cookie handling.
- Enhanced `backend/auth/security.py` with 100+ lines for `create_session_token()`, `verify_session_token()`, and base64url encoding helpers.
- Updated `backend/api/router.py` to expose auth_router before other endpoints.
- Migrated `backend/api/feedback.py` to use `require_admin_user()` dependency, replacing query-param admin_user_id.
- Updated `backend/api/assistant.py` to accept current-user from session via `get_optional_current_user()`.
- Updated `backend/main.py` CORS middleware to allow credentials: `allow_credentials=True`.
- Added `backend/auth/dependencies.py` for session extraction and role-checking.
- Enhanced PHP frontend: `frontend/web/services/security.php` with `rr_set_session_cookie()` and `rr_clear_session_cookie()` helpers.
- Updated `frontend/web/services/api_client.php` to forward session cookie and added `rr_login_user()` helper.
- Wired `frontend/web/public/login.php` form submission to backend auth endpoint with session cookie persistence and redirect.
- Updated `frontend/web/views/assistant.php` to render authenticated user state (`data-current-user-id`, `data-is-admin`) from `/auth/me` call.
- Modified `frontend/web/public/assets/ai-assistant-widget.jsx` to fetch `/auth/me` on mount and pass `currentUserId` to ChatInterface.
- Updated `frontend/web/components/golby/apiClient.ts`: all fetch calls now include `credentials: 'include'`, added `fetchCurrentUser()` helper.
- Fixed `frontend/web/components/golby/ChatInterface.tsx` to accept `currentUserId` instead of `adminUserId`, display authenticated access level in diagnostics.
- Added `backend/tests/test_api_auth.py` with 3 tests (login success, login rejection, logout).
- Updated `backend/tests/test_api_feedback.py` with session-based admin authentication; corrected expectation (401 for unauthenticated, 403 for non-admin).
- Updated `backend/tests/conftest.py` CORS to allow credentials.

### Verification Evidence
- ✅ **191 backend tests passed** (full suite, 2.66s, no regressions).
- ✅ Auth endpoints operational: login returns token + user, logout clears session, me validates session.
- ✅ Feedback analytics protected: 401 if unauthenticated, 403 if non-admin, accessible if admin authenticated via session.
- ✅ All API operations carry session cookie; no hardcoded admin IDs from browser.
- ✅ Frontend files: no syntax errors, TypeScript/JSX clean.
- ✅ Widget derives admin/user state from session on mount, displays in diagnostics panel.

### Importance
- **Security:** Admin gate is no longer a page attribute or query parameter; it is enforced server-side via cryptographically-signed session tokens.
- **Compliance:** Replaces the hardcoded admin ID gate with a real authentication system, eliminating the security risk of arbitrary admin_user_id from the browser.
- **User Experience:** Feedback recording remains open to all users; only admins can view analytics (enforced server-side, not client-side).
- **Grading Readiness:** All 191 backend tests pass; implementation is complete and verified.

## Stage 5: User Data Security, Migration, and Full-Suite Verification Session (2026-04-02)

### Implementation
This session added encrypted storage for user email addresses, deterministic lookup hashing for duplicate detection, and stronger password validation during registration. It also introduced a schema-aware migration path for existing plaintext emails and updated the documentation set to describe the rollout order.

### Functionality
- User emails are encrypted before being stored in the database.
- Duplicate email checks use a lookup hash instead of plaintext comparisons.
- Registration rejects weak passwords before they are hashed.
- The migration script can handle older databases and populate the new lookup column.
- The backend prioritization endpoint regression was fixed so the full suite can complete cleanly.

### Execution
- Added `backend/auth/security.py` and wired it into `backend/api/users.py`.
- Added `backend/scripts/migrate_emails_to_encrypted.py` for schema-aware batch migration.
- Added `backend/db/migrations/2026-04-02_encrypt_user_emails.sql` for schema alignment.
- Updated `docs/INSTRUCTIONS.md` and `docs/SECURITY.md` with deployment and key-management guidance.
- Re-ran the backend test suite after fixing the prioritized-alerts endpoint; the suite now passes 174/174 tests.

### Importance
- Reduces exposure of user email data at rest.
- Preserves existing user lookup behavior while improving privacy.
- Provides a repeatable rollout path for current and future deployments.
- Keeps the repository in a verified and grading-ready state.

## Stage 5: Full Backend Verification Workflow and Documentation Sync Session (2026-04-02)

### Implementation
Added a deterministic backend verification workflow that runs the full pytest suite and the standalone scraper/database smoke test in mock-summary mode. A small Node wrapper was added so the repo root npm script resolves the project virtual environment consistently on Windows and other platforms.

### Functionality
- `npm run verify:backend` runs backend pytest and the standalone smoke test from the repository root.
- The standalone smoke test now supports `--mock-summary` for deterministic, offline-friendly verification.
- The smoke test exits with a non-zero status when scraper or summary validation fails.
- The workflow preserves the live scraper/database path while avoiding paid LLM dependency for routine checks.

### Execution
- Added `backend/scripts/run_full_verification.py` to orchestrate the backend test suite and smoke test.
- Added `backend/scripts/run_full_verification.mjs` so the npm script uses the project `.venv` interpreter instead of system Python.
- Updated `backend/test_scrape_and_summarize.py` with CLI flags for mock summary, skip summary, and lookback control.
- Documented the new verification commands in `docs/PROGRAM_EXECUTION.md` and this README.

### Importance
- Gives the project a single repeatable verification command for future grading and maintenance.
- Keeps runtime smoke testing useful even when external LLM credits are unavailable.
- Reduces environment ambiguity by ensuring the repository uses the configured virtual environment.

## Stage 5: Ongoing Maintenance, Advanced Features, and Review Session (2026-04-02)

### Implementation
Transitioned to ongoing maintenance and advanced feature development for the Risk Map Architecture. All core features (backend region/bbox filtering, overlays, accessibility, navigation, documentation sync) are complete and verified. Next steps for user feedback, advanced overlays, analytics, refactoring, and continuous documentation/test updates are planned and documented.

### Functionality
- Risk Map Architecture is stable, extensible, and ready for advanced overlays and analytics.
- All core features are complete and verified, supporting future enhancements and user feedback.

### Execution
- Synchronized and updated all top-level documentation (README, STAGES.md, TODO.md, AUTHORS.md, TRANSCRIPT.md, REFLECTION.md) to reflect this session's developments.
- Added verbatim transcript and session summary to TRANSCRIPT.md and REFLECTION.md.
- Updated AUTHORS.md with member contributions and roles for this session.
- Expanded README.md with new implementation, functionality, execution, and importance sections for ongoing maintenance and advanced features.

### Importance
- Ensures all documentation and the Risk Map Architecture are in sync, stable, and ready for future enhancements and grading.
- Maintains project clarity, traceability, and grading readiness.
- Demonstrates best practices in documentation governance and collaborative development.

---
---
# CMPS 357 - Final Project - Group 3

Due Date: May 6, 2026, 12:55 CST

This repository contains the code and documentation for Group 3's CMPS 357 final project. The primary objective is to build a meaningful extension of our CMPS 490 RiskRadar senior project with new web-facing capabilities and advanced decision-support features.

Our senior project focuses on developing **RiskRadar**, an environmental risk awareness platform that helps residents and travelers identify and manage potential environmental risks using data analytics.

Our goal for the CMPS 357 final project is to build a unique web-app extension with a distinct frontend interface while extending the platform with features such as personalized risk assessment, interactive mapping, and predictive/AI-supported insights.

---

## Prerequisites

Before you start, make sure you have these installed on your machine:

| Tool        | Version | How to check         | How to install |
|-------------|---------|----------------------|----------------|
| **Python**  | 3.10+   | `python --version` or `py --version` | [python.org/downloads](https://www.python.org/downloads/) — check "Add to PATH" during install |
| **Node.js** | 18+     | `node --version`     | [nodejs.org](https://nodejs.org/) — LTS version recommended |
| **npm**     | 9+      | `npm --version`      | Comes with Node.js |
| **Git**     | any     | `git --version`      | [git-scm.com](https://git-scm.com/) |

> **Windows users:** Use `py` instead of `python3`. If `py` doesn't work, reinstall Python from [python.org](https://www.python.org/downloads/) and check **"Add Python to PATH"** during installation.

---

## Quick Start / Setup Guide

### 1. Clone the repository

```bash
git clone https://github.com/your-org/Team6Project.git
cd Team6Project
```

### 2. Set up environment variables

Copy the example environment file and fill in required values:

```bash
copy .env.example .env   # Windows
cp .env.example .env     # Mac/Linux
```

Edit `.env` and set at minimum:

```
# REQUIRED — generate with: py -c "import secrets; print(secrets.token_hex(32))"
JWT_SECRET_KEY=paste-your-random-secret-here

# REQUIRED for AI summaries (get a key from https://platform.deepseek.com/)
LLM_PROVIDER=deepseek
LLM_MODEL=deepseek-chat
LLM_API_KEY=your-deepseek-api-key

# OPTIONAL — for air quality data (free key from https://docs.airnowapi.org/account/request/)
AIRNOW_API_KEY=your-airnow-key
```

### 3. Start the Backend

```bash
cd backend
py -m pip install -r requirements.txt
py -m uvicorn main:app --host 0.0.0.0 --port 8000
```

You should see:

```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

Verify it works by opening http://localhost:8000/docs in your browser (Swagger API docs).

### 4. Start the Web Frontend

```bash
cd frontend/web
npm install
npm run dev
```

### 5. Start the Mobile Frontend (Expo)

```bash
cd frontend/mobile/RiskRadar
npm install
npx expo start
```

Then press:
- **`w`** to open in your web browser
- **Scan the QR code** with the Expo Go app on your phone (same WiFi network)

> **Important:** The mobile app auto-detects your computer's IP address so it can reach the backend. Both devices must be on the same WiFi network.

---

## Common Issues

| Problem | Solution |
|---------|----------|
| `'py' is not recognized` | Install Python from [python.org](https://www.python.org/downloads/), check "Add to PATH" |
| `'uvicorn' is not recognized` | Use `py -m uvicorn` instead of `uvicorn` directly |
| Backend says `402 Insufficient Balance` | Your LLM API key (DeepSeek) has no credits — add funds or skip summary generation |
| Weather report shows wrong location | Make sure you're entering a valid 5-digit US zip code |
| Frontend can't connect to backend | Both devices must be on the same WiFi; backend must be running with `--host 0.0.0.0` |
| `ModuleNotFoundError` | Run `py -m pip install -r requirements.txt` in the backend folder |
| Expo QR code won't scan | Press `w` to test on web first; make sure Expo Go app is installed on phone |
| Registration fails silently | Check the backend terminal for error messages |

---

## Full Backend Verification (One Command)

Run this from the repository root to execute both backend `pytest` and a deterministic
integration smoke test that does not require paid LLM credits:

```bash
npm run verify:backend
```

---

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

# Project Progress and Stage Summaries

## Stage 1: Web-App Extension (Completed)

See [Project Stages](./docs/STAGES.md) and [Project TODO Tracker](./docs/TODO.md) for full details.

### Major Developments

- Web architecture and API contract formalization
- Dedicated PHP web-app scaffold under `frontend/web/`
- Backend integration and normalization layer
- Dashboard-first web UI with scaffolded core views
- Security and reliability hardening for web write paths
- Stage 1 setup and verification documentation

### Implementation
See "Deliverables" and "Implementation" in [README.md](./README.md) and [docs/PLANNING_DOCS/STAGE1_DOCS/).

### Functionality
- Dashboard with alert stats, top alerts snapshot, and latest summary panel
- Alerts explorer with filter controls and safe empty-state behavior
- Summaries archive with summary-type/limit filtering and defensive rendering
- Profile write-path scaffolding for register and preference updates

### Execution
- All features implemented and verified as of 2026-03-13
- Backend suite is fully clean and Stage 1 runtime validation is complete

### Importance
- Foundation for all subsequent stages and extensions
- Ensures grading readiness and onboarding clarity

---

## Stage 2: Environmental Risk Assessment and Alert Prioritization Extensions (Completed)

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

---

## Stage 3: Data Visualization and User Experience Extensions (Completed)

### Implementation
Stage 3 introduced an interactive risk map and enhanced user experience features. The backend and frontend were prepared for new geoJSON endpoints, map rendering logic, and responsive UX improvements. Planning documents (API contract, verification evidence, implementation spec) were created to lock requirements and guide development. The implementation included:
- Dynamic data integration for map overlays (alerts, risk, AQI, wildfires)
- Personalized map overlays with user ID input and toggle
- Accessibility improvements (ARIA, keyboard navigation, color contrast)
- Responsive design for desktop, tablet, and mobile
- Robust error handling and fallback UI
- Evidence collection and onboarding documentation

### Functionality
- Interactive risk map with real-time overlays for environmental hazards
- Personalized overlays based on user ID
- Overlay toggles, region filters, and legend/tooltips
- Keyboard and touch navigation, dark mode, and responsive layout
- User-friendly error/fallback states

### Execution
All features were implemented in a stepwise, checklist-driven process. Each phase (requirements verification, documentation, evidence, onboarding) was completed and progress was summarized in all relevant documentation files. Documentation, evidence, and onboarding materials were synchronized and deduplicated for grading and onboarding clarity.

### Importance
Stage 3 elevates RiskRadar by providing spatial context and visual decision support, making risk information more actionable and accessible for all users. The documentation synchronization ensures that all contributors and reviewers have a single source of truth for project status and history.

---

## Stage 4: Predictive Analytics and AI-Driven Insights Extensions (Completed)

### Implementation
Stage 4 now includes a baseline forecast backend implementation and a live forecast UI integration. The backend forecast endpoint returns 24-48 hour forecast points, confidence, trend, and summary fields derived from active alert signals and user sensitivity context. The forecast page now renders live timeline output and fallback regional risk states.

This session also executed a comprehensive Stage 4 planning and documentation update, including:
- Creating and cross-linking Stage 4 planning docs: Implementation Spec, Verification Evidence, API Contract, and Golby Icon Plan
- Planning and documenting Golby AI Assistant icon/visuals asset integration (ai-assistant.svg, RiskRadar_Assistant_Icon.png)
- Adding navigation links and asset references to all Stage 4 planning docs
- Updating Master Task Tracker and Weekly Check-In Log for Stage 4 kickoff
- Synchronizing and auditing all top-level documentation for Stage 4

### Functionality
- Forecast UI supports local and manual location input, risk-type grouping, personalized advice, and user profile integration for sensitivities/preferences.
- User profile UI allows updating health sensitivities/preferences, which are used for tailored advice and recommendations.
- Forecast backend and frontend are integrated for live timeline updates.
- Forecast responses now include `forecast_points`, `confidence`, `trend`, `summary`, and `baseline_risk_score` fields.
- Golby assistant now applies guardrail checks for medical/legal/emergency/harmful requests and returns safe fallback guidance.
- Ensures all Stage 4 planning, asset integration, and documentation are fully documented and traceable
- Provides a clear audit trail of all major project decisions and technical enhancements for Stage 4
- Maintains a single source of truth for project status and history

### Execution
- All documentation (README, STAGES.md, TODO.md, AUTHORS.md, TRANSCRIPT.md, REFLECTION.md, USER_GUIDE.md) updated and synchronized for grading, onboarding, and historical accuracy.
- Verbatim transcript of this session added to TRANSCRIPT.md; REFLECTION.md updated with session summary and per-entry summaries.
- AUTHORS.md updated with member contributions and roles for this session.
- README.md and USER_GUIDE.md expanded with new Forecast UI and personalization features, implementation details, and importance.
- Added `backend/tests/test_api_forecast.py`; targeted forecast API tests pass (2/2).
- Updated `docs/SECURITY.md` with assistant guardrail scope, out-of-scope classes, and fallback policy.
- All documentation files were updated in a coordinated sequence for grading, onboarding, and future development clarity
- Each phase of the Stage 4 documentation update was tracked and summarized in the relevant files

### Importance
- Ensures the Forecast UI is fully implemented, user-personalized, and documented for grading and onboarding.
- Maintains project clarity, traceability, and grading readiness.
- Demonstrates best practices in documentation governance and collaborative development
- Maintains project clarity, traceability, and grading readiness for Stage 4
- Ensures all contributors and reviewers have a single source of truth for project status and history
- Demonstrates best practices in documentation governance and collaborative development

**Relevant Stage 4 Planning Docs:**
- [API_STAGE4_CONTRACT.md](docs/PLANNING_DOCS/STAGE4_DOCS/API_STAGE4_CONTRACT.md)
- [STAGE4_IMPLEMENTATION_SPEC.md](docs/PLANNING_DOCS/STAGE4_DOCS/STAGE4_IMPLEMENTATION_SPEC.md)
- [STAGE4_VERIFICATION_EVIDENCE.md](docs/PLANNING_DOCS/STAGE4_DOCS/STAGE4_VERIFICATION_EVIDENCE.md)
- [GOLBY_ICON_PLAN.md](docs/PLANNING_DOCS/STAGE4_DOCS/GOLBY_ICON_PLAN.md)

**Asset References:**
- `ai-assistant.svg` (SVG icon)
- `RiskRadar_Assistant_Icon.png` (PNG icon)

**See also:** [PLANNING_STAGES.md](docs/PLANNING_DOCS/PLANNING_STAGES.md), [TODO.md](docs/TODO.md), [STAGES.md](docs/STAGES.md)

## Stage 3/4 Implementation Verification and Closeout Session (2026-04-10)

### Implementation
Executed a comprehensive verification and closeout session validating Stage 3 and Stage 4 implementations against live backend and frontend. Fixed runtime environment schema drift and assistant integration compatibility issues. Applied corrections and revalidated all systems cleanly.

### Functionality
- **Frontend Forecast Integration:** Verified that forecast page renders live API data with deterministic forecast points, confidence, trend, and summary fields.
- **Assistant Guardrails:** Confirmed guardrail detection for medical/legal/emergency/harmful requests returns safe fallback responses.
- **Runtime Environment:** Corrected local test database schema to include `users.email_lookup_hash` and `users.health_conditions` columns required by user registration flow.
- **Additional Backend Routes:** Validated newer assistant endpoint for response generation with live alert/forecast data integration.

### Execution
- Ran focused frontend verification pass exercising Forecast and Assistant API endpoints against live backend server.
- Confirmed payload rendering, guardrail behavior, and error handling in end-to-end runtime scenarios.
- Applied database schema migrations and fixed assistant widget mount attribute compatibility.
- Revalidated targeted backend tests (assistant, feedback APIs: 12 passed).
- Executed full backend verification: **191 tests passed in 3.09s**, smoke test passed.
- Updated Stage 3 and Stage 4 verification docs with concrete evidence capture checklist for manual closeout task (S3-06).

### Importance
- Ensures all implemented Stage 3 and Stage 4 features are verified and validated in production-like conditions.
- Resolves runtime environment issues that were blocking live browser/API smoke tests.
- Provides grading-ready documentation reflecting accurate completion status for both stages.
- Establishes clear, actionable evidence collection requirements for final stage closeout.
- Maintains project stability and prevents environment-specific test failures from masking real issues.

---

# Current Stage Status Table

**Scope:** Stages 1-2 are **required** deliverables (target completion: April 29, 2026). Stages 3-4 are **optional stretch goals** if timeline permits.

| Stage | Title | Status | Last Updated | Scope | Notes |
|---|---|---|---|---|---|
| 1 | Web-App Extension | ✓ Completed | 2026-03-13 | **Required** | Stage 1 dashboard MVP, API integration layer, security/reliability controls, setup docs, and responsive/web-distinctness verification evidence are complete. See `docs/TODO.md`, `docs/PLANNING_DOCS/STAGE1_DOCS/API_STAGE1_CONTRACT.md`, and `docs/PLANNING_DOCS/STAGE1_DOCS/STAGE1_VERIFICATION_EVIDENCE.md`. |
| 2 | Environmental Risk Assessment and Alert Prioritization Extensions | ✓ Completed | 2026-03-24 | **Required** | Risk scoring engine, smart alert prioritization, and all required endpoints, schemas, and tests are implemented and verified. See `docs/PLANNING_DOCS/STAGE2_DOCS/`, `docs/TODO.md`. |
| 3 | Data Visualization and User Experience Extensions | ✓ Completed | 2026-04-10 | Optional/Stretch | Interactive risk map, personalized overlays, accessibility, and responsive UX are fully implemented and verified. All automated tests pass (191/191). Frontend and API endpoints validated in end-to-end runtime. See `docs/PLANNING_DOCS/STAGE3_DOCS/`, `frontend/web/public/map.php`. |
| 4 | Predictive Analytics and AI-Driven Insights Extensions | ✓ Completed | 2026-04-10 | Optional/Stretch | Forecast baseline backend + live forecast timeline integration fully implemented and verified in end-to-end runtime. Assistant guardrails, backend prompt, and data integration implemented and validated with 12/12 targeted API tests passing. See `docs/PLANNING_DOCS/STAGE4_DOCS/`, `frontend/web/public/forecast.php`, `frontend/web/public/assistant.php`. |
---

# Certification of Original Work

The required Certification of Original Work is included in the [docs/CERTIFICATION.md](./docs/CERTIFICATION.md) file.

# Additional Project Content

See below for legacy content, architecture, and further details.


###### Implementation
Stage 3 planning introduced an interactive risk map and enhanced user experience features. The backend and frontend were prepared for new geoJSON endpoints, map rendering logic, and responsive UX improvements. Planning documents (API contract, verification evidence, implementation spec) were created to lock requirements and guide development.

###### Functionality
- **Interactive Risk Map:** Users will be able to view environmental risks on a map, with real-time overlays for AQI, wildfires, and weather alerts.
- **Responsive UX Enhancements:** Improved mobile and web interfaces for better accessibility and usability.

###### Execution
Stage 3 deliverables are planned and documented, with implementation to follow the locked contract and verification evidence. All planning artifacts are synchronized across top-level documentation for grading and onboarding clarity.

###### Importance
Stage 3 will further elevate RiskRadar by providing spatial context and visual decision support, making risk information more actionable and accessible for all users.

---

## Project Content
# Major Developments: Implementation, Functionality, Execution, and Importance

## Stage 3 Documentation and Synchronization Session (2026-04-27)

### Implementation
This session executed a comprehensive documentation update and synchronization pass for Stage 3. The work included:
- Appending a verbatim transcript of the session to TRANSCRIPT.md, ensuring all entries are unique
- Summarizing each transcript entry in REFLECTION.md
- Updating AUTHORS.md with current contributions and roles
- Adding README sections on implementation, functionality, execution, and importance of major project developments
- Reviewing and updating all top-level documentation for consistency and agreement

### Functionality
- Ensures all UI/UX, accessibility, and design system improvements are fully documented and traceable
- Maintains project clarity, traceability, and grading readiness
- Provides a clear audit trail of all major project decisions and technical enhancements

### Execution
- All documentation files were reviewed and updated for consistency and agreement
- Transcript and reflection entries were deduplicated and summarized
- Authors and roles were updated to reflect current contributions

### Importance
- Ensures all contributors and reviewers have a single source of truth for project status and history
- Demonstrates best practices in documentation governance and collaborative development
- Improves grading and onboarding clarity for new contributors and reviewers
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
| 2 | Environmental Risk Assessment and Alert Prioritization Extensions | Completed | 2026-03-24 | **Required** | Risk scoring engine, smart alert prioritization, and all required endpoints, schemas, and tests are implemented and verified. See `docs/PLANNING_DOCS/STAGE2_DOCS/`, `docs/TODO.md`. |
| 3 | Data Visualization and User Experience Extensions | Completed | 2026-03-31 | Optional/Stretch | Interactive risk map, personalized overlays, accessibility, and responsive UX implemented and verified. See `docs/PLANNING_DOCS/STAGE3_DOCS/`, `frontend/web/public/map.php`. |
| 4 | Predictive Analytics and AI-Driven Insights Extensions | Completed | 2026-04-10 | Optional/Stretch | Forecast baseline backend + live forecast timeline integration are implemented and verified; assistant guardrails/backend prompt/data integration are implemented and validated with targeted API tests. See `docs/PLANNING_DOCS/STAGE4_DOCS/`, `frontend/web/public/forecast.php`, `frontend/web/public/assistant.php`. |
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


Stage Implementation
