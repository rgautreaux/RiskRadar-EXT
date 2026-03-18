# Stage 1: Web-App Extension API Contract Matrix (Completed)

This document defines the backend contracts used by the Stage 1 PHP web-app implementation in `frontend/web/`.

- Base URL: configured via frontend environment/config.
- API prefix: `/api/v1`
- Content type for write requests: `application/json`
- Error-handling baseline for PHP wrappers:
  - Timeout or network failure: return normalized error object and render non-blocking fallback UI.
  - Non-2xx response: surface safe message, preserve page shell/navigation.
  - Malformed or empty JSON: fail closed to safe defaults (empty list, null, or zero-state card).

## Stage 1 Web Architecture and Route Usage Flow

### Request flow (web page to backend)

1. Public entrypoint receives browser request:
  - `frontend/web/public/index.php`
  - `frontend/web/public/alerts.php`
  - `frontend/web/public/summaries.php`
  - `frontend/web/public/profile.php`
2. Entrypoint loads `frontend/web/services/bootstrap.php` to initialize session, config, and shared helpers.
3. Entrypoint calls API wrapper functions in `frontend/web/services/api_client.php`.
4. Wrapper composes URL from `base_url + prefix + route`, sends HTTP request, and normalizes data.
5. Entrypoint renders corresponding `frontend/web/views/*.php` template using normalized data.
6. Template output uses escaped rendering helpers and defensive fallbacks to keep page shells usable during API failures.

### Stage 1 page-to-endpoint mapping

| Web Page | Primary Wrapper Calls | Backend Routes Used |
|---|---|---|
| `public/index.php` (Dashboard) | `rr_fetch_alert_stats`, `rr_fetch_alerts(limit=5)`, `rr_fetch_latest_summary` | `GET /api/v1/alerts/stats`, `GET /api/v1/alerts`, `GET /api/v1/summaries/latest` |
| `public/alerts.php` | `rr_fetch_alerts(filters)` | `GET /api/v1/alerts` |
| `public/summaries.php` | `rr_fetch_summaries(filters)` | `GET /api/v1/summaries` |
| `public/profile.php` | `rr_register_user`, `rr_update_preferences` | `POST /api/v1/users/register`, `PUT /api/v1/users/{user_id}/preferences` |

## URL and Environment Configuration (Local and Deployed)

Stage 1 web runtime uses `frontend/web/config/app.php` with optional overrides in `frontend/web/config/config.local.php`.

### Configuration keys

- `RISKRADAR_API_BASE_URL`: backend origin (scheme + host + port)
- `RISKRADAR_API_PREFIX`: API path prefix (Stage 1: `/api/v1`)
- `RISKRADAR_API_TIMEOUT`: request timeout in seconds

### Local development profile

- Typical backend URL: `http://127.0.0.1:8000`
- Alternate local workflow used during validation: `http://127.0.0.1:8001`
- Prefix: `/api/v1`

### Deployed/staging profile template

- Base URL should be set to deployed backend host (for example `https://<backend-host>`)
- Prefix remains `/api/v1` unless backend routing changes
- Timeout should be increased if deployment network latency requires it (for example `8-12` seconds)

### URL composition rule

The API wrapper resolves request URLs as:

`{RISKRADAR_API_BASE_URL}/{trim(RISKRADAR_API_PREFIX)}/{resource_path}`

Example:

- Base URL: `http://127.0.0.1:8001`
- Prefix: `/api/v1`
- Resource path: `alerts/stats`
- Final URL: `http://127.0.0.1:8001/api/v1/alerts/stats`

## Endpoint Matrix

| Route | Method | Request Inputs | Success Response | Common Error Cases | Frontend Fallback Expectation |
|---|---|---|---|---|---|
| `/api/v1/alerts` | GET | Query: `alert_type?`, `severity?`, `source?`, `limit` (<=200), `offset` | `list[AlertOut]` | timeout, non-2xx, malformed JSON | Show empty alerts list with retry prompt; keep dashboard usable. |
| `/api/v1/alerts/stats` | GET | None | `AlertStats` | timeout, non-2xx, malformed JSON | Show zero-state stats card and warning banner text. |
| `/api/v1/alerts/{alert_id}` | GET | Path: `alert_id:int` | `AlertOut` | `404` not found, timeout | Show not-found state for detail view and back-navigation action. |
| `/api/v1/summaries` | GET | Query: `summary_type?`, `limit?` | `list[SummaryOut]` | timeout, non-2xx, malformed JSON | Show empty summaries section and recovery message. |
| `/api/v1/summaries/latest` | GET | None | `SummaryOut` or `null` | timeout, non-2xx | Show "No summary available" panel if null/error. |
| `/api/v1/summaries/generate` | POST | None | `SummaryOut` | `404` if no alerts to summarize, timeout | Keep page active and show non-blocking generation status/error message. |
| `/api/v1/users/register` | POST | JSON body: `UserCreate` | `UserOut` | `400` duplicate email, validation failure, timeout | Preserve form values and show inline validation errors. |
| `/api/v1/users/{user_id}/preferences` | PUT | Path: `user_id:int`; JSON body: `UserPrefsUpdate` | `UserOut` | `404` user not found, validation failure, timeout | Preserve preferences form state and display save-failure notice. |

## Request/Response Schema Snapshot

### `AlertOut`
- `id: int`
- `source: str`
- `source_id: str | null`
- `alert_type: str`
- `severity: str`
- `title: str`
- `description: str | null`
- `latitude: float | null`
- `longitude: float | null`
- `location_name: str | null`
- `event_start: str | null`
- `event_end: str | null`
- `fetched_at: str`
- `created_at: str`

### `AlertStats`
- `total: int`
- `by_type: { [key: string]: number }`
- `by_severity: { [key: string]: number }`

### `SummaryOut`
- `id: int`
- `title: str`
- `content: str`
- `summary_type: str`
- `region: str | null`
- `generated_at: str`
- `model_used: str | null`

### `UserCreate` (request)
- `display_name: str`
- `email: str`
- `password: str`
- `zip_code: str | null`

### `UserPrefsUpdate` (request)
- `zip_code: str | null`
- `alert_types: string[] | null`
- `notify_severity: str | null`
- `device_token: str | null`

### `UserOut`
- `id: int`
- `display_name: str | null`
- `email: str | null`
- `zip_code: str | null`
- `alert_types: str | null` (serialized list in current backend)
- `notify_severity: str | null`
- `created_at: str`

## Backend Source References

- Router prefix and includes: `backend/api/router.py`
- Alerts routes: `backend/api/alerts.py`
- Summaries routes: `backend/api/summaries.py`
- Users routes: `backend/api/users.py`
- Alert schemas: `backend/schemas/alert.py`
- Summary schemas: `backend/schemas/summary.py`
- User schemas: `backend/schemas/user.py`