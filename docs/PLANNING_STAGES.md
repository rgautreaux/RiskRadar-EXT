# Stage 1 Planning (Kickoff)

**Context:** This document details the tactical execution plan for Stage 1 (Web-App Extension), which is a **REQUIRED** deliverable targeting completion by **Week of March 31, 2026** as part of the broader CMPS 357 project due April 29, 2026. See [STAGES.md](./STAGES.md) and [README.md](../README.md) for overall timeline and scope alignment (Stages 1-2 required; Stages 3-4 optional/stretch).

---

## Stage 1: Web-App Extension (MVP Start Plan)

### Objective
Begin Stage 1 with a small, functional PHP web-app vertical slice that connects to existing RiskRadar backend APIs and demonstrates a distinct web interface.

### Scope Decisions (Confirmed)
- **MVP page scope**: Dashboard first (`alerts` summary + latest `summary`)
- **Web app location**: `frontend/web/` (with mobile app retained in `frontend/mobile/`)
- **Backend runtime during development**: Current startup as-is (scheduler enabled)

### Stage 1 Kickoff Steps

1. **Baseline Stage 1 documentation targets**
	- Align Stage 1 wording and checklist between `docs/STAGES.md` and `README.md` for dashboard-first MVP.
	- Keep status language consistent with current progress tracking.

2. **Create PHP web-app structure in `/frontend/web`**
	- Add initial directories:
	  - `/frontend/web/views`
	  - `/frontend/web/components`
	  - `/frontend/web/services`
	  - `/frontend/web/public`
	  - `/frontend/web/config`
	- Add initial pages:
	  - `index.php` (dashboard)
	  - alerts page
	  - summaries page
	  - user/preferences page

3. **Add frontend environment/config template**
	- Provide a config template for API base URL and timeout behavior.
	- Ensure config aligns with backend API prefix (`/api/v1`) and local/dev URLs.

4. **Implement PHP API service wrappers**
	- Build reusable service functions for:
	  - Alerts endpoints
	  - Summaries endpoints
	  - User register/preferences endpoints
	- Document endpoint contract details for each route (method, expected params, response shape, fallback behavior).
	- Standardize handling for:
	  - timeouts
	  - non-2xx responses
	  - malformed/empty JSON payloads

5. **Build dashboard-first MVP UI**
	- Display alerts summary/stats and latest generated summary on homepage.
	- Add lightweight navigation to other core pages.
	- Keep interface clearly distinct from mobile app presentation.
	- Include at least one web-specific comparative element (for example: top alerts snapshot + latest summary panel).

6. **Add security and resilience essentials**
	- Validate/sanitize user input for query params/forms.
	- Use output escaping in PHP templates and CSRF protection for form submissions.
	- Add defensive rendering for null/missing API fields.
	- Avoid exposing secrets in frontend code or client payloads.

7. **Document Stage 1 setup and run flow**
	- Add local startup instructions for backend + PHP server.
	- List required environment values for backend/frontend.
	- Include expected API dependency notes and troubleshooting basics.

8. **Run Stage 1 MVP verification checklist**
	- Confirm web app loads successfully and connects to backend.
	- Confirm dashboard renders live API data.
	- Confirm graceful behavior for API timeout, non-2xx, and malformed/empty JSON conditions.
	- Confirm responsive and usable behavior at 360px, 768px, and 1280px viewports.

### Web Distinctness Criteria (Stage 1)
- Desktop-oriented dashboard density (multi-card stats + latest summary context in one view).
- Web-native layout/navigation patterns that are not a direct mirror of mobile screens.
- At least one comparative overview module on the dashboard.
- Keyboard-friendly navigation verified during manual QA.

### MVP Boundary (What Stage 1 Start Includes)
- Included:
  - Dashboard vertical slice (alerts stats + latest summary)
  - Core read-focused pages scaffold
  - Basic user register/preferences form path
  - Setup and run documentation
- Deferred to later stages:
  - Personalized risk scoring
  - Smart alert prioritization
  - Interactive map
  - Predictive analytics and AI assistant enhancements

### Stage 1 Deliverables (Kickoff Phase)
- `/frontend/web` scaffold with initial PHP pages/components/services
- API integration layer for alerts/summaries/users
- Stage 1 endpoint contract matrix in `docs/API_STAGE1_CONTRACT.md`
- Environment/config template for frontend
- Updated setup notes and verification checklist

### Verification Evidence to Collect
- Screenshots or short walkthrough of dashboard and core pages
- Notes showing API success and API-failure behavior
- Confirmation that Stage 1 progress markers remain current in project docs

## Stage 1: Finalization Steps (Post-Kickoff Closure and Validation)
Use this finish order to minimize risk and close Stage 1 quickly:

-[] Finish S1-05 first (highest remaining implementation risk).
-[] Implement/verify allowlist validation, sanitization, output escaping, CSRF, and defensive null handling exactly as Stage 1 requires in STAGES.md:53 and TODO.md:60.
-[] Add concrete evidence links in the task tracker row after verification.
-[] Close responsive and distinctness evidence next (the main blocker to completion).
-[] Capture proof at 360px, 768px, 1280px plus notes showing web-vs-mobile layout distinction required by TODO.md:107, TODO.md:108, and criteria in STAGES.md:79.
-[] Attach screenshots/walkthrough artifacts to S1-04/S1-06 evidence fields in TODO.md:59 and TODO.md:61.
-[] Convert in-progress docs tasks to completed.
-[] S1-01: finalize architecture/route contract wording and confirm full parity with the matrix in API_STAGE1_CONTRACT.md:13.
-[] S1-06: finalize setup/run walkthrough with the actual local port workflow already observed in TODO.md:49.
-[] Sync status sources in one pass.
-[] Update checklist checkboxes and master tracker statuses in TODO.md:93.
-[] Ensure Stage progress wording remains consistent in STAGES.md:114 and README status table (as required by tracker hygiene notes in TODO.md:186).