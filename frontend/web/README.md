# Web Frontend

This directory contains the CMPS 357 Stage 1 PHP web-app extension for RiskRadar.

## Current Stage 1 MVP Surface

- `public/index.php` — dashboard with alert stats, top alerts snapshot, and latest summary panel
- `public/alerts.php` — alert list with filter controls and defensive empty-state behavior
- `public/summaries.php` — summary archive view with filter controls
- `public/profile.php` — registration and preference update scaffolding for backend write paths

## Structure

- `views/` — page templates rendered by public entry points
- `components/` — shared layout helpers
- `services/` — backend API wrappers, validation, security, and formatting helpers
- `public/` — public entry files and static assets
- `config/` — runtime configuration and local override template

## Configuration

The web app reads backend settings from `config/app.php`.

Override locally in one of two ways:

1. Copy `config/config.local.example.php` to `config/config.local.php` and edit the values.
2. Or set environment variables before starting PHP:
	- `RISKRADAR_API_BASE_URL`
	- `RISKRADAR_API_PREFIX`
	- `RISKRADAR_API_TIMEOUT`

Default local backend target:

- Base URL: `http://127.0.0.1:8000`
- API prefix: `/api/v1`

If port `8000` is unavailable on your machine, point the PHP app at another backend port by setting `RISKRADAR_API_BASE_URL` or by creating `config/config.local.php`.

## Run Locally

Start the backend first from `backend/` using the existing FastAPI workflow for this repository.

Then serve the PHP app from `frontend/web/public/`.

Example command when PHP is installed and on `PATH`:

```powershell
php -S 127.0.0.1:8080 -t frontend/web/public
```

Then open:

- `http://127.0.0.1:8080/index.php`

## Stage 1 Implementation Notes

- API calls normalize responses and fail closed to safe defaults for timeout, non-2xx, and malformed JSON cases.
- Forms use CSRF tokens and allowlisted validation for key inputs.
- Rendered output is escaped in shared helpers before display.
- The web layout is intentionally desktop-oriented and distinct from the mobile app flow.

## Current Limitation

PHP was installed locally during Stage 1 verification, but the executable is not yet on the user `PATH`. The app can still be served by invoking the installed binary directly from the WinGet package directory.
