## Verification Snapshot (Latest)

- Latest full backend verification (`npm run verify:backend`): **198 passed** plus standalone smoke test pass (2026-04-11).
- Historical lower totals in older session entries are retained intentionally as time-stamped snapshots.

## Stage 5: Verified Map Closeout and Documentation Sync Session (2026-04-11)

### Implementation
Completed the final documentation synchronization pass after confirming the Stage 3 map closeout is verified and the evidence bundle is complete.

### Functionality
- Confirmed the interactive risk map is verifier-clean with the required S3-06 artifacts in place.
- Kept the map fix scoped to coordinate normalization so the demo renders correctly without broader UI churn.
- Brought the top-level stage summary into alignment with the verified map closeout state.

### Verification Evidence
- ✅ `npm run verify:evidence:s3` passes with all required files and links present.
- ✅ The map demo now resolves alert and risk geometry using backend payload shapes.
- ✅ Required Stage 3 artifacts are present under `static/evidence/`.

### Importance
- Establishes a clear verified endpoint for the Stage 3 map deliverable.
- Reduces ambiguity for graders by documenting the final working state.
- Keeps the stage summary consistent with the current repository evidence.

## Stage 5: Web-Only Scope Hardening and S3 Evidence Closeout Session (2026-04-11)

### Implementation
Executed a synchronized hardening pass for top-level docs to keep required CMPS 357 workflows backend+web only, then completed the S3-06 evidence artifact set required by the repository verifier.

### Functionality
- Clarified web-only required setup paths in top-level and execution documentation.
- Corrected top-level web startup command to PHP runtime serving flow.
- Retained mobile paths only as explicit reference-only guidance.
- Completed Stage 3 evidence artifact bundle at exact verifier-gated file paths.

### Verification Evidence
- ✅ Backend/web command-path sanity checks passed.
- ✅ `npm run verify:evidence:s3` passed with all artifacts and links complete.
- ✅ Final evidence verifier output reports no missing files and no missing links.

### Importance
- Reduces onboarding and grading friction caused by stale setup assumptions.
- Increases execution safety by aligning docs with actual repository architecture.
- Converts Stage 3 evidence closeout from pending to objectively verified completion.

## Stage 5: Rebecca Implementation Closeout and Max Handoff Session (2026-04-11)

### Implementation
Finalized Rebecca-owned remediation and documentation work, then formally handed off the remaining S3-06 manual evidence capture/final filing tasks to Max.

### Functionality
- No additional Rebecca-safe implementation items remain from the sprint remediation backlog.
- S3-06 manual capture/final filing ownership is now explicit in TODO, Stage 3 evidence docs, and closeout manifest.
- Automated evidence gate remains active via `npm run verify:evidence:s3`.

### Verification Evidence
- ✅ Top-level documentation synchronization completed.
- ✅ Manual closeout assignment for S3-06 documented as Max-owned.
- ✅ Evidence validator reports only missing manual artifacts (no missing-link defects).

### Importance
- Completes Rebecca's implementation scope cleanly without frontend overlap.
- Improves execution clarity for grading/onboarding handoff.

## Stage 5: Demo Verification Pass and FIRMS Warning Risk-Free Fix Session (2026-04-11)

### Implementation
Ran repeated demo verification passes (headless and presenter-visible) and implemented a minimal-risk registry fix so required-key checks use settings-loaded values from `.env` before process-environment fallback.

### Functionality
- **Demo Pass Validation:** `npm run demo:setup`, `npm run demo:verify`, and `npm run demo:info` consistently produced expected seeded outputs.
- **Automation Validation:** `npm run demo:run` and `npm run demo:report` completed successfully and regenerated walkthrough evidence files.
- **Warning Classification:** Confirmed FIRMS key warning is non-severe for seeded demo mode but relevant for live wildfire ingestion.
- **Configuration Hardening:** Updated scraper key resolution in `backend/scrapers/registry.py` to check settings values first, then environment variables.

### Execution
- Performed pre-pass setup/verification, executed walkthrough, regenerated report artifacts, and re-verified post-run consistency.
- Applied a localized backend fix to registry key checks without changing scraper behavior when keys are truly missing.
- Preserved demo-first safety by avoiding broader scheduler/scraper refactors.

### Verification Evidence
- ✅ Demo seed and verification counts remained stable (4 users, 15 alerts, 2 summaries).
- ✅ Automated walkthrough passed **6/6** steps in both headless and visible modes.
- ✅ Evidence files refreshed: `static/evidence/demo_journey_log.json`, `static/evidence/demo_screenshots/manifest.json`, `static/evidence/DEMO_REPORT.md`.
- ✅ Runtime registry import/load check passed after key-resolution update.

### Importance
- Increases confidence that demo workflows remain grading-ready across repeated runs.
- Removes avoidable false warning scenarios when keys are configured in `.env` but not shell-exported.
- Maintains low-risk operational posture by constraining the fix to key-lookup resolution logic.

## Stage 5: Sprint Remediation Implementation and Verification Closeout Session (2026-04-11)

### Implementation
Executed and closed the sprint remediation plan covering backend security hardening, datetime filtering correctness, frontend API portability, storage resilience improvements, map runtime path cleanup, and closeout documentation scaffolding.

### Functionality
- CORS origin policy now uses explicit configured origins.
- Feedback identity binding now derives from session context (no client-driven user spoofing path).
- Assistant and forecast time-window filtering now use parsed datetime comparisons across mixed timestamp formats.
- Golby and map API calls use runtime-configured API base values rather than fixed local assumptions.
- Golby localStorage access now falls back safely when storage is unavailable.
- Stage 3 evidence closeout scaffolding is prepared and linked for manual capture workflows.

### Verification Evidence
- ✅ Full backend verification command passed: **198 passed** (pytest) plus standalone scrape/summarize smoke test pass.
- ✅ Targeted assistant, forecast, and feedback suites remained green after remediation updates.
- ✅ Updated documentation links for S3-06 evidence bundle manifest and index are in place.

### Remaining Manual Task
- Stage 3 S3-06 screenshot/video artifact capture remains a manual evidence collection step owned by QA/onboarding workflow.

## Stage 5: Demo Workflow Sanity Pass and Documentation Synchronization Session (2026-04-11)

### Implementation
Executed a final repository-level sanity pass for demo setup, verification, and metadata reporting workflows, then synchronized top-level project documentation to reflect outcomes and decisions.

### Functionality
- **Demo Setup Validation:** `npm run demo:setup` creates and seeds demo data successfully from fixture inputs.
- **Demo Verification Validation:** `npm run demo:verify` confirms expected counts for users, alerts, and summaries.
- **Demo Metadata Validation:** `npm run demo:info` prints current seed metadata and token/user summaries.
- **Repository Hygiene:** `npm run demo:clean` removes generated `demo.db` and `seed_metadata.json` artifacts after validation.

### Execution
- Ran documented demo commands end-to-end and confirmed green outputs.
- Confirmed demo tooling under `backend/demo/` is actively referenced by package scripts and demo documentation.
- Preserved demo assets in version control to avoid breaking demo command workflows.
- Updated top-level tracking documents to keep chronology and status language aligned.

### Verification Evidence
- ✅ `npm run demo:setup` completed successfully.
- ✅ `npm run demo:verify` passed demo completeness checks.
- ✅ `npm run demo:info` returned expected metadata.
- ✅ `npm run demo:clean` removed generated artifacts.

### Importance
- Keeps demo documentation trustworthy by proving the published run commands execute as written.
- Reduces risk of accidental regressions from removing required demo tooling.
- Improves grading/onboarding readiness through synchronized, current top-level records.

## Stage 5: Golby Personality Learning, Communication Controls, and Cross-Device Sync Session (2026-04-10)

### Implementation
Built a complete soft-learning communication loop for Golby by extending existing assistant and feedback infrastructure. Added persistent user communication profiles, deterministic profile updates from feedback, explicit style-control commands, and frontend-to-backend profile synchronization while preserving guardrail-first safety behavior.

### Functionality
- **Persistent Profile:** Added `assistant_style_profile` on user records for warmth, calmness, humor, conciseness, detail, expandability, and learning metadata.
- **Feedback Learning:** Existing feedback endpoint now updates communication preferences using bounded, deterministic updates from reaction/rating/comment signals.
- **Profile-Aware Replies:** Assistant endpoint now shapes non-guardrail replies using learned profile values.
- **Style Directives:** Supports commands like “be shorter,” “more detail,” “be warmer,” “be goofy,” and “be calm,” with persistence for identified users.
- **Cross-Device Sync:** Frontend local Golby profile now syncs to backend user preferences after feedback updates.

### Execution
- Added backend service helpers in `backend/services/assistant_personality.py`.
- Extended `backend/db/models.py` and added migration `backend/db/migrations/2026-04-10_add_assistant_style_profile.sql`.
- Updated `backend/api/assistant.py`, `backend/api/feedback.py`, `backend/api/users.py`, and `backend/schemas/user.py`.
- Updated frontend Golby client integration in `frontend/web/components/golby/apiClient.ts` and `frontend/web/components/golby/ChatInterface.tsx`.
- Added/updated tests in `backend/tests/test_api_assistant.py`, `backend/tests/test_api_feedback.py`, and `backend/tests/test_api_users.py`.

### Verification Evidence
- ✅ Targeted suites: **27 passed** (assistant/feedback/users).
- ✅ Full backend suite: **196 passed, 0 failed**.

### Importance
- Improves assistant communication quality while keeping reliability and safety controls stable.
- Gives users explicit control over assistant style and allows preference carry-over across sessions/devices.
- Preserves deterministic behavior and maintainability by avoiding model retraining.

## Stage 5: Session-Based Authentication and Admin Gating Session (2026-04-10)

### Implementation
Replaced the hardcoded admin gate on feedback analytics (which accepted arbitrary `admin_user_id` query parameters from the browser) with a production-grade, cryptographically-signed session-based authentication system. Implemented HMAC-SHA256 signed session tokens stored in HttpOnly cookies with SameSite=Lax and scheme-aware secure flags. Wired the PHP login form and Golby widget to use the new session flow end-to-end.

### Functionality
- **Session Tokens:** HMAC-SHA256 signed tokens in format `payload.signature` using base64url encoding; tokens include user_id, issued-at, and expiration timestamps.
- **Auth Endpoints:** POST /auth/login (email+password → session token), GET /auth/me (session → authenticated user), POST /auth/logout (delete cookie).
- **Dependencies:** `require_admin_user()` (enforces admin role, 403 if not), `get_current_user()` (enforces auth, 401 if missing), `get_optional_current_user()` (returns user or None).
- **Admin Gating:** Feedback analytics (`/api/v1/feedback/analytics`, `/api/v1/feedback/weekly-report`) now require `require_admin_user()` dependency; arbitrary `admin_user_id` query params are rejected.
- **Frontend Login:** PHP form submission calls backend `/auth/login` endpoint; on success, session cookie is set and user is redirected to assistant.php.
- **Widget Authentication:** Golby widget calls `fetchCurrentUser()` on mount (GET /auth/me with `credentials: 'include'`); derives authenticated user state and displays in diagnostics panel.
- **API Client:** All widget fetch calls include `credentials: 'include'`; session cookie is automatically forwarded by browser.

### Execution
- **Backend Auth Layer:** Added `backend/auth/dependencies.py`, `backend/schemas/auth.py`, `backend/api/auth.py` with session extraction, login/logout, and current-user helpers.
- **Session Cryptography:** Enhanced `backend/auth/security.py` with `create_session_token()`, `verify_session_token()`, `_base64url_encode()`, `_base64url_decode()` functions.
- **API Routing:** Updated `backend/api/router.py` to expose auth_router before other endpoints; updated `backend/api/feedback.py` to use `require_admin_user()` dependency instead of query params.
- **CORS Middleware:** Updated `backend/main.py` to add `allow_credentials=True` to CORSMiddleware configuration.
- **Frontend Login:** Updated `frontend/web/public/login.php` to call backend auth endpoint, set session cookie, redirect on success.
- **Frontend Services:** Added `rr_set_session_cookie()` and `rr_clear_session_cookie()` helpers to `frontend/web/services/security.php`; updated `api_client.php` to forward session cookie.
- **Widget Integration:** Updated `ai-assistant-widget.jsx` to fetch `/auth/me` on mount; updated `ChatInterface.tsx` to accept `currentUserId` and display access level; updated `apiClient.ts` to include `credentials: 'include'` in all fetches.
- **Testing:** Added 3 auth tests (`test_api_auth.py`); updated 9 feedback tests to authenticate via session; corrected 401/403 expectations.

### Verification Evidence
- ✅ **191 backend tests passed** (full suite, no regressions).
- ✅ Auth endpoints: login returns token + user, logout clears session, me validates and returns user.
- ✅ Feedback analytics: 401 for unauthenticated, 403 for non-admin, accessible for admin with valid session.
- ✅ Widget: fetches `/auth/me` on mount, displays current user ID and access level, carries session cookie in all API calls.
- ✅ No hardcoded admin IDs from browser; all admin status derived from signed session token.

### Importance
- **Security Hardening:** Admin gate is now enforced server-side via cryptographically-signed session tokens, not through page attributes or query parameters.
- **Attack Surface Reduction:** Eliminates the risk of arbitrary `admin_user_id` values from the browser; admin status cannot be spoofed.
- **Compliance:** Replaces implicit, browser-passed admin flag with explicit, cryptographically-validated session-based authentication.
- **Production Readiness:** Session tokens include expiration, validation, and scheme-aware secure flag handling; suitable for deployment.

## Stage 5: User Data Security, Migration, and Full-Suite Verification Session (2026-04-02)

### Implementation
Added email encryption at rest for user records, deterministic email lookup hashing for duplicate checks, and stronger password policy enforcement during registration. A schema-aware migration script was added so existing plaintext emails can be converted safely.

### Functionality
- User emails are encrypted before storage and decrypted only for API responses.
- Duplicate email checks now use a deterministic lookup hash rather than plaintext comparison.
- Password policy enforcement rejects weak registration passwords before hashing.
- The migration script can handle older databases by adding the lookup column when needed.
- The backend suite was revalidated end to end and now passes 174/174 tests.

### Execution
- Added backend/auth/security.py for email encryption, hashing, and password helpers.
- Updated backend/api/users.py to validate password strength, encrypt emails, and serialize users safely.
- Added backend/scripts/migrate_emails_to_encrypted.py plus backend/db/migrations/2026-04-02_encrypt_user_emails.sql.
- Updated documentation in docs/INSTRUCTIONS.md and docs/SECURITY.md to capture setup and rollout order.
- Fixed the prioritized-alerts API endpoint so the full backend suite could complete successfully.

### Importance
- Protects user data at rest without breaking existing lookup behavior.
- Creates a repeatable migration path for existing deployments.
- Preserves the project's grading readiness by keeping the codebase verified and documented.

## Stage 5: Full Backend Verification Workflow and Documentation Sync Session (2026-04-02)

### Implementation
Added a repeatable backend verification workflow that combines the full pytest suite with a deterministic standalone smoke test. The smoke test was extended with mock-summary mode, and a Node wrapper was added so the repo-root npm script always uses the project virtual environment.

### Functionality
- `npm run verify:backend` runs the backend suite and smoke test together.
- `backend/test_scrape_and_summarize.py --mock-summary` validates the scraper/database path without requiring LLM credits.
- The smoke test now returns non-zero on validation failure so it can be used in CI or grading checks.

### Execution
- Added `backend/scripts/run_full_verification.py` as the orchestration entry point.
- Added `backend/scripts/run_full_verification.mjs` to resolve the repo `.venv` interpreter from npm.
- Updated the smoke test CLI and execution docs to support repeatable testing.

### Importance
- Provides a single canonical verification command for future maintenance and review.
- Improves reliability by avoiding system-Python drift and external billing dependencies.
- Keeps status, docs, and runtime validation aligned.
# Stage 4 Documentation Synchronization & Forecast UI Session (2026-04-02)

Summary:
- Verified and documented the completion of the Forecast UI, including local/manual location input, risk-type grouping, personalized advice, and user profile integration for sensitivities/preferences.
- Updated all top-level documentation (README, STAGES.md, TODO.md, AUTHORS.md, TRANSCRIPT.md, REFLECTION.md, USER_GUIDE.md) to reflect this session's developments and ensure full synchronization.
- Added a verbatim, word-for-word transcript of this session to TRANSCRIPT.md, ensuring all entries are unique and in correct chronological order.
- Updated REFLECTION.md with a summary of this session, the developments made, why they were made, and how it betters the project, as well as a summary of each TRANSCRIPT entry.
- Updated AUTHORS.md with each member's contributions and roles for this session.
- Expanded README.md and USER_GUIDE.md with new Forecast UI and personalization features, implementation details, and importance.

This ensures all documentation is in sync, the Forecast UI is fully documented, and the project is ready for grading and onboarding.
# Stage 4: AI Assistant Widget Integration & Documentation Sync Session (2026-03-31)

Summary:
- Integrated the React-based Golby AI Assistant widget into the PHP web frontend, resolving asset path and JS bundle issues.
- Updated assistant.php to mount the React widget and include all required assets (JS, CSS, SVG).
- Verified no syntax errors and confirmed frontend integration readiness.
- Synchronized all top-level documentation (README, STAGES.md, TODO.md, AUTHORS.md, TRANSCRIPT.md, REFLECTION.md) to reflect this session's developments.
- Added verbatim transcript and session summary to TRANSCRIPT.md and REFLECTION.md.
- Updated AUTHORS.md with member contributions and roles for this session.
- Expanded README.md with new AI Assistant integration details, implementation, and importance.

This ensures all documentation and the AI Assistant UI are in sync and ready for grading and onboarding.
# Stage 4: Forecast UI Completion & Documentation Update Session (2026-03-31)

Summary:
- Forecast UI implementation completed: supports local location default, manual input, risk-type grouping, personalized advice, and user profile integration for sensitivities/preferences.
- User profile UI now allows updating health sensitivities/preferences, which are used for tailored advice and recommendations.
- Backend and frontend are fully integrated for roundtrip updates.
- All documentation (README, STAGES.md, TODO.md, AUTHORS.md, TRANSCRIPT.md, REFLECTION.md) updated and synchronized for grading, onboarding, and historical accuracy.
- Verbatim transcript of this session added to TRANSCRIPT.md; REFLECTION.md updated with session summary and per-entry summaries.
- AUTHORS.md updated with member contributions and roles for this session.
- README.md and USER_GUIDE.md expanded with new Forecast UI and personalization features, implementation details, and importance.

This ensures all top-level documentation is in sync and the Forecast UI is fully implemented and documented for Stage 4.
## Stage 3: Data Visualization and User Experience Extensions (Completed 2026-03-31)

Summary:

This ensures all top-level documentation is in sync for grading, onboarding, and future development.
# Staged Development Plan for RiskRadar CMPS 357 Final Project

This document provides a complete, stage-by-stage implementation plan aligned with the required extension work in `docs/INSTRUCTIONS.md`. The format and structure follow the same style used in `EXAMPLE_STAGES.md` for consistency, readability, and professional reporting.

## Navigation Quick Links

- Stage 2 implementation spec: [PLANNING_DOCS/STAGE2_DOCS/STAGE2_IMPLEMENTATION_SPEC.md](./PLANNING_DOCS/STAGE2_DOCS/STAGE2_IMPLEMENTATION_SPEC.md)
- Stage 2 endpoint contract: [PLANNING_DOCS/STAGE2_DOCS/API_STAGE2_CONTRACT.md](./PLANNING_DOCS/STAGE2_DOCS/API_STAGE2_CONTRACT.md)
- Stage 2 verification evidence: [PLANNING_DOCS/STAGE2_DOCS/STAGE2_VERIFICATION_EVIDENCE.md](./PLANNING_DOCS/STAGE2_DOCS/STAGE2_VERIFICATION_EVIDENCE.md)
- This plan maps directly to Stages 1-4 in `docs/INSTRUCTIONS.md`.
- Stage progress markers should be updated as work is completed.

---

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
- **Stage 3**: Data Visualization and User Experience Extensions — ✅ Implementation Verified (2026-04-10)
   - Interactive risk map, personalized overlays, accessibility, and responsive UX fully implemented and verified.
   - Manual evidence bundle closeout remains as assignment for grading/onboarding team (S3-06 in `docs/TODO.md`).
   - Planning docs and verification checklist in `docs/PLANNING_DOCS/STAGE3_DOCS/`.
- **Stage 4**: Predictive Analytics and AI-Driven Insights Extensions — ✅ Completed (2026-04-10)
   - Forecast baseline backend and live forecast timeline integration are implemented and verified.
   - Assistant guardrails plus backend prompt/data integration are implemented and verified.
   - See `docs/PLANNING_DOCS/STAGE4_DOCS/`, `frontend/web/public/forecast.php`, `frontend/web/public/assistant.php`.
- **Stage 5**: Ongoing Maintenance, Advanced Features, and Review — ✅ Completed (2026-04-02)
   - Transitioned to ongoing maintenance and advanced feature development for the Risk Map Architecture.
   - All core features (backend region/bbox filtering, overlays, accessibility, navigation, documentation sync) are complete and verified.
   - Planned and documented next steps for user feedback, advanced overlays, analytics, refactoring, and continuous documentation/test updates.
   - Synchronized and updated all top-level documentation (README, STAGES.md, TODO.md, AUTHORS.md, TRANSCRIPT.md, REFLECTION.md) to reflect this session's developments.
   - Added verbatim transcript and session summary to TRANSCRIPT.md and REFLECTION.md.
   - Updated AUTHORS.md with member contributions and roles for this session.
   - Expanded README.md with new implementation, functionality, execution, and importance sections for ongoing maintenance and advanced features.

This ensures all documentation and the Risk Map Architecture are in sync, stable, and ready for future enhancements and grading.

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
🟡 **Implementation Complete; Evidence Closeout Ready** - Interactive risk map is fully implemented and verified via automated tests and runtime integration validation:

- Backend map endpoints implemented and CORS-enabled: `GET /api/v1/alerts/map`, `GET /api/v1/risk/map`, `GET /api/v1/risk/map/personalized/{user_id}`.
- Web frontend `map.php` fetches and renders live alert and risk overlay data from backend endpoints.
- Dynamic overlays with overlay toggles, region filters, legend, tooltips, and personalized user overlays.
- Keyboard/touch navigation, dark mode, and responsive layout implemented and verified.
- Accessibility improvements (ARIA, keyboard navigation, color contrast) applied.
- Fallback UI and error states handled gracefully; map remains interactive if overlays fail to load.
- Most evidence is organized and referenced in planning docs. Manual screenshot/recording bundle is ready for capture and assignment to grading/onboarding team roles (S3-06 task with concrete checklist in `docs/TODO.md`).
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
⏳ **In Progress** - Forecast UI, AI Assistant widget, and documentation sync/audit are underway. See README and TODO.md for current status.

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



