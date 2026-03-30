# RiskRadar — Program Execution Guide

> Step-by-step instructions for setting up, starting, and operating all components of the RiskRadar system (backend API, web frontend, and mobile app).

---

## Table of Contents

1. [Prerequisites](#1-prerequisites)
2. [Repository Setup](#2-repository-setup)
3. [Environment Configuration](#3-environment-configuration)
4. [Backend (FastAPI)](#4-backend-fastapi)
5. [Web Frontend (PHP)](#5-web-frontend-php)
6. [Mobile Frontend (Expo / React Native)](#6-mobile-frontend-expo--react-native)
7. [Database Options](#7-database-options)
8. [Running Tests](#8-running-tests)
9. [Common Operations](#9-common-operations)
10. [Troubleshooting](#10-troubleshooting)

---

## 1. Prerequisites

Install the following software before proceeding. Version numbers are minimums.

| Tool | Minimum Version | Purpose | Download |
|---|---|---|---|
| **Python** | 3.10+ | Backend API server | <https://www.python.org/downloads/> |
| **pip** | (bundled with Python) | Python package manager | — |
| **PHP** | 8.1+ | Web frontend dev server | <https://www.php.net/downloads> or `winget install PHP.PHP` on Windows |
| **Node.js** | 18+ | Mobile app tooling | <https://nodejs.org/> |
| **npm** | (bundled with Node.js) | Node package manager | — |
| **Git** | 2.30+ | Version control | <https://git-scm.com/> |

**Optional:**

| Tool | Purpose |
|---|---|
| **MariaDB / MySQL** | Production-grade database (SQLite is the default) |
| **Expo Go** (mobile app) | Run/preview the mobile app on a physical device |

### Verify installations

```bash
python --version
php --version
node --version
npm --version
git --version
```

> **Windows note:** If `python` is not recognized, try `py` instead. Make sure Python and PHP are on your system PATH.

---

## 2. Repository Setup

```bash
# Clone the repository
git clone <repository-url> cmps357-team-3
cd cmps357-team-3
```

The resulting directory layout:

```
cmps357-team-3/
├── .env                  ← You will create this (see Section 3)
├── backend/              ← FastAPI backend
├── frontend/
│   ├── web/              ← PHP web frontend
│   └── mobile/RiskRadar/ ← Expo/React Native mobile app
├── docs/                 ← Project documentation
└── riskradar_db.sql      ← Legacy MariaDB schema (optional import)
```

---

## 3. Environment Configuration

The backend reads configuration from a `.env` file located at the **repository root** (the parent of `backend/`).

### 3.1 Create the `.env` file

Create a file named `.env` in the project root with the following contents. Only the keys you intend to use require real values; the rest can be left empty.

```dotenv
# ── Database ──────────────────────────────────────────────
# Leave DATABASE_URL empty to use local SQLite (no setup needed).
# For MariaDB/MySQL, uncomment and fill in:
# DATABASE_URL=mysql+pymysql://riskradar_user:your_password@127.0.0.1:3306/riskradar_db

# ── External API Keys ────────────────────────────────────
# National Weather Service scraper works without a key.
# The others require free API keys from their respective providers.
AIRNOW_API_KEY=
NASA_FIRMS_MAP_KEY=
FIRECRAWL_API_KEY=

# ── LLM / Summarizer ─────────────────────────────────────
# Required only for generating AI summaries of alerts.
# Supported providers: deepseek, openai, anthropic
LLM_API_KEY=
LLM_PROVIDER=deepseek
LLM_MODEL=deepseek-chat

# ── App Defaults ──────────────────────────────────────────
DEFAULT_ZIP_CODE=90001
DEFAULT_LAT=34.0522
DEFAULT_LON=-118.2437
SCRAPE_INTERVAL_MINUTES=30
```

### 3.2 Key descriptions

| Variable | Required? | Description |
|---|---|---|
| `DATABASE_URL` | No | SQLAlchemy connection string. Leave blank for SQLite. |
| `AIRNOW_API_KEY` | No | API key from [AirNow](https://docs.airnowapi.org/). Enables air-quality alerts. |
| `NASA_FIRMS_MAP_KEY` | No | Map key from [NASA FIRMS](https://firms.modaps.eosdis.nasa.gov/map_key/). Enables wildfire data. |
| `FIRECRAWL_API_KEY` | No | API key from [Firecrawl](https://www.firecrawl.dev/). Enables web-based scraping sources. |
| `LLM_API_KEY` | No | API key for the chosen LLM provider. Required to generate AI summaries. |
| `LLM_PROVIDER` | No | `deepseek` (default), `openai`, or `anthropic`. |
| `LLM_MODEL` | No | Model name (e.g., `deepseek-chat`, `gpt-4o`, `claude-sonnet-4-20250514`). |
| `DEFAULT_ZIP_CODE` | No | Default US ZIP code for location-based queries. |
| `DEFAULT_LAT` / `DEFAULT_LON` | No | Default latitude/longitude (Los Angeles by default). |
| `SCRAPE_INTERVAL_MINUTES` | No | Minutes between scraper runs (default: 30). |

---

## 4. Backend (FastAPI)

### 4.1 Install Python dependencies

```bash
cd backend
pip install -r requirements.txt
```

Use a virtual environment to avoid conflicts with other projects:
>
> ```bash
> # Create and activate a virtual environment (from the backend/ directory)
> python -m venv venv
>
> # Windows (PowerShell)
> .\venv\Scripts\Activate.ps1
>
> # macOS / Linux
> source venv/bin/activate
>
> pip install -r requirements.txt
> ```

### 4.2 Start the backend server

From the `backend/` directory:

```bash
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

You should see output similar to:

```
INFO     Database initialized. Engine URL: sqlite:///...backend/riskradar.db
INFO     Scheduler started with X scrapers
INFO     Uvicorn running on http://127.0.0.1:8000
```

### 4.3 Verify the server is running

Open a browser or use `curl`:

```bash
curl http://127.0.0.1:8000/
```

Expected response:

```json
{"name": "RiskRadar API", "version": "1.0.0", "status": "running"}
```

### 4.4 Interactive API documentation

FastAPI auto-generates interactive docs:

| URL | Interface |
|---|---|
| <http://127.0.0.1:8000/docs> | Swagger UI — interactive endpoint testing |
| <http://127.0.0.1:8000/redoc> | ReDoc — read-only reference documentation |

### 4.5 What happens on startup

1. **Database initialization** — SQLAlchemy creates all tables (`alerts`, `summaries`, `users`, `scrape_log`) if they don't already exist.
2. **Scraper scheduling** — APScheduler registers all enabled scrapers from `backend/config/sources.yaml` with staggered start times to avoid simultaneous requests.
3. **API routing** — All endpoints are mounted under the `/api/v1` prefix.

### 4.6 API endpoints overview

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/v1/alerts` | List alerts (filterable by `alert_type`, `severity`, `source`, `limit`, `offset`) |
| `GET` | `/api/v1/alerts/stats` | Aggregate alert statistics |
| `GET` | `/api/v1/alerts/{alert_id}` | Get a single alert by ID |
| `GET` | `/api/v1/alerts/map` | Geospatial alert list for map rendering (filterable by `region`, `bbox`, `alert_type`, `severity`) |
| `GET` | `/api/v1/alerts/prioritized/{user_id}` | Personalized prioritized alert list for the given user (Stage 2) |
| `GET` | `/api/v1/summaries` | List AI-generated summaries |
| `GET` | `/api/v1/summaries/latest` | Get the most recent summary |
| `GET` | `/api/v1/summaries/{summary_id}` | Get a single summary by ID |
| `POST` | `/api/v1/summaries/generate` | Trigger a new daily-digest summary (requires `LLM_API_KEY`) |
| `POST` | `/api/v1/users/register` | Register a new user account |
| `PUT` | `/api/v1/users/{user_id}/preferences` | Update user notification preferences |
| `GET` | `/api/v1/risk/score/{user_id}` | Compute a personalized environmental risk score (0-100) for the user (Stage 2) |
| `GET` | `/api/v1/risk/map` | Geospatial risk overlay data for map rendering (filterable by `region`, `bbox`, `risk_level`) (Stage 3) |
| `GET` | `/api/v1/risk/map/personalized/{user_id}` | User-personalized risk overlay data for map rendering (Stage 3) |

### 4.7 Changing the port

If port 8000 is already in use, specify a different port:

```bash
uvicorn main:app --reload --host 127.0.0.1 --port 8001
```

If you change the backend port, update the web frontend configuration to match (see [Section 5.2](#52-configure-the-api-connection)).

---

## 5. Web Frontend (PHP)

The web frontend is a desktop-oriented PHP application that consumes the backend API.

### 5.1 Prerequisites

- PHP 8.1+ with the `curl` extension enabled (usually enabled by default).
- The backend server must be running (see [Section 4](#4-backend-fastapi)).

### 5.2 Configure the API connection

The web frontend reads its settings from `frontend/web/config/app.php`. By default it connects to `http://127.0.0.1:8000`.

**If you changed the backend port or host**, create a local config override:

```bash
cp frontend/web/config/config.local.example.php frontend/web/config/config.local.php
```

Edit `config.local.php`:

```php
<?php
return [
    'api' => [
        'base_url' => 'http://127.0.0.1:8001',   // match your backend port
        'prefix'   => '/api/v1',
        'timeout'  => 5.0,
    ],
];
```

Alternatively, set environment variables before starting the PHP server:

```bash
# PowerShell
$env:RISKRADAR_API_BASE_URL = "http://127.0.0.1:8001"

# Bash
export RISKRADAR_API_BASE_URL="http://127.0.0.1:8001"
```

### 5.3 Start the web frontend

From the **repository root**:

```bash
php -S 127.0.0.1:8080 -t frontend/web/public
```

### 5.4 Open the web app

Navigate to <http://127.0.0.1:8080/index.php> in your browser.

### 5.5 Available pages

| URL | Page | Description |
|---|---|---|
| `/index.php` | Dashboard | Alert stats, top 5 alerts, latest AI summary |
| `/alerts.php` | Alerts | Filterable alert list (type, severity, source) |
| `/alert_detail.php` | Alert Detail | Full detail view for a single alert |
| `/summaries.php` | Summaries | Browse AI-generated summary archive |
| `/summary_detail.php` | Summary Detail | Full detail view for a single summary |
| `/risk.php` | Risk Score | Personalized environmental risk score and factor breakdown (Stage 2) |
| `/smart_alerts.php` | Smart Alerts | Personalized prioritized alert list with urgency labels (Stage 2) |
| `/map.php` | Interactive Map | Live risk map with alert and risk overlays, personalized overlays, region filters, and accessibility support (Stage 3) |
| `/register.php` | Register | Create a new user account |
| `/login.php` | Login | User login (session support scaffolded) |
| `/profile.php` | Profile | Update notification preferences for an existing user |
| `/forecast.php` | Forecast | Short-horizon risk forecasting (Stage 4 scaffold — planned, not yet functional) |
| `/assistant.php` | Assistant | AI-driven insights assistant (Stage 4 scaffold — planned, not yet functional) |

---

## 6. Mobile Frontend (Expo / React Native)

The mobile app is built with Expo and React Native.

### 6.1 Install dependencies

```bash
cd frontend/mobile/RiskRadar
npm install
```

### 6.2 Start the Expo development server

```bash
npx expo start
```

This opens the Expo developer tools. From here you can:

- Press **`a`** to open in an Android emulator
- Press **`i`** to open in an iOS simulator (macOS only)
- Press **`w`** to open in a web browser
- Scan the QR code with the **Expo Go** app on a physical device

### 6.3 Other mobile commands

```bash
# Start directly for a specific platform
npx expo start --android
npx expo start --ios
npx expo start --web

# Lint the codebase
npm run lint
```

---

## 7. Database Options

### 7.1 SQLite (default — no setup required)

When `DATABASE_URL` is not set in `.env`, the backend automatically creates and uses a local SQLite database at `backend/riskradar.db`. This file is created on first startup.

No additional setup is needed.

### 7.2 MariaDB / MySQL (optional)

For a production-style database:

1. **Install MariaDB or MySQL** and start the service.

2. **Create the database and user:**

   ```sql
   CREATE DATABASE riskradar_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   CREATE USER 'riskradar_user'@'localhost' IDENTIFIED BY 'your_password';
   GRANT ALL PRIVILEGES ON riskradar_db.* TO 'riskradar_user'@'localhost';
   FLUSH PRIVILEGES;
   ```

3. **Set the connection string** in your `.env`:

   ```dotenv
   DATABASE_URL=mysql+pymysql://riskradar_user:your_password@127.0.0.1:3306/riskradar_db
   ```

4. **(Optional) Import the legacy schema:**

   ```bash
   mysql -u riskradar_user -p riskradar_db < riskradar_db.sql
   ```

5. **(Optional) Apply the ORM alignment migration:**

   ```bash
   mysql -u riskradar_user -p riskradar_db < backend/db/migrations/2026-03-03_mariadb_scraper_alignment.sql
   ```

6. **Start the backend** — SQLAlchemy will create any missing tables on startup.

---

## 8. Running Tests

### 8.1 Backend tests

From the `backend/` directory:

```bash
pytest
```

This runs all tests in `backend/tests/` with verbose output and short tracebacks (configured in `pytest.ini`).

To run a specific test file:

```bash
pytest tests/test_scrapers.py
pytest tests/test_api_alerts.py
```

### 8.2 Mobile app linting

```bash
cd frontend/mobile/RiskRadar
npm run lint
```

---

## 9. Common Operations

### 9.1 Triggering a manual summary generation

With the backend running and an `LLM_API_KEY` configured:

```bash
curl -X POST http://127.0.0.1:8000/api/v1/summaries/generate
```

This calls the configured LLM provider to generate a daily digest of the last 24 hours of alerts.

### 9.2 Viewing current alerts

```bash
# All alerts (default limit)
curl http://127.0.0.1:8000/api/v1/alerts

# Filter by type
curl "http://127.0.0.1:8000/api/v1/alerts?alert_type=earthquake"

# Filter by severity
curl "http://127.0.0.1:8000/api/v1/alerts?severity=high&limit=10"
```

### 9.3 Registering a user

```bash
curl -X POST http://127.0.0.1:8000/api/v1/users/register \
  -H "Content-Type: application/json" \
  -d '{"display_name": "Jane", "email": "jane@example.com", "password": "securepass123", "zip_code": "90001"}'
```

### 9.4 Adding a new data source

Edit `backend/config/sources.yaml` to add a new API source. Follow the existing USGS Earthquakes entry as a template. The scheduler picks up changes on the next restart.

### 9.5 Initializing the database manually

```bash
cd backend
python -m db.init_db
```

---

## 10. Troubleshooting

### Port already in use

```
ERROR: [Errno 10048] error while attempting to bind on address ('127.0.0.1', 8000)
```

**Fix:** Use a different port with `--port 8001` and update the web frontend config to match.

### PHP not found or not on PATH

```
'php' is not recognized as an internal or external command
```

**Fix (Windows):** Install via `winget install PHP.PHP` or download from <https://www.php.net/downloads>. Ensure the PHP directory is added to your system PATH. Restart your terminal after updating PATH.

### No alerts appearing

- **Check scraper logs** in the terminal where the backend is running. Look for `INFO` or `ERROR` messages from the scraper scheduler.
- **Verify API keys** — The NWS scraper works without a key. AirNow, FIRMS, and EPA scrapers require their respective keys in `.env`.
- **Wait for the scrape interval** — Scrapers run on a configurable interval (default: 30 minutes). The first run is staggered after startup.
- **Check manually:**
  ```bash
  curl http://127.0.0.1:8000/api/v1/alerts
  ```

### Summary generation fails

- Ensure `LLM_API_KEY` is set in `.env` with a valid key for the chosen provider.
- Ensure there are alerts in the database (summaries are generated from the last 24 hours of alerts).
- Check the backend logs for error details from the LLM provider.

### Web frontend shows "Backend API is unavailable"

- Confirm the backend server is running and accessible.
- Confirm the port in `frontend/web/config/app.php` (or `config.local.php`) matches the port the backend is running on.
- Check that PHP's `curl` extension is enabled: `php -m | findstr curl` (Windows) or `php -m | grep curl` (macOS/Linux).

### Database locked (SQLite)

If you see `database is locked` errors, ensure only one instance of the backend is running. SQLite does not support concurrent writers.

### ModuleNotFoundError on backend startup

```
ModuleNotFoundError: No module named 'fastapi'
```

**Fix:** Ensure you installed dependencies and activated your virtual environment:

```bash
cd backend
pip install -r requirements.txt
```

---

## Quick-Start Checklist

For the fastest path to a working system:

1. [ ] Clone the repository
2. [ ] Create `.env` in the project root (can be empty for basic operation)
3. [ ] Install Python dependencies: `cd backend && pip install -r requirements.txt`
4. [ ] Start the backend: `uvicorn main:app --reload --host 127.0.0.1 --port 8000`
5. [ ] Verify: open <http://127.0.0.1:8000/docs>
6. [ ] Start the web frontend: `php -S 127.0.0.1:8080 -t frontend/web/public`
7. [ ] Open the dashboard: <http://127.0.0.1:8080/index.php>
