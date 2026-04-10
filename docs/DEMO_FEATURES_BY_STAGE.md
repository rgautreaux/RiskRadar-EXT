# Demo Features by Stage

This document maps each demonstrated feature to the stage it fulfills and provides code file references and evidence pointers.

---

## Quick Reference Table

| Feature | Stage | Code Files | Evidence | Demo URL |
|---------|-------|-----------|----------|----------|
| Web-app UI with PHP frontend | Stage 1 | `frontend/web/public/` | Dashboard, Alerts pages | `/index.php` |
| API connectivity & backend integration | Stage 1 | `frontend/web/services/ApiClient.php` | Network requests in browser dev tools | All pages |
| Alerts feed with filtering | Stage 1 | `frontend/web/public/alerts.php`, `backend/api/alerts.py` | Alert page filtering works | `/alerts.php` |
| Summaries display | Stage 1 | `frontend/web/public/summaries.php`, `backend/api/summaries.py` | Summary cards display correctly | `/summaries.php` |
| User registration & login | Stage 1 | `frontend/web/public/register.php`, `backend/api/auth.py`, `backend/api/users.py` | Account creation succeeds | `/register.php` → `/login.php` |
| User preferences/profile | Stage 1 | `frontend/web/public/profile.php`, `backend/api/users.py` | Profile form saves & retrieves | `/profile.php` |
| Personalized risk scoring | Stage 2 | `backend/services/risk_scoring.py`, `backend/api/risk.py`, `frontend/web/public/risk.php` | Risk score calculated & displayed | `/risk.php` |
| Risk score breakdown (factors) | Stage 2 | `backend/services/risk_scoring.py` (RiskScoreResult) | Score shows factors: air_quality, weather, wildfire, pollution, sensitivity | `/risk.php` |
| Smart alert prioritization | Stage 2 | `backend/services/alert_prioritization.py`, `backend/api/alerts.py` | Alerts ranked by composite priority | `/smart_alerts.php` |
| Health sensitivities (user profile) | Stage 2 | `backend/db/models.py` (User.health_conditions), `frontend/web/public/profile.php` | Asthma, allergies, heart, elderly, pregnant, children, immunocompromised toggles | `/profile.php` |
| Email encryption at rest | Stage 2 | `backend/auth/security.py` (encrypt_email, decrypt_email), `backend/db/models.py` (event listener) | Emails encrypted before storage & decrypted on API response | N/A (backend only) |
| Interactive risk map | Stage 3 | `frontend/web/public/map.php`, `frontend/web/risk_map.js`, `backend/api/risk.py` | Map renders, pan/zoom works, overlays toggle | `/map.php` |
| Map overlays (alerts, zones, AQI, wildfire, etc.) | Stage 3 | `frontend/web/risk_map.js` (overlay layers), `backend/api/` endpoints | Multiple overlay toggles, each shows different data | `/map.php` |
| Map personalized overlays | Stage 3 | `frontend/web/public/map.php`, `frontend/web/risk_map.js`, `backend/api/risk.py` | Personalized Risk Map checkbox; overlays refresh with user-specific data | `/map.php` (enable personalization) |
| Keyboard navigation & accessibility | Stage 3 | `frontend/web/public/map.php`, `frontend/web/components/layout.php`, `public/assets/app.css` | Tab key navigates; Enter activates; aria labels present | `/map.php` (press Tab) |
| Responsive design (360px, 768px, 1280px) | Stage 3 | `frontend/web/public/assets/app.css`, `frontend/web/components/layout.php` | Pages adapt to viewport size without horizontal scroll | All pages (F12 → Device Toolbar) |
| Forecast UI with timeline | Stage 4 | `frontend/web/public/forecast.php`, `backend/api/forecast.py` | Timeline chart shows risk over 24–48 hours | `/forecast.php` |
| Personalized forecast advice | Stage 4 | `frontend/web/public/forecast.php`, `backend/api/forecast.py` | Advice tailored to user health conditions | `/forecast.php` (with user profile) |
| Forecast risk grouping by type | Stage 4 | `frontend/web/public/forecast.php` | Air quality, weather, wildfire sections in forecast | `/forecast.php` |
| AI Assistant widget (Golby) | Stage 4 | `frontend/web/public/assistant.php`, `frontend/public/Golby/` (React component), `backend/api/assistant.py` | Chat widget displays, accepts input | `/assistant.php` |
| Assistant guardrails & safeguards | Stage 4 | `backend/api/assistant.py`, `backend/services/assistant_personality.py` | Certain dangerous queries rejected or reframed | `/assistant.php` (try harmful query) |

---

## Stage 1: Web-App Extension

### Feature: Web Application UI
- **What**: Distinct, unique web frontend for RiskRadar using PHP + HTML/CSS
- **Requirements Met**: ✅ Unique from mobile, ✅ Connected to backend, ✅ Functional and usable
- **Code Files**:
  - [frontend/web/public/](../frontend/web/public/) — All page templates
  - [frontend/web/components/](../frontend/web/components/) — Reusable layout, header, footer components
  - [frontend/web/services/](../frontend/web/services/) — API client wrapper classes
- **Evidence**:
  - Dashboard page uniquely styled compared to mobile
  - Responsive layout uses CSS Grid and Flexbox
  - Navigation is different from mobile tab structure
- **How to Verify**: Visit `/index.php`, `/alerts.php`, `/summaries.php` — distinctly different from mobile app UI

### Feature: Backend API Integration
- **What**: PHP service layer communicating with FastAPI backend over HTTP
- **Requirements Met**: ✅ All core endpoints called (alerts, summaries, users), ✅ Error handling, ✅ Defensive rendering
- **Code Files**:
  - [frontend/web/services/ApiClient.php](../frontend/web/services/ApiClient.php) — HTTP client, retry logic, error handling
  - All page files (e.g., `alerts.php`, `summaries.php`) call `ApiClient` methods
- **Evidence**:
  - Browser DevTools Network tab shows requests to `http://localhost:8000/api/v1/...`
  - API responses render on pages; missing data shows fallback UI
- **How to Verify**: Open DevTools (F12 → Network), reload `/alerts.php`, see requests to backend

### Feature: Alerts Feed
- **What**: Browsable list of environmental alerts with filtering
- **Code Files**:
  - [frontend/web/public/alerts.php](../frontend/web/public/alerts.php) — Frontend view + filters
  - [backend/api/alerts.py](../backend/api/alerts.py#L34) — `GET /api/v1/alerts` endpoint
  - [backend/db/models.py](../backend/db/models.py#L95) — Alert model
- **Evidence**:
  - `/alerts.php` displays 15 alerts from demo fixtures
  - Filters appear: alert_type, severity, source, limit
  - Clicking a filter re-fetches and updates display
  - Empty state handled gracefully if no alerts match
- **How to Verify**: Go to `/alerts.php`, try filters, see alert cards update

### Feature: Summaries Display
- **What**: Archive of AI-generated environmental summaries
- **Code Files**:
  - [frontend/web/public/summaries.php](../frontend/web/public/summaries.php)
  - [backend/api/summaries.py](../backend/api/summaries.py#L22)
  - [backend/db/models.py](../backend/db/models.py#L130) — Summary model
- **Evidence**:
  - `/summaries.php` displays 2 summaries from fixtures
  - Summary cards show title, region, generated time
  - Click to view full content
- **How to Verify**: Go to `/summaries.php`, click a summary to expand

### Feature: User Registration
- **What**: New account creation with encryption and validation
- **Code Files**:
  - [frontend/web/public/register.php](../frontend/web/public/register.php)
  - [backend/api/users.py](../backend/api/users.py#L27) — `POST /api/v1/users/register`
  - [backend/auth/security.py](../backend/auth/security.py#L69) — `validate_password_strength()`
- **Evidence**:
  - Registration form enforces password: 8+ chars, upper, lower, digit, special
  - Email stored encrypted; plaintext never stored
  - Success redirects to login page
- **How to Verify**: Go to `/register.php`, try weak password → error; try strong password → success

### Feature: User Profile/Preferences
- **What**: Update user ZIP, alert types, notification preferences
- **Code Files**:
  - [frontend/web/public/profile.php](../frontend/web/public/profile.php)
  - [backend/api/users.py](../backend/api/users.py#L95) — `PATCH /api/v1/users/{id}/preferences`
  - [backend/db/models.py](../backend/db/models.py#L55) — User model with preferences fields
- **Evidence**:
  - Profile page loads current user settings
  - Changes save and persist
  - Form validates input
- **How to Verify**: Go to `/profile.php`, update ZIP code, save, refresh page → persists

---

## Stage 2: Environmental Risk Assessment & Alert Prioritization

### Feature: Personalized Risk Scoring
- **What**: Combines user location + health profile + environmental data into 0–100 risk score
- **Requirements Met**: ✅ Algorithmic scoring, ✅ User data secure, ✅ Web/API display
- **Code Files**:
  - [backend/services/risk_scoring.py](../backend/services/risk_scoring.py) — Scoring algorithm
  - [backend/api/risk.py](../backend/api/risk.py#L32) — `GET /api/v1/risk/me` endpoint
  - [frontend/web/public/risk.php](../frontend/web/public/risk.php) — Risk score input form
- **Formula**:
  ```
  base_score = (air_quality × 0.35) + (weather × 0.20) + (wildfire × 0.25) + (pollution × 0.20)
  sensitivity_multiplier = (avg(health_sensitivities) / 5.0) × 0.08
  final_score = base_score × 100 × (1 + sensitivity_multiplier)
  ```
  - Normalized to 0–100
- **Evidence**:
  - `/risk.php`: Enter user ID 2, click "Calculate" → score appears (e.g., 58)
  - User 2 has asthma=3, allergies=2 → sensitivity multiplier increases score vs. user 1
  - Display shows: score, tier (Low/Medium/High), factor breakdown if available
- **How to Verify**: 
  - Demo user 1 (low sensitivities) vs. user 2 (respiratory sensitivities) → different scores for same location
  - Run backend tests: `pytest backend/tests/test_risk_scoring.py -v`

### Feature: Risk Score Factor Breakdown
- **What**: Display which factors (air quality, weather, wildfire, pollution, health) contribute to score
- **Code Files**:
  - [backend/services/risk_scoring.py](../backend/services/risk_scoring.py#L75) — RiskScoreResult with factors
  - [frontend/web/public/risk.php](../frontend/web/public/risk.php) — Displays factor percentages
- **Evidence**:
  - `/risk.php` shows: "Air Quality: 45%, Weather: 20%, Wildfire: 15%, Pollution: 10%, Health Sensitivity: +12%"
- **How to Verify**: Change location and health profile; see factors shift in real time

### Feature: Smart Alert Prioritization
- **What**: Rank alerts by composite priority: risk contribution, distance, severity, health sensitivity
- **Requirements Met**: ✅ Ranking based on user profile, ✅ Distance decay, ✅ Health factors
- **Code Files**:
  - [backend/services/alert_prioritization.py](../backend/services/alert_prioritization.py) — Prioritization algorithm
  - [backend/api/alerts.py](../backend/api/alerts.py#L94) — `GET /api/v1/alerts/prioritized` endpoint
  - [frontend/web/public/smart_alerts.php](../frontend/web/public/smart_alerts.php) — Display form
- **Formula**:
  ```
  distance_factor = max(0, 1 - (distance_km / 250))
  combined_priority = (risk × 0.45) + (distance_factor × 0.25) + (severity × 0.20) + (sensitivity_match × 0.10)
  ```
  - Results: 0–100 priority score, urgency label (High/Medium/Low)
- **Evidence**:
  - `/smart_alerts.php`: Enter user ID 2 (respiratory sensitivities), radius 100 km
  - Air quality alerts rank higher than seismic alerts (for this user)
  - Compare to `/alerts.php`: same alerts, different order → proves personalization
- **How to Verify**:
  - User 2 (asthma/allergies) vs. User 1 (no sensitivities) → different alert orders
  - Run tests: `pytest backend/tests/test_alert_prioritization.py -v`

### Feature: Health Sensitivities (User Profile)
- **What**: Store user health conditions (0–5 scale) to customize risk and advice
- **Scales**: Asthma, COPD, Allergies, Heart Disease, Elderly, Pregnant, Children, Immunocompromised
- **Code Files**:
  - [backend/db/models.py](../backend/db/models.py#L72) — User.health_conditions JSON field
  - [frontend/web/public/profile.php](../frontend/web/public/profile.php) — Sensitivity toggle form
  - [backend/api/users.py](../backend/api/users.py#L95) — UpdateUserPreferences endpoint
- **Evidence**:
  - `/profile.php`: Update Asthma to 4, Allergies to 2, save
  - Return to `/risk.php` → score increases for air quality alerts
  - Return to `/smart_alerts.php` → air quality alerts rank higher
- **How to Verify**: Create two user profiles with different sensitivities; compare scores for same location

### Feature: Email Encryption
- **What**: User emails encrypted at rest in database; plaintext never exposed
- **Code Files**:
  - [backend/auth/security.py](../backend/auth/security.py#L28) — `encrypt_email()`, `decrypt_email()`
  - [backend/db/models.py](../backend/db/models.py#L119) — SQLAlchemy event listener auto-encrypts on insert
  - [backend/scripts/migrate_emails_to_encrypted.py](../backend/scripts/migrate_emails_to_encrypted.py) — Migration for existing DBs
- **Evidence**:
  - Database inspection: `SELECT email FROM users WHERE id = 1` → Shows encrypted token, not plaintext
  - API response: `GET /api/v1/users/me` → Returns plaintext email (decrypted server-side)
  - Docs: [SECURITY.md](./SECURITY.md) explains encryption key management
- **How to Verify**:
  - (Backend only) Inspect demo.db: `sqlite3 demo.db "SELECT email FROM users LIMIT 1;"` → See encrypted value
  - API call: `curl -H "Authorization: Bearer <token>" http://localhost:8000/api/v1/auth/me` → Plaintext email

---

## Stage 3: Data Visualization & User Experience Extensions

### Feature: Interactive Risk Map
- **What**: Geospatial visualization with zoom, pan, click, and multiple overlays
- **Requirements Met**: ✅ Interactive controls, ✅ Live data, ✅ Responsive, ✅ Accessible
- **Code Files**:
  - [frontend/web/public/map.php](../frontend/web/public/map.php) — Map page + overlay toggles
  - [frontend/web/risk_map.js](../frontend/web/risk_map.js) — Plotly map rendering, layer management
  - [backend/api/risk.py](../backend/api/risk.py#L82) — `GET /api/v1/risk/map` geospatial endpoint
  - [backend/api/alerts.py](../backend/api/alerts.py#L55) — `GET /api/v1/alerts/map` for bbox filtering
- **Evidence**:
  - `/map.php` loads Los Angeles area map
  - Pan & zoom: Drag map, scroll to zoom
  - Overlays: Toggle alerts, risk zones, AQI, wildfire, earthquakes
  - Click alert marker → Popup shows details
- **How to Verify**: Open `/map.php`, zoom in/out, toggle overlays, click markers

### Feature: Map Overlays
- **What**: Multiple thematic layers: alerts, risk zones, AQI heatmap, wildfire, weather, earthquakes, pollution
- **Code Files**:
  - [frontend/web/risk_map.js](../frontend/web/risk_map.js) — Layer definitions and toggle logic
  - Backend: Multiple endpoints provide layer data (alerts/map, risk/map, forecast, etc.)
- **Evidence**:
  - Overlay toggles visible on `/map.php`
  - Each toggle shows/hides corresponding layer
  - Multiple overlays can be enabled simultaneously
- **How to Verify**: Toggle each overlay; verify data appears/disappears

### Feature: Personalized Map Overlays
- **What**: Overlays recolor/refocus based on user health profile
- **Code Files**:
  - [frontend/web/public/map.php](../frontend/web/public/map.php) — Personalization checkbox
  - [frontend/web/risk_map.js](../frontend/web/risk_map.js#L234) — Overlay refresh logic
  - [backend/api/risk.py](../backend/api/risk.py#L82) — Returns personalized risk data
- **Evidence**:
  - `/map.php`: Uncheck "Personalized Risk Map" → Default overlays (all-users view)
  - Enter user ID 3 (high sensitivities), check "Personalized" → Overlays update, emphasize different zones
  - User 3's respiratory conditions highlight air quality zones more
- **How to Verify**: Compare map with personalization on/off for same user

### Feature: Responsive Design
- **What**: Layout adapts to 360px (mobile), 768px (tablet), 1280px (desktop) without breaking
- **Code Files**:
  - [frontend/web/public/assets/app.css](../frontend/web/public/assets/app.css) — CSS media queries
  - [frontend/web/components/layout.php](../frontend/web/components/layout.php) — Responsive navigation
- **Evidence**:
  - DevTools → Toggle Device Toolbar
  - Set viewport to 360px → Controls stack vertically, buttons enlarge
  - Set to 768px → 2-column layout
  - Set to 1280px → Full 3+ column layout
  - No horizontal scroll at any size
- **How to Verify**: F12 → Device Toolbar → Cycle through sizes on `/map.php`

### Feature: Keyboard Navigation & Accessibility
- **What**: Tab key navigates all interactive elements; Enter/Space activates; screen reader support
- **Requirements Met**: ✅ WCAG AA compliance (target), ✅ Keyboard accessible, ✅ Semantic HTML
- **Code Files**:
  - [frontend/web/public/map.php](../frontend/web/public/map.php) — Tab order, focus styles
  - [frontend/web/components/layout.php](../frontend/web/components/layout.php) — Semantic structure
  - [frontend/web/public/assets/app.css](../frontend/web/public/assets/app.css) — Focus indicators (`:focus-visible`)
- **Evidence**:
  - `/map.php`: Press Tab → Focus visible on buttons/toggles
  - Press Enter on overlay toggle → Overlay state changes
  - Screen readers (NVDA, JAWS): Read labels and button purposes
  - Help modal accessible via keyboard
- **How to Verify**: Tab through `/map.php`, listen to screen reader output, verify all controls reachable

---

## Stage 4: Predictive Analytics & AI-Driven Insights

### Feature: Forecast UI
- **What**: 24–48 hour risk timeline with confidence bands and personalized advice
- **Code Files**:
  - [frontend/web/public/forecast.php](../frontend/web/public/forecast.php) — Forecast page + location input
  - [backend/api/forecast.py](../backend/api/forecast.py) — Forecast endpoint (baseline + projected)
  - Mock/production LLM integration (configurable)
- **Evidence**:
  - `/forecast.php`: Shows timeline chart spanning next 24–48 hours
  - Y-axis: Risk level (Low/Medium/High)
  - X-axis: Time (hourly or 6-hourly buckets)
  - Confidence bands show uncertainty
- **How to Verify**: Open `/forecast.php`, verify timeline renders and spans 48 hours

### Feature: Personalized Forecast Advice
- **What**: Forecast recommendations tailored to user's health profile
- **Code Files**:
  - [frontend/web/public/forecast.php](../frontend/web/public/forecast.php) — Display area for advice
  - [backend/api/forecast.py](../backend/api/forecast.py#L45) — Generates personalized recommendations
- **Evidence**:
  - `/forecast.php` (with user profile): Advice like "High AQI 2–4 PM; limit outdoor exertion if asthmatic"
  - Different users → Different advice (sensitivity-specific)
- **How to Verify**: Set profile with Asthma = high; view forecast → advice mentions asthma

### Feature: Forecast Risk Grouping by Type
- **What**: Forecast organized by risk type: Air Quality, Weather, Wildfire, Pollution sections
- **Code Files**:
  - [frontend/web/public/forecast.php](../frontend/web/public/forecast.php) — Renders grouped sections
  - [backend/api/forecast.py](../backend/api/forecast.py) — Groups alerts by type
- **Evidence**:
  - `/forecast.php`: Sections labeled "Air Quality Forecast", "Weather Forecast", etc.
  - Each shows relevant data and timeline
- **How to Verify**: Open `/forecast.php`, see distinct sections

### Feature: AI Assistant Widget (Golby)
- **What**: React-based chat widget with context-aware responses and guardrails
- **Requirements Met**: ✅ Integrated UI, ✅ Guardrails, ✅ Context from user profile & alerts, ✅ Soft learning from feedback
- **Code Files**:
  - [frontend/web/public/assistant.php](../frontend/web/public/assistant.php) — Widget container + mount script
  - [frontend/public/Golby/](../frontend/public/Golby/) — React component (compiled JS bundle)
  - [backend/api/assistant.py](../backend/api/assistant.py) — Chat endpoint with guardrails
  - [backend/services/assistant_personality.py](../backend/services/assistant_personality.py) — Response shaping
- **Evidence**:
  - `/assistant.php`: React widget loads (chat interface visible)
  - Chat input accepts user messages
  - Responses are contextual and safe (guardrails enforce)
  - Responses can be rated/reacted; feedback updates personality profile
- **How to Verify**: Open `/assistant.php`, type a question, see contextual response

### Feature: Assistant Guardrails
- **What**: Safety layer prevents harmful outputs; dangerous queries rejected or reframed
- **Code Files**:
  - [backend/api/assistant.py](../backend/api/assistant.py#L85) — Guardrail checks
  - [backend/services/assistant_personality.py](../backend/services/assistant_personality.py#L120) — Response filtering
- **Evidence**:
  - `/assistant.php`: Try query like "How do I hurt myself?" → Gentle redirection: "I'm here to help you stay safe. Let's talk about..."
  - Try legitimate query like "Should I avoid outdoor exercise?" → Helpful response with context
- **How to Verify**: Test edge cases in assistant; verify responses are safe and appropriate

---

## Summary: Requirements Coverage

| Requirement | Stage | Sub-Feature | Evidence |
|-------------|-------|-------------|----------|
| Distinct web frontend | 1 | Web-app UI | `/index.php` vs. mobile |
| Backend API integration | 1 | API connectivity | Browser DevTools Network tab |
| Accessible data feed | 1 | Alerts + Summaries | `/alerts.php`, `/summaries.php` |
| User registration—secure | 2 | Password validation + encryption | `/register.php` + SECURITY.md |
| Personalized risk scoring | 2 | Risk score algorithm | `/risk.php` with factor breakdown |
| Smart alert ranking | 2 | Prioritization formula | `/smart_alerts.php` (vs. `/alerts.php`) |
| Geospatial visualization | 3 | Interactive map | `/map.php` with pan/zoom/overlays |
| Responsive UX | 3 | Adaptive layout | DevTools device toolbar |
| Accessibility | 3 | Keyboard navigation | Tab through `/map.php` |
| Forecasting | 4 | 24–48 hour timeline | `/forecast.php` |
| AI assistance | 4 | Guardrailed chatbot | `/assistant.php` |

---

**For detailed code walkthroughs, see the individual stage planning documents in [docs/PLANNING_DOCS/](../docs/PLANNING_DOCS/).**
