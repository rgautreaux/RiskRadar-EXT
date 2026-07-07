# Guest Access Restriction Implementation Plan (Max/Rebecca Split)

## Objective
Apply account-required restrictions for guest users while preserving full access for authenticated account users.

### Restricted For Guests
- Personalized Risk Scoring
- Health-Sensitivity Personalization
- Personalized Risk Map Overlay
- Forecasting Features
- Smart Alerts (included as personalized feature)

### Unaffected For Authenticated Users
- Full access to all base and enhancement features

---

## Scope and File Map

### Backend Enforcement (Authoritative)
- `backend/auth/dependencies.py`
- `backend/api/risk.py`
- `backend/api/users.py`
- `backend/api/forecast.py`
- `backend/api/alerts.py`

### Frontend Enforcement + UX
- `frontend/web/services/security.php`
- `frontend/web/services/api_client.php`
- `frontend/web/public/risk.php`
- `frontend/web/public/smart_alerts.php`
- `frontend/web/public/profile.php`
- `frontend/web/public/forecast.php`
- `frontend/web/public/map.php`
- `frontend/web/views/risk.php`
- `frontend/web/views/smart_alerts.php`
- `frontend/web/views/profile.php`
- `frontend/web/views/forecast.php`
- `frontend/web/views/map.php`
- `frontend/web/public/assets/forecast-location.js`

### Tests
- `backend/tests/test_api_risk.py` (new)
- `backend/tests/test_api_users.py`
- `backend/tests/test_api_forecast.py`
- `backend/tests/test_api_alerts.py`

---

## Recommended Execution Order

## Phase 1: Foundations (Must Complete First)
- [ ] Add account-required and ownership/admin-check helper(s) in `backend/auth/dependencies.py`.
- [ ] Add frontend account-only guard helper in `frontend/web/services/security.php`.
- [ ] Define shared restriction message copy (guest lock CTA text) to reuse across views.

Dependency note:
- All backend endpoint gating depends on backend helper completion.
- All frontend page gating depends on frontend helper completion.

---

## Phase 2: Backend Restrictions (Security First)
- [ ] Gate personalized risk score in `backend/api/risk.py`.
- [ ] Gate personalized risk map endpoint in `backend/api/risk.py`.
- [ ] Gate preferences update (health sensitivity path) in `backend/api/users.py`.
- [ ] Gate forecast endpoints in `backend/api/forecast.py`.
- [ ] Gate prioritized/smart alerts endpoint in `backend/api/alerts.py`.
- [ ] Normalize restricted responses to 401 unauthenticated and 403 unauthorized-owner.

Dependency note:
- Complete this phase before frontend UX lock screens to avoid bypass risk.

---

## Phase 3: Frontend Page Guards and Guest UX
- [ ] Apply account-only guard to restricted pages:
- [ ] `frontend/web/public/risk.php`
- [ ] `frontend/web/public/smart_alerts.php`
- [ ] `frontend/web/public/profile.php`
- [ ] `frontend/web/public/forecast.php`
- [ ] Keep `frontend/web/public/map.php` accessible but disable personalized map controls for guests.
- [ ] Add lock-state CTA/message blocks in:
- [ ] `frontend/web/views/risk.php`
- [ ] `frontend/web/views/smart_alerts.php`
- [ ] `frontend/web/views/profile.php`
- [ ] `frontend/web/views/forecast.php`
- [ ] `frontend/web/views/map.php`
- [ ] Prevent guest forecast requests in `frontend/web/public/assets/forecast-location.js`.

---

## Phase 4: API Client Message Normalization
- [ ] Update 401/403 handling and user-facing copy for restricted features in `frontend/web/services/api_client.php`.
- [ ] Ensure restricted endpoint failures do not show misleading backend-unavailable messages.

---

## Phase 5: Verification and Regression
- [ ] Add/extend backend auth tests in:
- [ ] `backend/tests/test_api_risk.py`
- [ ] `backend/tests/test_api_users.py`
- [ ] `backend/tests/test_api_forecast.py`
- [ ] `backend/tests/test_api_alerts.py`
- [ ] Validate guest behavior:
- [ ] blocked for restricted features
- [ ] map base overlays still work
- [ ] Validate authenticated behavior:
- [ ] full access to all features
- [ ] owner/admin authorization expectations
- [ ] Run backend verification suite and targeted page checks.

---

## Max/Rebecca Recommended Split

## Rebecca (Backend/Auth + Test Ownership)
1. Implement reusable auth/authorization helpers in `backend/auth/dependencies.py`.
2. Gate backend routes in:
- `backend/api/risk.py`
- `backend/api/users.py`
- `backend/api/forecast.py`
- `backend/api/alerts.py`
3. Build/extend backend auth tests in:
- `backend/tests/test_api_risk.py`
- `backend/tests/test_api_users.py`
- `backend/tests/test_api_forecast.py`
- `backend/tests/test_api_alerts.py`
4. Confirm response semantics (401/403) are consistent.

## Max (Frontend UX + Page Locking Ownership)
1. Add frontend account-only helper in `frontend/web/services/security.php`.
2. Apply page guard behavior in:
- `frontend/web/public/risk.php`
- `frontend/web/public/smart_alerts.php`
- `frontend/web/public/profile.php`
- `frontend/web/public/forecast.php`
- `frontend/web/public/map.php` (personalized controls disabled only)
3. Add lock-state CTA UI in:
- `frontend/web/views/risk.php`
- `frontend/web/views/smart_alerts.php`
- `frontend/web/views/profile.php`
- `frontend/web/views/forecast.php`
- `frontend/web/views/map.php`
4. Update JS gating in `frontend/web/public/assets/forecast-location.js`.
5. Normalize frontend restricted messaging in `frontend/web/services/api_client.php`.

---

## Parallelization Plan

### Parallel Window A (After Phase 1 starts)
- Rebecca: backend helper implementation in `backend/auth/dependencies.py`
- Max: frontend helper implementation in `frontend/web/services/security.php`

### Parallel Window B (After both helpers are merged)
- Rebecca: backend route gating and backend tests
- Max: frontend page/view gating and forecast JS gating

### Parallel Window C (Final)
- Rebecca + Max: integration verification, smoke tests, UX polish, docs sync

---

## Merge and Validation Order
1. Merge backend helper and route gating first.
2. Merge frontend lock-state and page guards second.
3. Merge tests and run full verification.
4. Perform final guest vs authenticated walkthrough.

---

## Acceptance Checklist
- [ ] Guests cannot access personalized risk scoring.
- [ ] Guests cannot access health-sensitivity personalization.
- [ ] Guests cannot use personalized risk map overlay.
- [ ] Guests cannot access forecasting features.
- [ ] Guests cannot access smart alerts.
- [ ] Authenticated users retain full feature access.
- [ ] Base guest features (dashboard, alerts, summaries, non-personalized map) continue to work.
- [ ] Test suite passes and no auth regressions are introduced.
