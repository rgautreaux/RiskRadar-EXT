# Sprint Remediation Plan (2026-04-11)

## Objective
Close critical security, data-integrity, deployment-portability, and closeout gaps identified in the post-analysis review.

## Scope
Included:
- CORS hardening
- Feedback identity-spoofing prevention
- Timestamp window correctness in assistant/forecast
- Frontend API base portability
- Frontend localStorage resilience
- Map implementation path cleanup
- Stage 3 S3-06 evidence closeout

Excluded for this sprint:
- New forecasting model architecture
- LLM platform migration
- Large UI redesign unrelated to identified risk items

## Backlog

| Priority | Item | Owner | Effort | Dependencies |
|---|---|---|---:|---|
| P0 | CORS origin hardening | Backend Security Lead | 0.5d | None |
| P0 | Feedback spoofing fix | Backend API Lead | 0.5d | None |
| P0 | Timestamp filtering correctness | Backend Data Lead | 1.0d | Feedback fix recommended before final verification |
| P1 | Frontend API base portability | Frontend Lead | 1.5d | Timestamp fix complete |
| P1 | localStorage hardening in Golby chat | Frontend Security Lead | 1.0d | None |
| P1 | Map logic consolidation (single active runtime path) | Frontend Architect | 0.5d | API base portability |
| P1 | Stage 3 S3-06 evidence closeout | QA and Documentation Lead | 1.0d | None (parallelizable) |
| P1 | Final regression and doc synchronization | QA Lead + Tech Writer | 1.5d | All above complete |

Total estimated effort: 7.5 engineer-days

## Work Items

### 1) P0 - CORS origin hardening
Owner: Backend Security Lead  
Effort: 0.5d

Files:
- `backend/main.py`
- `backend/tests/conftest.py`
- `backend/config/settings.py`

Tasks:
1. Replace wildcard origins with explicit allow-list from config.
2. Keep credentialed requests enabled only with explicit origins.
3. Mirror behavior in test app setup.

Verification:
1. Disallowed origin request receives no permissive CORS headers.
2. Allowed origin request succeeds with expected headers.
3. Relevant API tests pass.

### 2) P0 - Feedback spoofing fix
Owner: Backend API Lead  
Effort: 0.5d

Files:
- `backend/api/feedback.py`
- `backend/schemas/feedback.py`
- `backend/tests/test_api_feedback.py`

Tasks:
1. Remove client-driven user binding for feedback creation.
2. Bind user context only from authenticated session when present.
3. Update tests to reflect authenticated profile-learning path.

Verification:
1. Unauthenticated feedback cannot set another user's ID.
2. Authenticated feedback updates current user's profile-learning signals.
3. Feedback suite passes.

### 3) P0 - Timestamp filtering correctness
Owner: Backend Data Lead  
Effort: 1.0d

Files:
- `backend/api/assistant.py`
- `backend/api/forecast.py`
- `backend/tests/test_api_assistant.py`
- `backend/tests/test_api_forecast.py`

Tasks:
1. Replace string-based window filtering with parsed datetime comparisons.
2. Normalize `Z`, offset, and naive timestamps to UTC.
3. Keep behavior consistent between assistant and forecast.

Verification:
1. Mixed timestamp format fixtures produce stable inclusion/exclusion.
2. Assistant and forecast suites pass.

### 4) P1 - Frontend API base portability
Owner: Frontend Lead  
Effort: 1.5d

Files:
- `frontend/web/components/golby/apiClient.ts`
- `frontend/web/views/assistant.php`
- `frontend/web/risk_map.js`
- `frontend/web/views/map.php`

Tasks:
1. Replace hardcoded `/api/v1` calls with runtime-configured API base.
2. Inject API base into assistant and map pages.
3. Preserve credentials behavior for session-backed endpoints.

Verification:
1. API calls target configured base/prefix in local and split-port setups.
2. Golby and map requests succeed without reverse-proxy assumptions.

### 5) P1 - localStorage hardening
Owner: Frontend Security Lead  
Effort: 1.0d

Files:
- `frontend/web/components/golby/ChatInterface.tsx`

Tasks:
1. Wrap all storage reads/writes in safe fallbacks.
2. Ensure session/profile state gracefully degrades when storage is unavailable.

Verification:
1. No uncaught errors when storage access fails.
2. Chat initializes and remains usable with fallback behavior.

### 6) P1 - Map path consolidation
Owner: Frontend Architect  
Effort: 0.5d

Files:
- `frontend/web/views/map.php`
- `frontend/web/risk_map.js`

Tasks:
1. Ensure one canonical map fetch/render path is active.
2. Remove or neutralize conflicting duplicate behavior.

Verification:
1. No duplicate map render/fetch lifecycle.
2. Overlay toggles, popups, and personalization still work.

### 7) P1 - Stage 3 S3-06 evidence closeout
Owner: QA + Documentation Lead  
Effort: 1.0d

Files:
- `docs/TODO.md`
- `docs/PLANNING_DOCS/STAGE3_DOCS/STAGE3_VERIFICATION_EVIDENCE.md`
- `static/evidence/*`

Tasks:
1. Capture required desktop/mobile screenshots.
2. Record short walkthrough video.
3. Link artifacts in stage verification docs.
4. Close S3-06 checklist in tracker.

Verification:
1. Required artifacts exist under `static/evidence/`.
2. Documentation links resolve correctly.
3. S3-06 checklist items are complete.

### 8) P1 - Final regression and docs sync
Owner: QA Lead + Tech Writer  
Effort: 1.5d

Files:
- `README.md`
- `docs/TODO.md`
- `docs/STAGES.md`

Tasks:
1. Run backend verification and targeted manual smoke tests.
2. Resolve or document any residual defects.
3. Sync status language across tracker and summary docs.

Verification:
1. Backend verification command passes.
2. Manual smoke passes for auth, map, forecast, assistant, feedback.
3. README/STAGES/TODO are consistent.

## Sprint Sequencing

### Week 1 (parallel tracks)
- Track A (Backend): CORS + feedback spoofing + timestamp filtering
- Track B (Frontend): API base portability + localStorage hardening
- Track C (QA/Docs): S3-06 artifact capture

### Week 2
- Map path consolidation
- End-to-end verification
- Documentation synchronization and closeout

## Exit Criteria
1. No P0 items remain open.
2. Targeted API suites pass for feedback, assistant, and forecast.
3. Frontend clients no longer depend on hardcoded `/api/v1` paths.
4. Stage 3 evidence bundle is complete and linked.
5. README/STAGES/TODO represent the same final status.