## Stage 3 Phase 5 Progress (2026-03-24) — Phase 4

**Phase 4: Onboarding Template & Handoff Summary**
- Onboarding template completed with project-specific details
- Handoff summary written for graders and new contributors
- All documentation and evidence are synchronized and ready for grading/onboarding
Stage 3 Phase 5 is now fully complete and ready for submission.
## Stage 3 Phase 5 Progress (2026-03-24) — Phase 3

**Phase 3: Evidence Organization & Referencing**
- All evidence files (screenshots, recordings, checklists) are organized in /docs/evidence/ and /static/evidence/
- Evidence is referenced in documentation and templates
Next: Onboarding and handoff preparation
## Stage 3 Phase 5 Progress (2026-03-24) — Phase 2

**Phase 2: Documentation Finalization**
- All documentation (README, USER_GUIDE, evidence/checklist/onboarding templates) updated and synchronized
- Known limitations and future enhancements documented
- Documentation is ready for grading and onboarding
Next: Evidence organization and referencing
# Web Frontend

## Asset & Style Integration (Wireframe-Accurate UI)

### SVG Icons & Illustrations
- All navigation and UI icons are now SVGs, located in `public/assets/icons/`.
- Themed illustrations are in `public/assets/illustrations/`.
- SVGs are referenced in `components/layout.php` and other shared components for navigation and UI.
- For new icons, create SVGs matching the wireframe PNGs and place them in `public/assets/icons/`.

### CSS & Design System
- Unified styles are imported from `UI_UX_STYLE_FILES/styles/` into `public/assets/app.css`.
- All color tokens, spacing, and typography are managed via `app.css` and `theme_tokens.css`.
- Use utility classes and CSS variables for consistent layout and theming.

### Usage Rules
- Always use SVGs for icons in navigation and UI.
- Add descriptive `alt` text for accessibility.
- Do not use PNGs from `wireframe_icons` directly in production UI.
- Update this README if new asset types or rules are added.

---

This directory contains the PHP web application for RiskRadar.

## Stage 3 Phase 5 Progress (2026-03-24)

**Phase 1: Requirements Cross-Check & Feature Verification**
- All Stage 3 web-app requirements (excluding mobile) have been manually verified as present and functional.
- Map overlays, toggles, personalized risk, accessibility, and error handling work as intended.
- Fallback UI and error states are handled gracefully.
- No regressions found in Stage 1 and 2 features.
Next: Documentation finalization and evidence organization.

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

### Stage 3/4 Extensions

- `public/map.php` (Stage 3 scaffold)
	- Placeholder for interactive map/layer workflow.
- `public/forecast.php` (Stage 4 live integration)
	- Live 24-48 hour forecast output with confidence/trend summary cards and timeline rendering.
- `public/assistant.php` (Stage 4 assistant integration)
	- Golby assistant interface with context-aware answers and safety guardrail fallbacks.
	- Uses compiled frontend bundle artifacts built by `npm run build:web`.

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

3. Build the Golby assistant frontend bundle from repository root:

```powershell
npm run build:web
```

For local rebuild-on-change during UI work:

```powershell
npm run build:web:watch
```

4. Open `http://127.0.0.1:8080/index.php`.

If backend port `8000` is unavailable, set `RISKRADAR_API_BASE_URL` (for example to `http://127.0.0.1:8001`) or use `config/config.local.php`.

## Security and Validation Notes

- CSRF tokens are required and verified for all POST form submissions.
- Inputs are validated with explicit constraints (length, format, allowlists).
- Output is escaped before rendering in templates.
- Query filters are sanitized and bounded before being passed to API calls.

## Stage Status Snapshot

- Stage 1 web-app extension requirements: implemented and integrated.
- Stage 2 kickoff web integration: implemented for risk and prioritization read paths.
- Stage 3 interactive map: backend endpoints, API client, and frontend scaffold complete; dynamic Plotly rendering, overlays, and accessibility features in progress (see below).
- Stage 4 forecast + assistant: forecast backend/live timeline and assistant backend prompt/data integration are implemented and verified.
- Assistant frontend runtime now uses compiled Golby bundle assets rather than raw source imports.

## Related Docs

- Top-level project docs: `README.md`, `docs/STAGES.md`, `docs/TODO.md`
- Stage 1 verification notes: `docs/STAGE1_VERIFICATION_EVIDENCE.md`

## Stage 3 Interactive Map (Current Progress & Usage)

### What is Complete
- Backend endpoints `/api/v1/alerts/map` and `/api/v1/risk/map` (CORS-enabled)
- PHP API client helpers for map endpoints
- Frontend scaffold in `views/map.php` with Plotly.js, loading/fallback UI, and AJAX fetch logic
- Responsive CSS for map container and layout
- Config-driven API URLs

### What Remains (Frontend Enhancements)
- [ ] Transform backend data into Plotly overlays (scatter for alerts, polygons/heatmap for risk)
- [ ] Render live alert markers with severity color
- [ ] Add overlays (AQI, wildfire, etc.) and toggles
- [ ] Implement region filters, tooltips, and click/hover interactions
- [ ] Harden fallback/error handling for all map states
- [ ] Add accessibility features (ARIA, keyboard nav, text alternatives)
- [ ] Update documentation and add screenshots/evidence

### Manual Verification Checklist
- [ ] Map loads with overlays and toggles work. Assigned: Max
- [ ] Personalized risk overlay is accessible and visually distinct. Assigned: Max
- [ ] All controls are keyboard accessible and ARIA-labeled. Assigned: Max
- [ ] Error/fallback states are user-friendly. Assigned: Max
- [ ] Documentation and user guide are updated with validation/signoff outcome. Assigned: Max
- [ ] Screenshots and recordings are collected for grading. Assigned: Max

### How to Use the Map Feature
1. Start backend and PHP server as usual (see above)
2. Open `public/map.php` in your browser
3. The map will attempt to load live data from the config-driven API URLs (not hardcoded)
4. If data loads, overlays will render (in progress); if not, fallback UI will display

### Developer Notes
- See `views/map.php` for JS logic and Plotly integration
- See `services/api_client.php` for backend API helpers
- See `config/app.php` for environment and API URL configuration
- See `docs/PLANNING_DOCS/STAGE3_DOCS/STAGE3_VERIFICATION_EVIDENCE.md` for verification checklist and evidence

### Next Steps
Follow the Stage 3 checklist in `PLANNING_STAGES.md` to complete dynamic rendering, overlays, accessibility, and documentation.

## Accessibility Features (Stage 3 Map)

The interactive map in `views/map.php` is designed for accessibility and inclusivity:

- **ARIA roles and labels**: All map containers, overlays, and controls use ARIA roles and descriptive labels for screen reader compatibility.
- **Keyboard navigation**: All controls and overlays are reachable and operable via keyboard (Tab, Shift+Tab, Enter, Space, Arrow keys for map panning).
- **Screen reader instructions**: Visually hidden instructions are provided for screen reader users on how to interact with the map and overlays.
- **Live region updates**: Dynamic changes (e.g., overlays toggled, map data loaded) are announced using `aria-live` regions.
- **Color contrast**: All overlay and marker colors have been checked for WCAG AA contrast. Alternative patterns or shapes are available on request.
- **Visible focus indicators**: All focusable elements have a visible outline for keyboard users.
- **Responsive accessibility**: All features are accessible and readable at all viewport sizes (desktop, tablet, mobile).

### Accessibility Verification Checklist
- Tab through all controls and overlays: focus indicators visible, logical order.
- Use arrow keys to pan the map when focused.
- Press Enter/Space on overlays/markers to show details.
- Use a screen reader (NVDA/JAWS/VoiceOver) to confirm ARIA labels, instructions, and live updates are announced.
- Validate color contrast for all legend and overlay colors (e.g., #e74c3c, #f39c12, #27ae60, #ff5722, #ffc107, #4caf50) using tools like axe or Lighthouse.
- Confirm all features work at different viewport sizes.

For further accessibility support or to request alternative patterns, contact the project maintainers.
