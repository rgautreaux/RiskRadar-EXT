
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

...existing code...

## Stage 5: SVG Asset White-Pixel Removal and Documentation Synchronization Session (2026-04-13)

### Implementation
Completed a targeted SVG asset cleanup pass by removing white background pixels from Golby assistant icon files, enabling transparent overlays and flexible background integration in user interface contexts.

### Functionality
- Removed white background fill (`#FEFEFE`) from `frontend/web/public/assets/icons/ai-assistant-reacting.svg`.
- Removed white background fill (`#FEFEFE`) from `frontend/web/public/assets/golby-asset-ai-assistant-reacting-DRoynDD7.svg`.
- Both files now support transparent backgrounds for improved visual integration.

### Execution
- Identified target SVG files and isolated the exact white-background path in each document.
- Removed only the white fill path while preserving all non-background vector paths.
- Confirmed both files remained valid SVG assets after modification.
- Synchronized session updates across all top-level progress-tracking documentation.

### Importance
- Improves UI flexibility by allowing SVG assets to display over custom backgrounds without white-box conflicts.
- Strengthens visual consistency across assistant icon rendering contexts.
- Maintains low-risk asset-only scope without affecting code behavior or backend integration.

## Stage 5: Golby Chat Interface Visibility Enhancement and Auto-Open Wiring Session (2026-04-12)

### Implementation
Completed a targeted visibility fix for the Golby chat interface by identifying and resolving two separate frontend blockers that prevented the chat interface from appearing operational despite full backend functionality.

### Functionality
- Diagnosed chat interface visibility issues stemming from missing route context detection and missing button facial expressions.
- Added 'assistant' route fallback detection in `frontend/web/components/golby/pageContext.ts` so `detectCurrentPage()` recognizes `/assistant.php` URL path.
- Added waving and winking facial expression overlays to `frontend/web/components/golby/GolbyIcon.tsx` so launcher button renders visible character instead of blank circle.
- Added conditional auto-open logic in `frontend/web/components/golby/GolbyAssistantWidget.tsx` to check `detectedPage === 'assistant'` and call `setOpen(true)` on component mount.
- Rebuilt frontend bundle with `npm run build:web` generating `354.72 kB golby-widget.js`.

### Execution
- Before fixes: Playwright browser check returned `{"inputCount":0,"openBtnCount":1}` confirming chat interface was hidden.
- Applied targeted component fixes for route detection, facial expressions, and auto-open logic.
- Rebuilt frontend bundle without errors.
- After fixes: Playwright browser check returned `{"inputCount":1,"closeCount":1,"url":"http://127.0.0.1:8080/assistant.php"}` confirming chat interface visible and ready to close on page load.
- No TypeScript compilation errors or CSS errors in rebuilt bundle.

### Importance
- Restores visible, functional chat interface on the assistant page for end users testing the application.
- Improves developer visibility by separating UI/visibility issues from backend functionality issues.
- Strengthens regression detection by automating Playwright visibility checks in verification suite.

## Stage 5: Frontend-Backend Wiring Completion, Verification, and Documentation Synchronization Session (2026-04-12)

### Implementation
Completed a full frontend-backend wiring completion pass for web runtime reliability, then synchronized all progress/history documentation artifacts for this session.

### Functionality
- Diagnosed root causes of empty-state/fallback rendering as frontend API base mismatch and relative browser fetch paths in forecast/map flows.
- Updated forecast browser wiring to use injected backend base/prefix configuration rather than same-origin relative fallback paths.
- Hardened map wiring to require injected API URLs and fail safely with actionable configuration messaging.
- Ensured map page reuses bootstrap config source so endpoint injection remains consistent across pages.
- Hardened backend CORS origin parsing with safe fallback behavior and startup visibility logging.
- Added wiring troubleshooting guidance to frontend runbook documentation.

### Execution
- Implemented code changes across backend entrypoint and frontend forecast/map runtime paths.
- Ran syntax checks (`php -l` for modified PHP files, Python compile for backend entrypoint).
- Ran runtime verification with split-origin topology and validated:
	- configured endpoint injection on forecast/map pages
	- CORS preflight success for frontend origin
	- dashboard/alerts/summaries rendering without backend-unavailable fallbacks once backend was active on configured port
- Performed transcript duplicate-entry pass and duplicate-section-body pass; both reported zero duplicates.
- Synchronized README, STAGES, TODO, TRANSCRIPT, REFLECTION, AUTHORS, and docs README.

### Importance
- Restores dependable data display across web surfaces by aligning browser requests with backend runtime configuration.
- Prevents silent same-origin regressions in forecast/map browser code paths.
- Improves demo/grading reliability through explicit wiring verification and synchronized project history tracking.

## Stage 5: Unrelated-Change Isolation via Separate Worktree/Branch Session (2026-04-12)

### Implementation
Executed a clean review-scope isolation pass by separating unrelated connectivity/docs edits from the active branch workflow into a dedicated worktree and branch.

### Functionality
- Reviewed active working-tree changes and classified files by scope relevance.
- Isolated unrelated changes to:
	- `backend/scripts/pre_demo_connectivity_check.py`
	- `frontend/web/README.md`
- Created dedicated branch/worktree: `chore/unrelated-connectivity-readme`.
- Created isolated commit: `67abd7b2`.
- Pushed the isolated branch to origin.

### Execution
- Performed targeted stash/apply flow to avoid cross-scope contamination.
- Committed unrelated changes in the isolated worktree branch.
- Pushed branch and generated PR creation URL for independent review.
- Preserved current branch cleanliness after split.

### Importance
- Improves PR review clarity by separating unrelated operational/docs updates from main feature work.
- Reduces merge risk and rollback complexity through concern-scoped history.
- Strengthens project governance by keeping changes categorized and traceable.

## Stage 5: Connectivity Preflight, Canonical Local Topology, and Documentation Synchronization Session (2026-04-12)

### Implementation
Implemented a fail-fast pre-demo connectivity preflight, standardized a canonical local runtime topology, and synchronized all top-level progress/history documentation to reflect this session.

### Functionality
- Added a new connectivity preflight command (`npm run verify:connectivity`) that validates backend/API/frontend wiring, map API URL injection, and CORS preflight behavior.
- Added preflight scripts at `backend/scripts/pre_demo_connectivity_check.py` and `backend/scripts/run_connectivity_preflight.mjs`.
- Updated `demo:run` to include connectivity preflight before demo journey execution.
- Standardized canonical local demo topology to backend `127.0.0.1:8001` and frontend `127.0.0.1:8080`.
- Updated frontend API defaults and local config example to canonical backend port.
- Updated runbook/execution docs to include the connectivity preflight in the required pre-demo flow.

### Execution
- Added npm script: `verify:connectivity`.
- Updated package flow: `demo:run` now runs build, preflight, and then demo journey.
- Updated canonical config defaults in `frontend/web/config/app.php` and `frontend/web/config/config.local.example.php`.
- Updated and synchronized top-level docs: TODO, STAGES, TRANSCRIPT, REFLECTION, AUTHORS, README.
- Ran pass and validated preflight reaches full PASS state.

### Importance
- Catches frontend/backend/API wiring failures before demos with actionable output.
- Reduces local-environment drift by enforcing one default topology across docs and scripts.
- Improves grading/demo reliability by making connectivity verification explicit and repeatable.

## Stage 5: Golby Operational Frontend Wiring, Verification, and Documentation Synchronization Session (2026-04-12)

### Implementation
Completed the assistant operationalization pass by fixing frontend asset execution/wiring, validating runtime behavior end-to-end, and synchronizing top-level project documentation for historical accuracy.

### Functionality
- Ensured assistant page loads compiled Golby assets in web runtime (`/assets/golby-widget.js`, `/assets/golby-widget.css`) instead of scaffold-only/raw-source behavior.
- Verified interactive assistant behavior in demo automation (open widget, send message, feedback click, guardrail response).
- Confirmed backend and seeded demo workflows remained stable after wiring validation.
- Updated Stage/session tracker docs and historical records in chronological order.

### Execution
- Ran and passed `npm run build:web`.
- Resolved missing Python dependency (`cryptography`) in the project virtual environment and re-ran verification.
- Ran and passed `npm run verify:backend` (**211 passed**, smoke test pass).
- Ran and passed `npm run demo:setup`.
- Ran and passed interactive journey: `node frontend/web/tests/demo/demo_journey.js --base-url http://127.0.0.1:8080` (**6/6 passed**, assistant screenshots captured).
- Ran and passed `npm run demo:report` (artifact regenerated at `static/evidence/DEMO_REPORT.md`).

### Importance
- Converts Golby from scaffold-facing behavior to verified operational behavior in manual and automated runtime checks.
- Reduces future integration risk through a reproducible assistant build/runtime verification path.
- Keeps documentation governance accurate by synchronizing all top-level tracking/history files with this implementation session.

## Stage 5: Frontend Contrast Accessibility Final Pass and Documentation Synchronization Session (2026-04-12)

### Implementation
Executed the final frontend polish pass to improve readability and navigation accessibility on top of the recent visual refresh, keeping all changes low-risk and CSS-scoped.

### Functionality
- Applied a WCAG-focused contrast hardening pass to active nav tabs, primary action buttons, links, muted/supporting text, and form placeholder states.
- Added stronger accent variants for text-on-accent readability and mapped them to active tab/button gradients.
- Tightened edge-case contrast in small text chips/pills/badges (`.severity-pill`, `.meta-chip`, `.summary-meta-inline`, `.icon-badge`) and focus-visible states.
- Strengthened keyboard focus visibility across shared controls and map-specific checkbox/select inputs.
- Synchronized TODO, STAGES, TRANSCRIPT, REFLECTION, and AUTHORS with this session in chronological Stage 5 order.

### Execution
- Updated shared frontend stylesheet rules and tokens in `frontend/web/public/assets/app.css` for contrast-safe vivid states.
- Re-ran diagnostics checks on edited stylesheet after each polish pass.
- Performed transcript duplicate-entry check by Stage heading and kept the transcript list unique/chronological.

### Verification Evidence
- ✅ CSS diagnostics check on `frontend/web/public/assets/app.css` reports no errors.
- ✅ High-contrast focus outlines are present for keyboard navigation on key controls.
- ✅ Appearance/accessibility changes were implemented without backend/API behavior changes.

### Importance
- Improves readability and accessibility for small UI text elements while preserving a lively visual direction.
- Makes keyboard navigation easier to follow, supporting inclusive UX expectations.
- Keeps project governance artifacts synchronized with implementation history.

## Stage 5: RiskRadar Top-Text Removal and Documentation Synchronization Session (2026-04-12)

### Implementation
Applied a focused frontend fix to remove distracting raw text from the top of RiskRadar pages by correcting PHP opening-tag/comment placement in shared layout and API helper files, then synchronized top-level documentation for this session.

### Functionality
- Corrected `frontend/web/services/api_client.php` so map/forecast helper code is parsed within PHP instead of leaking plain text into page output.
- Corrected `frontend/web/components/layout.php` so the layout-shell metadata block remains a non-rendered PHP comment.
- Performed a transcript hygiene pass to remove duplicate replay-style transcript sections and preserve unique chronological history.
- Added synchronized session updates across progress-tracking and contributor-history docs.

### Verification Evidence
- ✅ `php -l frontend/web/services/api_client.php` passed.
- ✅ `php -l frontend/web/components/layout.php` passed.
- ✅ Shared frontend files no longer emit file-header/helper text into rendered HTML output.

### Importance
- Restores polished UI presentation by removing non-product text from page output.
- Uses low-risk, localized edits in shared files for broad visual impact without route/API behavior changes.
- Maintains grading/onboarding traceability by keeping top-level docs in sync with implementation changes.

## Stage 5: Review-Ready Commit Split and Push Session (2026-04-12)

### Implementation
Grouped the remaining uncommitted and unpushed changes into review-friendly commits by project area, then pushed the branch so the PR history is easier to review.

### Functionality
- Split backend normalization/guardrail changes into a focused backend commit.
- Split evidence checklist/index updates into a dedicated evidence docs commit.
- Split top-level status tracker edits into a separate docs sync commit.
- Isolated the local SQLite runtime artifact into its own runtime commit for easier review filtering.

### Verification Evidence
- ✅ Commits were created and pushed successfully to `Rebecca-Gautreaux-Work-Branch`.
- ✅ The branch now contains a clear commit stack organized by project area.
- ✅ Uncommitted work was reduced to a review-friendly set of categorized commits.

### Importance
- Makes PR review easier by separating code, evidence docs, top-level docs, and runtime artifacts.
- Keeps low-risk documentation/history updates distinct from backend implementation changes.
- Improves traceability for reviewers who want to inspect each part independently.

## Stage 5: Rebecca-Safe Database Normalization Guardrails and Closeout Session (2026-04-12)

### Implementation
Completed the remaining Rebecca-safe database normalization tasks by adding low-risk verification guardrails, compatibility fallback observability, and rollout evidence scaffolding while preserving legacy JSON compatibility paths.

### Functionality
- Added fallback observability logging for relational-first compatibility paths in summaries and users APIs.
- Added one-shot normalization guardrail verification script that runs dry-run backfills and summary-link reconciliation checks.
- Extended full backend verification workflow with optional normalization guardrail execution flags.
- Added staging-ready normalization evidence checklist and indexed it under docs evidence.

### Verification Evidence
- ✅ Focused suites passed after guardrail/logging additions.
- ✅ Full backend suite passed: **211/211**.
- ✅ Full verification command with guardrails completed successfully in non-strict safe mode.

### Importance
- Improves operational safety by surfacing normalization drift before merge/deploy.
- Preserves low-risk ownership boundaries by avoiding destructive schema cleanup.
- Provides a concrete staging evidence path for grading/onboarding traceability.

## Stage 5: Frontend Visual Refresh Low-Risk Implementation and Max Validation Handoff Session (2026-04-12)

### Implementation
Completed the Rebecca-safe frontend visual refresh pass using token-first and shared-style updates, then synchronized top-level documentation to assign remaining manual validation/signoff to Max.

### Functionality
- Refreshed shared frontend visual system (palette balance, surface depth, heading hierarchy, and interaction states) without changing backend/API behavior.
- Applied low-risk page polish to dashboard, alerts, summaries, and map-facing UI surfaces using shared classes.
- Removed inline style attributes from `frontend/web/views/map.php` by moving popup/help/legend/loading styles into `frontend/web/public/assets/app.css`.
- Added explicit ownership annotations assigning remaining manual frontend validation/signoff tasks to Max in project tracker docs.

### Verification Evidence
- ✅ Diagnostics check reported no new errors in edited frontend files (`app.css`, `map.php`, `dashboard.php`, `alerts.php`, `summaries.php`).
- ✅ PowerShell search confirmed no remaining `style="..."` attributes in `frontend/web/views/map.php` after style extraction.
- ✅ Documentation synchronization completed across top-level tracking surfaces with preserved chronology/style.

### Importance
- Delivers a safer, more engaging UI uplift without expanding code-surface risk into backend/runtime behavior.
- Improves maintainability by centralizing map presentation styles into shared CSS.
- Clarifies closeout accountability by explicitly assigning final manual validation/signoff to Max.


## Stage 5: Session-Based UserID/Profile Flow, UI/UX Verification, and Documentation Handoff to Max (2026-04-13)

### Implementation
Migrated the profile page and related flows to a secure, session-based UserID system, removing manual UserID entry from the frontend and enforcing session-derived user context throughout the stack. Improved checkbox grid alignment and added device token help text for clarity. Due to login issues, further manual UI/UX verification and documentation updates are assigned to Max.

### Functionality
- UserID is now session-based and read-only in the profile UI; manual entry is no longer possible.
- Profile updates and preferences are tied to the authenticated session user.
- Checkbox grid alignment and device token help text improved for usability.
- All backend and frontend logic updated to enforce session-based user context.

### Pending Tasks (Assigned to Max)
- Manually verify the updated profile UI and all related flows for correctness and usability.
- Test session-based UserID enforcement and ensure no manual entry is possible.
- Confirm checkbox grid alignment and device token help text render as intended on all supported browsers/devices.
- Update all related documentation (README.md, USER_GUIDE.md, in-app help) to reflect the new session-based flow and UI changes.
- Report any regressions or issues found during manual verification.

**Note:** These tasks are assigned to Max due to current login/access issues for the previous implementer. Please document all findings and update the project tracker accordingly.

## Stage 5: Verified Map Closeout and Documentation Sync Session (2026-04-11)

### Implementation
Completed the final documentation sync after confirming the Stage 3 map closeout was fully verified and the required evidence bundle was present.

### Functionality
- Confirmed the interactive map path is now verifier-clean with all required S3-06 artifacts present.
- Kept the map demo fix focused on frontend data normalization rather than broader UI churn.
- Synchronized the top-level project summary to reflect the verified state of the map closeout and evidence bundle.

### Verification Evidence
- ✅ `npm run verify:evidence:s3` passes with all required artifacts and links present.
- ✅ The map demo no longer fails on alert/risk coordinate shape mismatches.
- ✅ The Stage 3 evidence bundle is filed under `static/evidence/` with the expected filenames.

### Importance
- Confirms the map demonstration is in a grading-ready state.
- Preserves a concise, verifiable record of the final map closeout.
- Keeps the top-level project summary aligned with the current repository state.

## Stage 5: Web-Only Scope Hardening and S3 Evidence Closeout Session (2026-04-11)

### Implementation
Completed a documentation-hardening and evidence-closeout session to keep CMPS 357 workflows web-only by default and to finish S3-06 verifier-gated evidence artifacts.

### Functionality
- Updated top-level and execution docs so required setup/validation paths explicitly target backend + web only.
- Replaced outdated web startup assumptions in top-level setup steps with the actual PHP server command path.
- Preserved mobile references only as clearly marked reference-only context.
- Materialized required S3-06 evidence artifacts under `static/evidence/` for verifier compatibility.

### Verification Evidence
- ✅ Re-verified required backend/web command paths (`uvicorn` help path and PHP runtime availability).
- ✅ `npm run verify:evidence:s3` now passes with all required S3-06 files present.
- ✅ Evidence links remained complete while missing-artifact count was reduced to zero.

### Importance
- Prevents contributor/grader setup failures from missing mobile directory assumptions.
- Aligns documentation with actual repository runtime behavior.
- Closes Stage 3 evidence gating with objective pass status for onboarding/grading readiness.

## Stage 5: Rebecca Implementation Closeout and Max Handoff Session (2026-04-11)

### Implementation
Completed a final non-frontend closeout pass for remaining safe tasks by assigning all S3-06 manual evidence capture/final filing work to Max and synchronizing top-level project documentation.

### Functionality
- Confirmed no additional backend/frontend implementation items remained in Rebecca scope from the sprint remediation plan.
- Added explicit S3-06 ownership assignment to Max across closeout tracking artifacts.
- Preserved automated validation path (`npm run verify:evidence:s3`) to gate manual evidence completion.

### Verification Evidence
- ✅ Documentation sync completed across top-level tracking files.
- ✅ Ownership for manual S3-06 capture/final filing explicitly assigned to Max.
- ✅ `npm run verify:evidence:s3` currently fails only for missing manual artifacts, confirming no unresolved automation/linkage gap.

### Importance
- Clarifies ownership boundaries and prevents implementation drift.
- Keeps grading/onboarding closeout unblocked while preserving safe change scope.

## Stage 5: Demo Verification Pass and FIRMS Warning Risk-Free Fix Session (2026-04-11)

### Implementation
Completed repeated demo verification passes in both headless and presenter-visible modes, then applied a minimal-risk backend configuration fix so required scraper-key checks consistently honor `.env` values loaded by settings.

### Functionality
- Re-ran demo workflow commands (`demo:setup`, `demo:verify`, `demo:info`) and confirmed stable seeded counts and metadata outputs.
- Executed automated walkthrough and evidence generation (`demo:run`, `demo:report`) with successful end-to-end pass and refreshed artifacts.
- Confirmed the FIRMS warning severity is non-blocking for seeded demo workflows but relevant for live wildfire ingestion.
- Updated scraper key-resolution checks to evaluate settings-backed values before process environment fallback.

### Verification Evidence
- ✅ Demo setup/verify/info commands passed with expected counts (4 users, 15 alerts, 2 summaries).
- ✅ Automated walkthrough passed **6/6** steps in headless and visible presenter modes.
- ✅ Evidence artifacts were regenerated (`static/evidence/demo_journey_log.json`, screenshots manifest, `DEMO_REPORT.md`).
- ✅ Post-run demo verification remained green after walkthrough execution.

### Importance
- Improves presentation reliability by proving repeatability across multiple demo passes.
- Reduces false configuration warnings in live-scraper scenarios without changing seeded demo behavior.
- Preserves safety by using a localized, low-risk code change in scraper registry lookup logic.

## Stage 5: Sprint Remediation Implementation and Verification Closeout Session (2026-04-11)

### Implementation
Closed the sprint remediation plan by implementing security, data-integrity, deployment-portability, and closeout documentation updates across backend and frontend surfaces.

### Functionality
- Hardened CORS origin handling with explicit configured allow-lists.
- Removed client-driven feedback identity binding path; session context now controls user attribution.
- Standardized assistant/forecast active-window filtering using parsed datetime logic for mixed timestamp formats.
- Replaced hardcoded frontend API assumptions with runtime-configured API base wiring in assistant and map paths.
- Added safe localStorage fallbacks for Golby runtime stability.
- Prepared and linked Stage 3 manual evidence closeout scaffolding artifacts.

### Verification Evidence
- ✅ Full backend verification passed with **198 passed** in pytest and smoke test pass.
- ✅ Targeted suites for assistant/forecast/feedback remained green after remediation.

### Remaining Manual Item
- S3-06 manual screenshot/video evidence capture remains open by design for grading/onboarding workflow.

## Stage 5: Demo Workflow Sanity Pass and Documentation Synchronization Session (2026-04-11)

### Implementation
Ran a final sanity pass on documented demo workflows and synchronized top-level documentation with the resulting validation outcomes.

### Functionality
- Confirmed `npm run demo:setup` seeds demo users, alerts, and summaries from fixtures.
- Confirmed `npm run demo:verify` validates schema/data completeness checks.
- Confirmed `npm run demo:info` returns seed metadata and user/token mappings.
- Confirmed `npm run demo:clean` removes generated demo artifacts after verification.

### Execution
- Executed all documented demo commands in sequence and confirmed expected outputs.
- Kept `backend/demo/` tooling in place because package scripts and demo docs depend on it.
- Updated synchronized top-level documentation entries for this session.

### Verification Evidence
- ✅ Demo command sequence passed end-to-end.
- ✅ Post-run cleanup completed successfully.

### Importance
- Maintains confidence that grading/demo runbooks are executable without undocumented steps.
- Preserves repository safety by retaining required demo tooling and avoiding accidental breakage.

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
py -m uvicorn main:app --host 0.0.0.0 --port 8001
```

You should see:

```
INFO:     Uvicorn running on http://0.0.0.0:8001
```

Verify it works by opening http://localhost:8001/docs in your browser (Swagger API docs).

### 4. Start the Web Frontend

```bash
php -S 127.0.0.1:8080 -t frontend/web/public
```

Then open `http://127.0.0.1:8080/index.php`.

### 5. Mobile Frontend Status (Not Required for CMPS 357)

The mobile app is not required for this CMPS 357 repository workflow.

- Required local workflow: backend + web frontend only
- Mobile app codebase: [RiskRadar Mobile App Repository](https://github.com/QuiHu/Team6Project.git)
- If you do not have `frontend/mobile/RiskRadar`, that is expected for this project scope

### Safe Commands for This Repository

```bash
# Backend
py -m pip install -r backend/requirements.txt
npm run backend:test
npm run backend:check
npm run backend:run

# Web frontend
php -S 127.0.0.1:8080 -t frontend/web/public
```

### Commands to Avoid in This Repository

```bash
cd frontend/mobile/RiskRadar
npx expo start
```

Those commands are mobile-repo commands and will fail here if the mobile directory is absent.

### Backend-Only Workflow (No Frontend)

If you want to avoid frontend/mobile errors and work only on backend tasks, use:

- [`docs/BACKEND_ONLY_WORKFLOW.md`](./docs/BACKEND_ONLY_WORKFLOW.md)

---

## Running the Demo

The RiskRadar demo infrastructure provides a complete, reproducible walkthrough of all features across Stages 1–4. Designed for graders and presenters, the demo includes pre-populated data, CLI tools, and comprehensive documentation.

### Quick Demo Setup

```bash
# Create fresh demo database with fixture data
npm run demo:setup

# Verify demo data loaded successfully
npm run demo:verify

# Print user IDs and session tokens for reference
npm run demo:info
```

### Demo Flow (12–15 minutes)

Once backend and web frontend are running, follow the guided walkthrough:

1. **[DEMO_RUNBOOK.md](./docs/DEMO_RUNBOOK.md)** — Step-by-step presentation script (2 min per step)
2. **[DEMO_FEATURES_BY_STAGE.md](./docs/DEMO_FEATURES_BY_STAGE.md)** — Feature-to-code mapping for graders
3. **[DEMO_ONBOARDING.md](./docs/DEMO_ONBOARDING.md)** — How to customize or extend the demo

### Demo CLI Commands

```bash
# Demo database operations
npm run demo:setup           # Create fresh demo.db with fixtures
npm run demo:seed            # Add fixtures to existing SQLite
npm run demo:reset           # Clear and reseed existing database
npm run demo:clean           # Remove demo.db and metadata
npm run demo:verify          # Validate schema and data completeness
npm run demo:info            # Print user IDs, tokens, alert summary

# Generate additional alerts (for scale demos)
npm run demo:generate-alerts -- --count 50 --type air_quality
npm run demo:generate-alerts -- --count 100 --distribution balanced
```

### Demo Users (in fixtures)

| ID | Name | Sensitivities | Use Case |
|----|------|---|----------|
| 1 | Demo User (Low Risk) | None | Baseline Stage 1 demo |
| 2 | Demo User (Medium Risk) | Asthma=3, Allergies=2 | Stage 2 personalization |
| 3 | Demo User (High Risk) | Asthma=4, COPD=3, Allergies=3, Heart=2, Immunocompromised=1 | Complex risk scoring |
| 4 | Demo Admin | Allergies=1, Elderly=1 | Admin features (auth, analytics) |

### For Graders

The demo fulfills all course requirements:
- ✅ **Stage 1**: Web-app backend connectivity, alerts/summaries feed, user registration/profile
- ✅ **Stage 2**: Personalized risk scoring, smart alert prioritization, health sensitivities
- ✅ **Stage 3**: Interactive geospatial map, overlays, responsive UX, accessibility  
- ✅ **Stage 4**: Forecast UI with personalized advice, AI assistant with guardrails

See [DEMO_FEATURES_BY_STAGE.md](./docs/DEMO_FEATURES_BY_STAGE.md) for detailed feature-to-code mapping.

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
| Assistant or user routes return HTTP 500 with `no such column: users.is_admin` | Local SQLite schema is stale. Stop backend and rebuild backend DB with fixtures: `c:/Users/rebec/OneDrive/Documents/GitHub/cmps-357-sp26-final-project-cmps357-team-3/.venv/Scripts/python.exe backend/demo/seed_demo_data.py --mode fresh --db-path backend/riskradar.db`, then restart backend on `8001`. |

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
- Backend-only workflow (no frontend runtime required): [docs/BACKEND_ONLY_WORKFLOW.md](./docs/BACKEND_ONLY_WORKFLOW.md)
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

## Verification Snapshot (Latest)

- Latest final Golby verification pass: connectivity preflight **PASS**, frontend build **PASS**, and demo journey **6/6 passed** on canonical local topology (2026-04-14).
- Latest full backend verification (`npm run verify:backend`): **211 passed** plus standalone smoke test pass and normalization guardrail step pass (2026-04-12).
- Latest connectivity preflight (`npm run verify:connectivity`): **PASS** for canonical base/prefix, backend root, readiness API, alerts API, forecast API, assistant user lookup, frontend index, frontend map API wiring, and CORS (2026-04-13).
- Latest end-to-end demo journey: **6/6 passed** using split-origin local topology (`--base-url http://127.0.0.1:8080 --api-base-url http://127.0.0.1:8001`) (2026-04-13).
- Widget/assistant feature-equivalence review completed and branding restoration validated with successful frontend build (`npm run build:web`) (2026-04-13).
- SVG asset white-pixel removal completed for assistant icon transparency optimization (2026-04-13).
- Historical 191/196 totals in session sections are preserved as point-in-time records from earlier runs.

## Stage 5: Final Golby Verification Pass, Safe Artifact Reversion, and Documentation Synchronization Session (2026-04-14)

### Implementation
Completed a final Stage 5 verification and hygiene closeout by running the full Golby validation chain on live local services, reverting generated runtime artifacts, and synchronizing project documentation in chronological order.

### Functionality
- Confirmed canonical split-origin runtime behavior remains healthy for backend API (`127.0.0.1:8001`) and frontend PHP (`127.0.0.1:8080`).
- Confirmed pre-demo connectivity checks still pass end-to-end, including map API wiring with guest-session setup and CORS.
- Confirmed Golby assistant journey behavior remains stable with full **6/6** demo steps passing.
- Reverted generated runtime artifacts (SQLite DB churn, pycache files, evidence snapshots/logs) so review scope remains intentional.

### Execution
- Started backend service and frontend service on canonical ports.
- Ran `py backend/scripts/pre_demo_connectivity_check.py` to full PASS.
- Ran `npm run build:web` successfully.
- Ran `node frontend/web/tests/demo/demo_journey.js --base-url http://127.0.0.1:8080 --api-base-url http://127.0.0.1:8001` to **6/6 passed**.
- Stopped temporary local services and restored generated artifacts.
- Ran transcript duplicate-heading pass and confirmed `NO_DUPLICATE_STAGE_HEADINGS`.

### Importance
- Provides high-confidence final verification that Golby and wiring-critical paths remain operational.
- Keeps repository history clean by excluding generated runtime/evidence churn from implementation review.
- Maintains documentation governance by synchronizing progress, transcript, reflection, and authorship records.

## Stage 5: Connectivity Hardening Completion, Safe Artifact Isolation, and Documentation Synchronization Session (2026-04-13)

### Implementation
Completed the remaining wiring-hardening closeout tasks, including startup schema fail-fast, readiness verification flow, map-wiring preflight reliability fixes, and safe cleanup of runtime artifacts for review-ready repository state.

### Functionality
- Confirmed strict schema validation and readiness behavior are active in backend startup/runtime.
- Confirmed pre-demo connectivity checks validate canonical wiring, including map API markers after guest-session setup.
- Confirmed demo journey auth/session resilience and assistant-path checks pass in full split-origin local execution.
- Isolated runtime/evidence artifacts with safety stashes so intentional code/docs changes remain review-focused.

### Execution
- Ran `npm run verify:connectivity` to full PASS.
- Ran `node frontend/web/tests/demo/demo_journey.js --base-url http://127.0.0.1:8080 --api-base-url http://127.0.0.1:8001` to **6/6 passed**.
- Performed transcript duplicate-heading pass and confirmed no duplicate Stage-session headings.
- Synchronized top-level documentation set (README, STAGES, TODO, TRANSCRIPT, REFLECTION, AUTHORS, PROGRAM_EXECUTION, DEMO_RUNBOOK, USER_GUIDE).

### Importance
- Closes the remaining frontend-backend wiring reliability gaps before demos.
- Improves fail-fast behavior for schema drift and readiness regressions.
- Keeps repository history and operational guidance aligned with verified runtime behavior.

## Stage 5: Golby Feature Verification and RiskRadar Branding Restoration Session (2026-04-13)

### Implementation
Completed a focused parity-and-branding session: confirmed widget and assistant page are feature-equivalent, then restored the intended RiskRadar globe mascot presentation in Golby UI rendering.

### Functionality
- Verified both assistant entry points share the same ChatInterface behavior and capability coverage.
- Replaced placeholder Golby rendering with embedded `ai-assistant-reacting.svg` in `frontend/web/components/golby/GolbyIcon.tsx`.
- Rebuilt facial overlay geometry to align with the globe asset coordinate system (495x468) rather than the previous 100x100 placeholder model.
- Preserved and validated expression support across assistant visual states (happy, thinking, waving, winking, laughing, surprised, puzzled, excited).

### Execution
- Performed source-level comparison for widget and assistant page feature parity.
- Refactored mascot rendering path in Golby icon component and adjusted overlay positioning.
- Ran `npm run build:web` successfully and confirmed no TypeScript errors after branding restoration.
- Synchronized top-level docs (TRANSCRIPT, REFLECTION, STAGES, TODO, AUTHORS, README) in Stage 5 chronological order.

### Importance
- Restores authentic RiskRadar visual identity across assistant UI surfaces.
- Removes mismatch between mockup branding and live widget/page presentation.
- Preserves functional stability while improving user trust and interface polish.

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

As an extension effort related to RiskRadar, this repository focuses on the CMPS 357 web-app implementation and shared backend. Mobile implementation work is maintained in the separate CMPS 490 mobile repository.

### RiskRadar Web-App Extension

This repository is scoped to the web-app extension workflow for CMPS 357 while sharing the backend API service in `backend/`.

**Frontend surfaces:**
- `frontend/web/` — designated CMPS 357 PHP web-app extension workspace

**Web frontend scaffold:**
- `frontend/web/views/` — page templates and routed screens
- `frontend/web/components/` — reusable PHP/UI fragments
- `frontend/web/services/` — backend API wrappers and response helpers
- `frontend/web/public/` — public-facing assets and entry files
- `frontend/web/config/` — environment and runtime configuration templates

**Mobile frontend note:**
- Mobile frontend work is out-of-scope for this repository's required setup path.
- If needed, use the separate mobile repository linked above.

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
	- Preserved clean scope boundaries by keeping CMPS 357 work in `frontend/web/`.
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
