# Documentation Synchronization Note

All top-level documentation (README, STAGES.md, TODO.md, AUTHORS.md, TRANSCRIPT.md, REFLECTION.md) has been reviewed and updated for consistency and agreement through the Stage 5 connectivity hardening and documentation synchronization sessions (2026-04-14). This ensures grading clarity, onboarding readiness, and a single source of truth for project status and history.


# RiskRadar Web-Extension User Guide

This guide walks you through how to run and use the RiskRadar Web-Extension, including all features and updates through Stage 5 connectivity hardening closeout (2026-04-14).

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
   - Enter email and password to sign in.
   - Session-based authentication is enabled (HttpOnly cookie-backed login flow).
   - Use this login before opening admin-only analytics paths.

### Profile (Preferences)
- **URL:** `/profile.php`
- **Features:**
   - Update user profile preferences for the currently logged-in user (UserID is now session-based and read-only).
   - Set ZIP code, alert types, minimum severity, device token, and health sensitivities/preferences (asthma, COPD, allergies, heart, elderly, pregnant, children, immunocompromised).
   - Save preferences and receive a success message upon update.
   - Preferences are now used for personalized risk scoring, smart alerts, and forecast advice.

**Note:** Manual entry of UserID is no longer possible; all profile updates are tied to the authenticated session user. Further manual UI/UX verification and documentation updates for this flow are assigned to Max due to current login issues for the previous implementer. Please document findings and update the project tracker accordingly.

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

### Assistant (Stage 4)
- **URL:** `/assistant.php`
- **Features:**
   - Operational Golby assistant widget for natural-language risk Q&A.
   - Supports live backend responses with local fallback behavior.
   - Includes safety guardrails for medical/legal/emergency/harmful request classes.
   - Guest users are limited by `GUEST_DAILY_LIMIT` and see a registration prompt for personalized requests.
   - Supports feedback controls that feed communication-style learning pathways.

#### Guest Chat Policy
- Anonymous users can send up to `GUEST_DAILY_LIMIT` Golby messages per day before the assistant returns a daily-limit message.
- Requests that reference personal state such as "my risk" or "my profile" are reserved for signed-in users.
- Set `GUEST_DAILY_LIMIT` in the backend environment if you want to raise or lower the guest message cap.
- Registered users are not subject to the guest message cap.

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
uvicorn main:app --reload --host 127.0.0.1 --port 8001
```

When successful, the API is available at:

- `http://127.0.0.1:8001`
- Health/root check: `http://127.0.0.1:8001/`

Notes:

- The backend uses SQLite by default, so no database server is required for local use.
- On startup, the app initializes the database and starts the scraper scheduler.

---

## 3. Start the Web Frontend

Open a second terminal in the project root and run:

```powershell
php -S 127.0.0.1:8080 -t frontend/web/public
```

Build assistant frontend assets before using `/assistant.php`:

```powershell
npm run build:web
```

Optional watch mode while iterating on assistant UI:

```powershell
npm run build:web:watch
```

Open the app in your browser:

- `http://127.0.0.1:8080/login.php`

Run the connectivity preflight before demos or manual validation:

```powershell
npm run verify:connectivity
```

---

## 4. (Optional) Change Backend URL for the Web App

By default, the web app points to:

- Base URL: `http://127.0.0.1:8001`
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

### Step A: Start at Login (Required Entry)

1. Open `http://127.0.0.1:8080/login.php`
2. Choose one of three paths:
   - **Sign in** with an existing account
   - **Create one** to open the registration form
   - **Continue as Guest** to access the app without account sign-in

Expected result: successful sign-in or guest entry opens the Dashboard and allows access to feature pages.

### Step B: Create an Account (Optional but Recommended)

1. From Login, select **Create one** (or open `http://127.0.0.1:8080/register.php`)
2. Fill in:
   - Display name
   - Email
   - Password (8+ characters)
   - ZIP code (optional)
3. Select **Create account**

Expected result: successful registration redirects to the Login page with a success message.

### Step C: Sign In or Continue as Guest

1. Open `http://127.0.0.1:8080/login.php`
2. Either sign in with your account or select **Continue as Guest**

Expected result: you are redirected to `index.php` and can navigate to protected pages.

### Step D: Set Profile Preferences

1. Open `http://127.0.0.1:8080/profile.php`
2. Enter your numeric **User ID** (created during registration)
3. Optionally set:
   - ZIP code
   - Alert types
   - Minimum severity
   - Device token
4. Select **Save preferences**

Expected result: success message and stored preference summary.

### Step E: Explore the Dashboard

1. Open `http://127.0.0.1:8080/index.php`
2. Review:
   - Total alert count
   - Highest severity bucket
   - Most common alert type
   - Top alerts snapshot
   - Latest generated summary

Use this as your high-level status page.

### Step F: Browse Alerts

1. Open `http://127.0.0.1:8080/alerts.php`
2. Use filters:
   - Alert type
   - Severity
   - Source
   - Limit
3. Select **Apply filters**
4. Open details from **View full alert details**

Expected result: filtered alert cards with metadata and timestamps.

### Step G: Browse Summaries

1. Open `http://127.0.0.1:8080/summaries.php`
2. Use filters:
   - Summary type
   - Limit
3. Select **Refresh list**
4. Open details from **Open full summary**

Expected result: summary cards with type, generated time, region, model, and full text preview.

### Step H: View Risk Score (Stage 2)

1. Open `http://127.0.0.1:8080/risk.php`
2. Enter your numeric **User ID**
3. Review:
   - Overall risk score (0-100) with tier label (Low / Medium / High)
   - Component breakdown: proximity, severity, health sensitivity, alert density

Expected result: personalized risk score with factor-level breakdown based on your location and health preferences.

### Step I: View Smart Alerts (Stage 2)

1. Open `http://127.0.0.1:8080/smart_alerts.php`
2. Enter your numeric **User ID**
3. Review the prioritized alert list ranked by urgency, proximity, and health sensitivity

Expected result: alerts sorted by composite priority score with urgency labels (High / Medium / Low).

### Step J: Interactive Map (Stage 3)

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
- Visit `http://127.0.0.1:8001/` and verify it returns a JSON status payload.
- Verify web config points to the correct API base URL and prefix.

### PHP server command fails

- Check PHP installation with `php -v`.
- Ensure PHP is on your PATH.

### Backend command fails

- Ensure virtual environment is activated.
- Re-run `pip install -r backend/requirements.txt` (or from `backend/`, `pip install -r requirements.txt`).

### Login or protected-page redirect issues

- Protected pages redirect to `/login.php` when no authenticated session and no guest session are active.
- If redirected unexpectedly, sign in again or choose **Continue as Guest** from `/login.php`.

---

## 7. Stopping the App

- In the backend terminal: `Ctrl + C`
- In the PHP server terminal: `Ctrl + C`

---

## 8. Recommended First-Time Flow

For a full first run:

1. Start backend API
2. Start PHP web server
3. Open Login (`/login.php`)
4. Choose sign-in, register, or guest path
5. Update preferences in Profile (`/profile.php`) if signed in
6. Check Dashboard (`/index.php`)
7. Explore Alerts and Summaries (`/alerts.php`, `/summaries.php`)
8. View your Risk Score and Smart Alerts (`/risk.php`, `/smart_alerts.php`) using your user ID
9. Explore the Interactive Map (`/map.php`) with live overlays and personalized risk layers

You are now ready to use and demonstrate the current RiskRadar Web-Extension features.

---

## For Graders & Evaluators

### Running the Formal Demo

RiskRadar includes a comprehensive, reproducible demo designed for academic evaluation. The demo showcases all features across Stages 1–4 with pre-populated data and detailed documentation.

**Quick Start:**
```bash
# Setup: 1 minute
npm run demo:setup
npm run demo:verify

# Demo Flow: ~12–15 minutes (see DEMO_RUNBOOK.md)
# Navigate through 6 steps covering all stages
```

**Documentation for Graders:**
- [**DEMO_RUNBOOK.md**](./docs/DEMO_RUNBOOK.md) — Complete 12–15 minute walkthrough script with presenter notes, timings, and Q&A reference
- [**DEMO_FEATURES_BY_STAGE.md**](./docs/DEMO_FEATURES_BY_STAGE.md) — Feature-to-code mapping; directly links demonstrated features to implementation files and stage requirements
- [**DEMO_ONBOARDING.md**](./docs/DEMO_ONBOARDING.md) — How to customize or extend the demo for additional test scenarios

### Demo Features Checklist

**Stage 1: Web-App Extension**
- ✅ Unique PHP web frontend (distinct from mobile)
- ✅ Backend API connectivity (all core endpoints)
- ✅ Alerts feed with filtering
- ✅ Summaries archive
- ✅ User registration & profile

**Stage 2: Risk Assessment & Prioritization**
- ✅ Personalized risk scoring (0–100)
- ✅ Risk factor breakdown (air quality, weather, wildfire, pollution, health sensitivity)
- ✅ Smart alert prioritization (composite scoring)
- ✅ Health sensitivities user profile (0–5 scale)
- ✅ Email encryption at rest

**Stage 3: Data Visualization & UX**
- ✅ Interactive geospatial risk map (pan, zoom, click)
- ✅ Multiple overlay types (alerts, risk zones, AQI, wildfire, earthquakes, pollution)
- ✅ Personalized map overlays (user-specific risk highlighting)
- ✅ Responsive design (360px, 768px, 1280px viewports)
- ✅ Accessibility (keyboard navigation, screen reader support)

**Stage 4: Predictive Analytics & AI**
- ✅ 24–48 hour risk forecast with confidence bands
- ✅ Personalized forecast advice (sensitivity-aware recommendations)
- ✅ Forecast grouping by risk type
- ✅ AI Assistant widget (Golby) with context awareness
- ✅ Guardrails & safety layer (reject/reframe dangerous queries)

### Quick Verification

To verify all features are functional:

```bash
# Backend verification (full test suite)
npm run verify:backend

# Connectivity preflight (frontend/backend wiring)
npm run verify:connectivity

# Demo database verification
npm run demo:verify

# Frontend navigation (manual)
# Navigate to: http://127.0.0.1:8080/index.php → /risk.php → /map.php → /forecast.php
```

### Common Grading Questions

**Q: How do I verify Stage 2 personalization?**
A: Navigate to `/risk.php` with User 2 vs. User 1 (same location). User 2 has asthma/allergies, so air quality alerts contribute more to their score. Compare the output.

**Q: How do I test the map accessibility?**
A: Go to `/map.php`. Press Tab to navigate overlays. Press Enter to toggle. Open browser console (F12) with a screen reader (NVDA, JAWS) to verify labels and button purposes.

**Q: Are the fetched data real or mock?**
A: Mock. Demo uses fixtures for reproducibility and determinism during grading. With `--live` flag, the system fetches real environmental data from EPA, NWS, NASA APIs (production mode).

**Q: What's the current authentication status?**
A: Session-based auth is implemented. Users log in via `/login.php`; backend issues cryptographically-signed session tokens stored in HttpOnly cookies. Admin endpoints require admin role.

### For Technical Review

Implementation highlights:
- **Risk Scoring**: [backend/services/risk_scoring.py](../backend/services/risk_scoring.py) — Weighted formula combining 5 factors
- **Alert Prioritization**: [backend/services/alert_prioritization.py](../backend/services/alert_prioritization.py) — Composite priority scoring with distance decay
- **Map Integration**: [frontend/web/risk_map.js](../frontend/web/risk_map.js) — Plotly.js geospatial layers
- **Security**: [backend/auth/security.py](../backend/auth/security.py) — Email encryption, password hashing, session tokens
- **Database Models**: [backend/db/models.py](../backend/db/models.py) — SQLAlchemy ORM with all required fields

See [DEMO_FEATURES_BY_STAGE.md](./docs/DEMO_FEATURES_BY_STAGE.md) for full code-to-feature mapping.

---

## Risk Scoring, Alert Ranking, and Personalization (Stage 4+)

### Risk Scoring Formula
- Every alert and user now receives a transparent risk score (0-100) based on:
  - Distance from user (35%)
  - Alert severity (30%)
  - User health sensitivity (25%)
  - Recency/freshness (10%)
- The formula and factor breakdown are visible in the UI (see alert details and smart alerts pages).
- Users can view a detailed breakdown of how each factor contributed to their risk score for any alert.

### Alert Ranking
- Alerts are ranked for each user by combining risk score, relevance, and severity.
- The smart alerts page shows prioritized alerts, with a breakdown of the factors for each alert.
- Tie-breaking is deterministic: priority score, severity, distance, recency, then alert ID.

### Personalization & User Preferences
- Users can update their location, health conditions, and alert preferences in the Profile page.
- These preferences directly affect risk scores and alert rankings.
- Guest users see generic results; registered users get personalized risk and alert ranking.

### How to Use
- Go to the Profile page to update your preferences.
- Visit the Smart Alerts page to see your personalized alert ranking and risk breakdown.
- Click any alert to view its detailed risk score and an explanation of the formula.
- Use the help/info tooltips to understand how your risk is calculated.

### Accessibility & Transparency
- All risk scoring and ranking logic is fully documented and visible to users.
- Explanations are available in the UI and in this guide for transparency and trust.

---

You are now ready to use and demonstrate the current RiskRadar Web-Extension features.

---

# Stage 4 Forecast UI Completion & Documentation Update Session (2026-03-31)

Summary:

This ensures all top-level documentation is in sync and the Forecast UI is fully implemented and documented for Stage 4.


# Stage 4 Documentation Synchronization & Progress Update Session (2026-04-02)

Summary:

This ensures all documentation is in sync, the Forecast UI is fully documented, and the project is ready for grading and onboarding.

---

## AI Assistant & Forecast Limitations
- The AI Assistant is for informational purposes only and does not provide emergency or real-time alerts.
- Forecasts are based on available data and may not capture sudden changes or rare events.
- Always consult official sources for critical decisions.
- Accessibility and language support are being improved in future updates.

---

## Accessibility & Navigation Testing (Stage 3+)

The interactive map and overlays are fully accessible by keyboard and screen reader. To verify accessibility and navigation features:

### Automated Testing
- Run the automated test script at `frontend/web/tests/test_map_accessibility.js` (requires Node.js, puppeteer, axe-puppeteer, jest):
  1. `npm install puppeteer axe-puppeteer jest`
   2. Start the PHP server and ensure the map is available at http://127.0.0.1:8080/map.php
  3. `npx jest frontend/web/tests/test_map_accessibility.js`
- This script checks:
  - No critical accessibility violations (axe-core)
  - Tab navigation to all controls and overlays
  - Marker modal opens with keyboard

### Manual Testing
- Use the checklist in `frontend/web/tests/test_map_accessibility.md` for keyboard, screen reader, and responsive layout verification.
- All overlays, toggles, and modals are accessible by Tab/Shift+Tab, Enter/Space, and ARIA attributes are present.
- Overlay toggling and marker focus are announced for assistive tech.

See README for more details and troubleshooting.
