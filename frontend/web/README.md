# Web Frontend

This directory contains the PHP web application for RiskRadar.

It started as the CMPS 357 Stage 1 web extension and now includes:

- completed Stage 1 deliverables (dashboard, alerts, summaries, profile/preferences)
- account UX additions (register/login pages)
- Stage 2 kickoff integration for risk score and prioritized alerts
- Stage 3/4 scaffold pages for map, forecast, and AI assistant

## Current Deliverables

### Implemented and Live

- `public/index.php` (Dashboard)
	- Calls backend stats, alert list, and latest summary endpoints.
	- Displays total alerts, severity/type highlights, top alerts snapshot, and newest summary.
- `public/alerts.php` (Alert Explorer)
	- Reads and validates query filters (`alert_type`, `severity`, `source`, `limit`, `offset`).
	- Shows filterable alert cards with safe empty-state behavior.
- `public/alert_detail.php` (Alert Detail)
	- Loads one alert by ID and renders metadata (source, severity, location, timestamps, coordinates when present).
	- Returns an error view with proper status handling when the ID is invalid or missing.
- `public/summaries.php` (Summary Archive)
	- Supports `summary_type` and `limit` filters.
	- Displays normalized summary cards with generated time, region, and model metadata.
- `public/summary_detail.php` (Summary Detail)
	- Loads one summary by ID and renders full content and metadata.
- `public/profile.php` (Preferences Update)
	- Handles write path for existing users via `PUT users/{id}/preferences`.
	- Validates input, enforces CSRF checks, and uses session flash messages for outcomes.
- `public/register.php` (User Registration)
	- Handles account creation with server-side validation and CSRF protection.
	- Calls `POST users/register` and redirects to login on success.
- `public/login.php` (Login UI)
	- Implements validated, CSRF-protected login form scaffolding.
	- Displays clear UX messaging that backend login/auth endpoint is not yet active.

### Stage 2 Kickoff (Connected to Planned Endpoints)

- `public/risk.php` (Personal Risk Scoring)
	- Calls `GET users/{id}/risk-score`.
	- Calls `GET alerts/prioritized` with `user_id` and `limit`.
	- Renders score, derived risk level, and prioritized alert preview.

### Stage 3/4 Scaffolds

- `public/map.php` (Stage 3 scaffold)
	- Placeholder for interactive map/layer workflow.
- `public/forecast.php` (Stage 4 scaffold)
	- Placeholder for 24-48 hour forecast timeline and confidence visuals.
- `public/assistant.php` (Stage 4 scaffold)
	- Placeholder for natural-language risk assistant flow.

### Error and Fallback Pages

- `public/error.php` renders explicit error title/message with HTTP 500 behavior.
- `public/404.php` renders a dedicated not-found page.

## How the Web App Works

### Request/Render Flow

1. Public entry files in `public/` load shared bootstrap setup.
2. `services/bootstrap.php` initializes session/config and includes shared helpers.
3. Page controller calls helper/API functions from `services/`.
4. Data is normalized and sanitized before rendering.
5. A corresponding template in `views/` renders content inside shared layout wrappers.

### Service Layer

- `services/api_client.php`
	- API URL building and HTTP transport.
	- cURL-first with `file_get_contents` fallback.
	- Defensive result wrappers: `ok`, `status`, `data`, `message`.
	- Normalization for alerts, summaries, users, and risk payloads.
- `services/validators.php`
	- Allowlisted query parsing and bounded integers.
	- Registration, login, and preferences form validation.
- `services/security.php`
	- CSRF token creation/verification.
	- Session flash messaging helpers.
- `services/presentation.php`
	- Escaping helpers and formatting utilities (datetime, severity classes, risk labels).

### Layout and UI

- `components/layout.php` defines shared shell, nav, and message rendering.
- `public/assets/app.css` provides a desktop-first design system with:
	- custom color variables and gradients
	- card/panel components
	- responsive breakpoints (`960px`, `640px`)

## Directory Structure

- `public/` - HTTP entry points and static assets
- `views/` - per-page templates
- `components/` - shared layout helpers
- `services/` - API, validation, security, and presentation helpers
- `config/` - runtime app config and local override template

## Backend Endpoints Used

The current web frontend reads/writes through the existing API prefix (`/api/v1`) and uses these routes:

- `GET /alerts/stats`
- `GET /alerts`
- `GET /alerts/{id}`
- `GET /alerts/prioritized` (Stage 2 kickoff integration)
- `GET /summaries`
- `GET /summaries/latest`
- `GET /summaries/{id}`
- `POST /users/register`
- `PUT /users/{id}/preferences`
- `GET /users/{id}/risk-score` (Stage 2 kickoff integration)

When endpoints fail, return non-2xx, or emit malformed JSON, the web app fails closed to safe fallback content and user-facing warning messages.

## Configuration

Primary config file:

- `config/app.php`

Override options:

1. Copy `config/config.local.example.php` to `config/config.local.php` and customize values.
2. Or set environment variables before serving PHP:
	 - `RISKRADAR_API_BASE_URL`
	 - `RISKRADAR_API_PREFIX`
	 - `RISKRADAR_API_TIMEOUT`

Defaults:

- Base URL: `http://127.0.0.1:8000`
- API prefix: `/api/v1`
- Timeout: `5.0` seconds

## Run Locally

1. Start the backend from `backend/` using the project FastAPI workflow.
2. From repository root, serve the PHP app:

```powershell
php -S 127.0.0.1:8080 -t frontend/web/public
```

3. Open `http://127.0.0.1:8080/index.php`.

If backend port `8000` is unavailable, set `RISKRADAR_API_BASE_URL` (for example to `http://127.0.0.1:8001`) or use `config/config.local.php`.

## Security and Validation Notes

- CSRF tokens are required and verified for all POST form submissions.
- Inputs are validated with explicit constraints (length, format, allowlists).
- Output is escaped before rendering in templates.
- Query filters are sanitized and bounded before being passed to API calls.

## Stage Status Snapshot

- Stage 1 web-app extension requirements: implemented and integrated.
- Stage 2 kickoff web integration: implemented for risk and prioritization read paths.
- Stage 3 map: scaffolded page and UX placeholder.
- Stage 4 forecast + assistant: scaffolded pages and UX placeholders.

## Related Docs

- Top-level project docs: `README.md`, `docs/STAGES.md`, `docs/TODO.md`
- Stage 1 verification notes: `docs/STAGE1_VERIFICATION_EVIDENCE.md`
