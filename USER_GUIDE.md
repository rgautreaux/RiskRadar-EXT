# Documentation Synchronization Note

All top-level documentation (README, STAGES.md, TODO.md, AUTHORS.md, TRANSCRIPT.md, REFLECTION.md) has been reviewed and updated for consistency and agreement as of the Stage 3 documentation and synchronization session. This ensures grading clarity, onboarding readiness, and a single source of truth for project status and history.


# RiskRadar Web-Extension User Guide

This guide walks you through how to run and use the RiskRadar Web-Extension, including all features and updates through Stage 4.

## Documentation Navigation Hub

- Project status summary: [README.md](./README.md)
- Stage narrative and deliverables: [docs/STAGES.md](./docs/STAGES.md)
- Task tracker and evidence log: [docs/TODO.md](./docs/TODO.md)
- Planning timeline and stage history: [docs/PLANNING_DOCS/PLANNING_STAGES.md](./docs/PLANNING_DOCS/PLANNING_STAGES.md)
- Stage 1 contract and verification evidence: [docs/PLANNING_DOCS/STAGE1_DOCS/API_STAGE1_CONTRACT.md](./docs/PLANNING_DOCS/STAGE1_DOCS/API_STAGE1_CONTRACT.md), [docs/PLANNING_DOCS/STAGE1_DOCS/STAGE1_VERIFICATION_EVIDENCE.md](./docs/PLANNING_DOCS/STAGE1_DOCS/STAGE1_VERIFICATION_EVIDENCE.md)
- Stage 2 implementation spec: [docs/PLANNING_DOCS/STAGE2_DOCS/STAGE2_IMPLEMENTATION_SPEC.md](./docs/PLANNING_DOCS/STAGE2_DOCS/STAGE2_IMPLEMENTATION_SPEC.md)

## What You Can Do Right Now

## Navigating All Implemented Features

The RiskRadar Web-Extension provides a comprehensive set of features accessible via the web interface. Below is a guide to all currently implemented and accessible features, including navigation tips and usage instructions for each page.

### Dashboard
- **URL:** `/index.php`
- **Features:**
   - Overview of total alert count, highest severity, most common alert type, and a snapshot of top alerts.
   - Displays the latest generated summary.
   - All data is live from the backend API.

### Alerts
- **URL:** `/alerts.php`
- **Features:**
   - Browse current alerts with real-time data from the backend.
   - Filter by alert type, severity, source, and result limit.
   - View full alert details by selecting an alert card.
   - Safe empty-state handling if no data is available.

### Summaries
- **URL:** `/summaries.php`
- **Features:**
   - Browse backend-generated summaries.
   - Filter by summary type and result limit.
   - Open full summary details for each entry.
   - Empty-state handling for missing or malformed API payloads.

### Registration
- **URL:** `/register.php`
- **Features:**
   - Create a new account by providing display name, email, password, and optional ZIP code.
   - On success, redirects to the Login page with a success message.

### Login
- **URL:** `/login.php`
- **Features:**
   - Enter email and ZIP code to attempt login.
   - **Note:** Backend login endpoint is not yet implemented; the page will display a message explaining this limitation.

### Profile (Preferences)
- **URL:** `/profile.php`
- **Features:**
   - Update user profile preferences by entering your numeric user ID.
   - Set ZIP code, alert types, minimum severity, device token, and health sensitivities/preferences (asthma, COPD, allergies, heart, elderly, pregnant, children, immunocompromised).
   - Save preferences and receive a success message upon update.
   - Preferences are now used for personalized risk scoring, smart alerts, and forecast advice.

### Risk Page
- **URL:** `/risk.php`
- **Features:**
   - Enter your user ID and radius to view your personalized risk score and prioritized alerts.
   - Results are tailored to your location and health profile if set in your preferences.
   - Shows overall risk score (0-100), tier label (Low/Medium/High), and factor-level breakdown (proximity, severity, health sensitivity, alert density).

### Smart Alerts (Prioritized Alerts)
- **URL:** `/smart_alerts.php`
- **Features:**
   - Enter your user ID, radius, and limit to view alerts ranked by personalized priority.
   - Prioritization uses distance, severity, health sensitivity, and recency.
   - Find your user ID on the Profile page after registering.
   - Alerts are sorted by composite priority score with urgency labels (High/Medium/Low).

### Interactive Map
- **URL:** `/map.php`
- **Features:**
   - Interactive map with pan/zoom, region filter, and multiple overlay toggles (alerts, risk zones, AQI, wildfire, earthquake, weather, pollution).
   - Enter your user ID and enable "Personalized Risk Map" to view overlays tailored to your profile and preferences.
   - All map controls, overlays, and popups are accessible by keyboard and screen reader.
   - Accessible legend and help modal explaining overlay meanings and navigation.

### Forecast (Stage 4)
- **URL:** `/forecast.php`
- **Features:**
   - Predictive risk forecast UI: enter ZIP or city/state, or use your location, to view a 24–48 hour risk forecast.
   - Timeline chart with risk levels and confidence bands (static for now; dynamic data coming soon).
   - Personalized advice and grouping by risk type, using your profile sensitivities/preferences.
   - Fully integrated with backend for roundtrip updates (when backend is ready).

### Assistant (Stage 4 Scaffold)
- **URL:** `/assistant.php`
- **Features:**
   - AI assistant widget scaffold for future natural-language risk Q&A and recommendations.
   - Chat functionality and backend integration coming in a future release.

---

## Backend API Endpoints (for advanced users)

The backend exposes a REST API for all core data:

- **Alerts:** `/api/v1/alerts` (list, filter, stats, map overlays)
- **Summaries:** `/api/v1/summaries` (list, latest, by ID, generate)
- **Risk:** `/api/v1/risk` (map overlays, personalized overlays)
- **Forecast:** `/api/v1/forecast` (location-based and personalized risk forecast for 24–48 hours)
- **Users:** `/api/v1/users/register`, `/api/v1/users/{user_id}/preferences` (register, update preferences)

These endpoints are used by the frontend and can be accessed directly for integration or testing.

---
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

### Step G: View Risk Score (Stage 2)

1. Open `http://127.0.0.1:8080/risk.php`
2. Enter your numeric **User ID**
3. Review:
   - Overall risk score (0-100) with tier label (Low / Medium / High)
   - Component breakdown: proximity, severity, health sensitivity, alert density

Expected result: personalized risk score with factor-level breakdown based on your location and health preferences.

### Step H: View Smart Alerts (Stage 2)

1. Open `http://127.0.0.1:8080/smart_alerts.php`
2. Enter your numeric **User ID**
3. Review the prioritized alert list ranked by urgency, proximity, and health sensitivity

Expected result: alerts sorted by composite priority score with urgency labels (High / Medium / Low).

### Step I: Interactive Map (Stage 3)

Open `http://127.0.0.1:8080/map.php` to access the interactive risk map.

**Personalized Map Workflow:**
- Enter your numeric user ID in the "User ID for Personalized Map" field above the map controls.
- Enable the "Personalized Risk Map" toggle to view risk overlays tailored to your profile and preferences.
- If no user ID is entered, a default demo user will be used for overlays.
- All map controls, overlays, and popups are accessible by keyboard and screen reader.

**Features:**
- Region filter, overlay toggles, and personalized risk overlays.
- Keyboard navigation for map panning/zooming.
- Accessible legend and tooltips explaining overlay meanings.

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
3. Register account (`/register.php`)
4. Update preferences in Profile (`/profile.php`)
5. Check Dashboard (`/index.php`)
6. Explore Alerts and Summaries (`/alerts.php`, `/summaries.php`)
7. View your Risk Score and Smart Alerts (`/risk.php`, `/smart_alerts.php`) using your user ID
8. Explore the Interactive Map (`/map.php`) with live overlays and personalized risk layers

You are now ready to use and demonstrate the current RiskRadar Web-Extension features.

---

# Stage 4 Forecast UI Completion & Documentation Update Session (2026-03-31)

Summary:
- Forecast UI implementation completed: supports local location default, manual input, risk-type grouping, personalized advice, and user profile integration for sensitivities/preferences.
- User profile UI now allows updating health sensitivities/preferences, which are used for tailored advice and recommendations.
- Backend and frontend are fully integrated for roundtrip updates.
- All documentation (README, STAGES.md, TODO.md, AUTHORS.md, TRANSCRIPT.md, REFLECTION.md) updated and synchronized for grading, onboarding, and historical accuracy.
- Verbatim transcript of this session added to TRANSCRIPT.md; REFLECTION.md updated with session summary and per-entry summaries.
- AUTHORS.md updated with member contributions and roles for this session.
- README.md and USER_GUIDE.md expanded with new Forecast UI and personalization features, implementation details, and importance.

This ensures all top-level documentation is in sync and the Forecast UI is fully implemented and documented for Stage 4.

---

# Stage 4 Documentation Synchronization & Progress Update Session (2026-04-02)

Summary:
- Verified and documented the completion of the Forecast UI, including local/manual location input, risk-type grouping, personalized advice, and user profile integration for sensitivities/preferences.
- Updated all top-level documentation (README, STAGES.md, TODO.md, AUTHORS.md, TRANSCRIPT.md, REFLECTION.md, USER_GUIDE.md) to reflect this session's developments and ensure full synchronization.
- Added a verbatim, word-for-word transcript of this session to TRANSCRIPT.md, ensuring all entries are unique and in correct chronological order.
- Updated REFLECTION.md with a summary of this session, the developments made, why they were made, and how it betters the project, as well as a summary of each TRANSCRIPT entry.
- Updated AUTHORS.md with each member's contributions and roles for this session.
- Expanded README.md and USER_GUIDE.md with new Forecast UI and personalization features, implementation details, and importance.

This ensures all documentation is in sync, the Forecast UI is fully documented, and the project is ready for grading and onboarding.

---

## AI Assistant & Forecast Limitations
- The AI Assistant is for informational purposes only and does not provide emergency or real-time alerts.
- Forecasts are based on available data and may not capture sudden changes or rare events.
- Always consult official sources for critical decisions.
- Accessibility and language support are being improved in future updates.
