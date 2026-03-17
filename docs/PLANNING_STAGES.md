# Stage 1 Planning (Kickoff)

**Context:** This document details the tactical execution plan for Stage 1 (Web-App Extension), which is a **REQUIRED** deliverable targeting completion by **Week of March 31, 2026** as part of the broader CMPS 357 project due April 29, 2026. See [STAGES.md](./STAGES.md) and [README.md](../README.md) for overall timeline and scope alignment (Stages 1-2 required; Stages 3-4 optional/stretch).

---

## Stage 1: Web-App Extension (Completed)

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

## Stage 1: Web-App Extension (Completed) Finalization Record

Stage 1 closure is complete as of **2026-03-13**.

### Completion Checklist Outcome

- [x] Finish S1-05 first (highest remaining implementation risk).
- [x] Implement/verify allowlist validation, sanitization, output escaping, CSRF, and defensive null handling.
- [x] Add concrete evidence links in the Stage 1 task tracker row.
- [x] Close responsive and distinctness evidence.
- [x] Capture 360px, 768px, and 1280px responsive verification notes and document web-vs-mobile distinctness.
- [x] Attach walkthrough/evidence artifacts to Stage 1 docs tracking.
- [x] Convert Stage 1 in-progress doc tasks to completed.
- [x] Finalize S1-01 architecture/route contract wording and URL configuration guidance in `docs/API_STAGE1_CONTRACT.md`.
- [x] Finalize S1-06 setup/run documentation and evidence linkage.
- [x] Sync Stage 1 status wording across planning/progress docs.

### Final Stage 1 Evidence Pointers

- Execution tracker and completed checklist: `docs/TODO.md`
- Architecture/contract matrix and route mapping: `docs/API_STAGE1_CONTRACT.md`
- Responsive and web-distinctness verification notes: `docs/STAGE1_VERIFICATION_EVIDENCE.md`

---

## Stage 2 Planning (Kickoff)

**Context:** This section defines the tactical execution plan for Stage 2 (Environmental Risk Assessment and Alert Prioritization Extensions), which is a **REQUIRED** deliverable targeting completion by **Week of April 28, 2026**. This plan is aligned to `docs/STAGES.md`, `docs/TODO.md`, and `README.md`.

### Objective
Deliver Stage 2 by implementing a deterministic, explainable personal risk-scoring pipeline and smart alert prioritization flow, then surfacing both outputs across web and mobile clients while preserving Stage 1 endpoint compatibility.

### Scope Decisions (Confirmed)
- **Risk score model**: 0-100 normalized weighted sum with threshold labels.
- **Sensitivity input model**: 0-5 per sensitivity factor (with defaults for backward compatibility).
- **Prioritization API strategy**: Add a new prioritized route and preserve existing Stage 1 route behavior.
- **Client scope**: Integrate Stage 2 outputs in both web and mobile baseline experiences.
- **Scoring approach**: Formula-based deterministic logic (no LLM dependency for score computation).

### Stage 2 Kickoff Steps

1. **Lock Stage 2 technical specification**
	- Finalize normalization rules for each factor and document 0-100 score conversion.
	- Finalize high/medium/low thresholds.
	- Finalize deterministic tie-break ordering for same-score alerts.

2. **Define and document sensitivity contract**
	- Confirm 0-5 sensitivity factors and default fallback values.
	- Document behavior for users with missing preferences/location data.
	- Keep fields optional in update pathways for existing-user compatibility.

3. **Implement backend schema/model updates (S2-02)**
	- Extend user model and schemas for sensitivity fields.
	- Add/adjust response schemas for risk score output and factor transparency.
	- Add priority metadata schema for ranked alerts.

4. **Implement risk scoring service (S2-03)**
	- Build reusable scoring service module.
	- Return score + factor breakdown for explainability.
	- Ensure deterministic output for repeated identical inputs.

5. **Expose score endpoint(s) (S2-04)**
	- Add score retrieval endpoint with validation/auth rules.
	- Add fallback-safe responses for missing or partial user context.
	- Add API examples to docs once endpoint shape is stable.

6. **Define and implement ranking logic (S2-05, S2-06)**
	- Weight risk contribution, severity, distance, and sensitivity relevance.
	- Normalize components into a stable priority score.
	- Apply deterministic tie handling and urgency labels.

7. **Integrate prioritization into alert pipeline (S2-07)**
	- Add prioritized alert endpoint and preserve legacy endpoint compatibility.
	- Include rank, score, urgency label, and short explanation metadata.
	- Preserve raw alert fields for auditability.

8. **Surface Stage 2 outputs in web/mobile UI (S2-08)**
	- Web: add score and prioritized context to risk/dashboard/alert detail views.
	- Mobile: add score + prioritized alert surface in baseline tabs flow.
	- Ensure clients consume backend ordering (no duplicated ranking logic in UI).

9. **Run Stage 2 verification and doc sync (S2-09 + docs)**
	- Add deterministic scoring/ranking tests and endpoint contract checks.
	- Validate backward compatibility with Stage 1 routes.
	- Update Stage 2 progress markers/evidence in `docs/TODO.md`, `docs/STAGES.md`, and `README.md`.

### Week-by-Week Execution Calendar (S2-01 to S2-09)

| Week Of | Planned Focus | Task IDs | Primary Owner | Expected Evidence |
|---|---|---|---|---|
| 2026-03-17 | Stage 2 design lock and ambiguity resolution | S2-01, S2-05 | Max (lead), Rebecca (review) | Formula draft, threshold definitions, tie-break policy notes |
| 2026-03-24 | Data model/schema preparation and service scaffolding | S2-02, S2-03 (start) | Rebecca (S2-02), Max (S2-03) | Schema/model diff, service skeletons, fixture updates |
| 2026-03-31 | Risk scoring implementation and endpoint integration | S2-03, S2-04 (start) | Max | Scoring module tests, endpoint prototype responses |
| 2026-04-07 | Prioritization algorithm and pipeline integration | S2-04, S2-06, S2-07 (start) | Max | Ranked output samples, route integration notes |
| 2026-04-14 | Client integration across web and mobile | S2-07, S2-08 | Rebecca (lead), Max (support) | UI screenshots/demo notes for prioritized alerts + score |
| 2026-04-21 | Testing hardening and cross-doc synchronization | S2-09, DOC-01, DOC-02 | Max + Rebecca | Test evidence, status updates in TODO/STAGES/README |
| 2026-04-28 | Stage 2 closure buffer and acceptance pass | Residuals/cleanup | Max + Rebecca | Final verification notes and Stage 2 completion marker |

### Stage 2 Deliverables (Kickoff Phase)
- Risk scoring service implementation and supporting schemas/models.
- Prioritized alert endpoint and metadata integration.
- Web + mobile baseline surfaces showing score and prioritized alerts.
- Test coverage for deterministic scoring/ranking and compatibility checks.
- Documentation updates across planning/tracking/architecture artifacts.

### Verification Evidence to Collect
- Repeat-input test output showing consistent risk score and rank order.
- API response examples for score and prioritized alert routes.
- Web and mobile screenshots/walkthrough notes for success and fallback states.
- Backward compatibility checks confirming Stage 1 routes remain stable.

### Stage 2 Risks and Mitigations
- **Risk:** Formula churn causes rework late in sprint.
  - **Mitigation:** Lock weights/thresholds in S2-01 and treat later changes as controlled refinements.
- **Risk:** Breaking Stage 1 consumers by changing legacy alert payloads.
  - **Mitigation:** Keep legacy routes stable and expose Stage 2 metadata via dedicated prioritized route.
- **Risk:** Missing user context (location/preferences) creates unstable ranking behavior.
  - **Mitigation:** Use documented defaults and deterministic fallback ranking path.
- **Risk:** Documentation lag near deadline.
  - **Mitigation:** Attach evidence artifacts to weekly tracker updates, not only at finalization.