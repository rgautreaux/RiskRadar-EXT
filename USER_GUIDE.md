# RiskRadar Web-Extension User Guide

This guide walks you through how to run and use the RiskRadar Web-Extension step-by-step.

## What You Can Do Right Now

The currently functional web experience includes:

- Dashboard overview of alerts and latest summary
- Alert browsing with filters
- Summary browsing with filters
- Account registration
- Profile preference updates for an existing user

Additional pages (`Risk`, `Map`, `Forecast`, `Assistant`) are scaffolded for later stages and currently display planned feature content.

---

## 1. Prerequisites

Make sure you have these installed:

- Python 3.10+
- PHP 8+
- pip (Python package installer)

Optional but recommended:

- A virtual environment tool (venv)

---

## 2. Start the Backend API

Open a terminal in the project root and run:

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

When successful, the API is available at:

- `http://127.0.0.1:8000`
- Health/root check: `http://127.0.0.1:8000/`

Notes:

- The backend uses SQLite by default, so no database server is required for local use.
- On startup, the app initializes the database and starts the scraper scheduler.

---

## 3. Start the Web Frontend

Open a second terminal in the project root and run:

```powershell
php -S 127.0.0.1:8080 -t frontend/web/public
```

Open the app in your browser:

- `http://127.0.0.1:8080/index.php`

---

## 4. (Optional) Change Backend URL for the Web App

By default, the web app points to:

- Base URL: `http://127.0.0.1:8000`
- API prefix: `/api/v1`

If your backend runs on another port:

1. Copy `frontend/web/config/config.local.example.php`
2. Rename the copy to `frontend/web/config/config.local.php`
3. Edit `base_url` to match your backend (for example, `http://127.0.0.1:8001`)

Alternative: set environment variables before starting PHP:

- `RISKRADAR_API_BASE_URL`
- `RISKRADAR_API_PREFIX`
- `RISKRADAR_API_TIMEOUT`

---

## 5. Use the Web-Extension (Step-by-Step)

### Step A: Create an Account

1. Open `http://127.0.0.1:8080/register.php`
2. Fill in:
   - Display name
   - Email
   - Password (8+ characters)
   - ZIP code (optional)
3. Select **Create account**

Expected result: successful registration redirects you to the Login page with a success message.

### Step B: Understand Login Status

1. Open `http://127.0.0.1:8080/login.php`
2. Enter credentials and submit

Current behavior: the backend login endpoint is not implemented for Stage 1, so the page shows a message explaining login is not yet supported.

### Step C: Set Profile Preferences

1. Open `http://127.0.0.1:8080/profile.php`
2. Enter your numeric **User ID** (created during registration)
3. Optionally set:
   - ZIP code
   - Alert types
   - Minimum severity
   - Device token
4. Select **Save preferences**

Expected result: success message and stored preference summary.

### Step D: Explore the Dashboard

1. Open `http://127.0.0.1:8080/index.php`
2. Review:
   - Total alert count
   - Highest severity bucket
   - Most common alert type
   - Top alerts snapshot
   - Latest generated summary

Use this as your high-level status page.

### Step E: Browse Alerts

1. Open `http://127.0.0.1:8080/alerts.php`
2. Use filters:
   - Alert type
   - Severity
   - Source
   - Limit
3. Select **Apply filters**
4. Open details from **View full alert details**

Expected result: filtered alert cards with metadata and timestamps.

### Step F: Browse Summaries

1. Open `http://127.0.0.1:8080/summaries.php`
2. Use filters:
   - Summary type
   - Limit
3. Select **Refresh list**
4. Open details from **Open full summary**

Expected result: summary cards with type, generated time, region, model, and full text preview.

### Step G: Review Future-Stage Pages

The following routes are available as scaffolds (non-final functionality):

- `http://127.0.0.1:8080/risk.php` (Stage 2)
- `http://127.0.0.1:8080/map.php` (Stage 3)
- `http://127.0.0.1:8080/forecast.php` (Stage 4)
- `http://127.0.0.1:8080/assistant.php` (Stage 4)

They describe planned features but do not yet provide live Stage 2-4 workflows.

---

## 6. Quick Troubleshooting

### Web page says no data / empty state

- Confirm backend is running on the expected port.
- Visit `http://127.0.0.1:8000/` and verify it returns a JSON status payload.
- Verify web config points to the correct API base URL and prefix.

### PHP server command fails

- Check PHP installation with `php -v`.
- Ensure PHP is on your PATH.

### Backend command fails

- Ensure virtual environment is activated.
- Re-run `pip install -r backend/requirements.txt` (or from `backend/`, `pip install -r requirements.txt`).

### Login does not work even with valid account

- This is expected in Stage 1. Registration and preference updates are available; backend login auth flow is not yet implemented.

---

## 7. Stopping the App

- In the backend terminal: `Ctrl + C`
- In the PHP server terminal: `Ctrl + C`

---

## 8. Recommended First-Time Flow

For a full first run:

1. Start backend API
2. Start PHP web server
3. Register account
4. Update preferences in Profile
5. Check Dashboard
6. Explore Alerts and Summaries
7. Review scaffold pages for upcoming stages

You are now ready to use and demonstrate the current RiskRadar Web-Extension features.
