# Stage 2: Environmental Risk Assessment and Alert Prioritization API Contract Matrix (In Progress)

Date: 2026-03-17

This document defines the Stage 2 API contract targets for personal risk scoring and smart alert prioritization.

- Base URL: configured by each client runtime.
- API prefix: `/api/v1`
- Contract status: policy locked and client scaffolding integrated; backend route implementation is in progress.
- Compatibility requirement: Stage 1 `GET /api/v1/alerts` behavior must remain stable while Stage 2 adds dedicated metadata routes.

## Stage 2 Architecture and Route Usage Flow

### Request flow (web/mobile to backend)

1. Clients call Stage 2 routes via existing API wrappers/services.
2. Backend computes deterministic risk and priority outputs using:
   - `backend/services/risk_scoring.py`
   - `backend/services/alert_prioritization.py`
3. API handlers return normalized payloads for score, rank, and urgency metadata.
4. Clients render score and prioritized alerts, or fallback-safe empty states if Stage 2 routes are unavailable.

### Client integration mapping

| Client Surface | Integration Module | Planned/Target Backend Routes |
|---|---|---|
| Web risk page | `frontend/web/public/risk.php` + `frontend/web/services/api_client.php` | `GET /api/v1/users/{user_id}/risk-score`, `GET /api/v1/alerts/prioritized` |
| Mobile risk hooks/services | `frontend/mobile/RiskRadar/services/riskService.ts` + `frontend/mobile/RiskRadar/hooks/useRiskData.ts` | `GET /api/v1/users/{user_id}/risk-score`, `GET /api/v1/alerts/prioritized` |

## URL and Environment Configuration

### Configuration keys

- `RISKRADAR_API_BASE_URL`
- `RISKRADAR_API_PREFIX`
- `RISKRADAR_API_TIMEOUT`

### URL composition rule

`{RISKRADAR_API_BASE_URL}/{trim(RISKRADAR_API_PREFIX)}/{resource_path}`

Example:
- Base URL: `http://127.0.0.1:8001`
- Prefix: `/api/v1`
- Resource path: `users/1/risk-score`
- Final URL: `http://127.0.0.1:8001/api/v1/users/1/risk-score`

## Endpoint Matrix

| Route | Method | Request Inputs | Target Success Response | Common Error Cases | Frontend/Mobile Fallback Expectation |
|---|---|---|---|---|---|
| `/api/v1/users/{user_id}/risk-score` | GET | Path: `user_id:int` | `RiskScoreOut` | `404` user not found, validation failure, timeout/non-2xx, malformed JSON | Return `null` score payload and render non-blocking "risk data unavailable" state. |
| `/api/v1/alerts/prioritized` | GET | Query: `user_id:int`, `limit?` (recommended `1-50`) | `list[PrioritizedAlertOut]` | missing/invalid query params, timeout/non-2xx, malformed JSON | Return empty list and keep page/app interactive with safe message. |
| `/api/v1/alerts` | GET | Existing Stage 1 query params (`alert_type?`, `severity?`, `source?`, `limit`, `offset`) | `list[AlertOut]` (unchanged Stage 1 contract) | existing Stage 1 error paths | Preserve Stage 1 behavior; no Stage 2 metadata requirement on this route. |

## Request/Response Schema Snapshot

These schema snapshots are Stage 2 target contracts derived from locked policy and current client/service scaffolding.

### `RiskScoreOut`
- `user_id: int`
- `score: float` (0.00-100.00)
- `level: "low" | "medium" | "high"`
- `base_score: float` (0.00-100.00)
- `multiplier: float` (>=1.0)

### `PrioritizedAlertOut`
- Stage 1 alert fields (`AlertOut`) plus:
- `priority_score: float` (0.00-100.00)
- `urgency_label: "low" | "medium" | "high"`
- `priority_explanation: str | null`

### Prioritization and Tie-Break Policy Snapshot
- Weighted score formula:
  - `priority = (0.45 * risk_contribution) + (0.25 * distance_score) + (0.20 * severity_score) + (0.10 * sensitivity_match_score)`
- Priority output:
  - `priority_score = round(clamp(priority, 0.0, 1.0) * 100.0, 2)`
- Urgency labels:
  - high: `>= 75`
  - medium: `>= 45 and < 75`
  - low: `< 45`
- Deterministic tie-break order:
  1. Higher `severity_score`
  2. More recent `fetched_at`
  3. Smaller `alert_id`

## Backend Source References

- API prefix/router wiring: `backend/api/router.py`
- Stage 2 scoring service scaffold: `backend/services/risk_scoring.py`
- Stage 2 prioritization service scaffold: `backend/services/alert_prioritization.py`
- Stage 2 scaffold tests: `backend/tests/test_stage2_scaffolding.py`
- Stage 2 policy lock: `docs/PLANNING_DOCS/STAGE2_DOCS/STAGE2_IMPLEMENTATION_SPEC.md`

## Implementation Status Note

As of 2026-03-17, Stage 2 client wrappers are integrated and service-level deterministic scaffolding exists. Route handlers for Stage 2 endpoints are tracked as in-progress and this contract is used as the implementation target.
