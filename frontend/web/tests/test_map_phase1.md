# Phase 1 (Dynamic Data Integration) Test Script — Stage 3 Web Map

## 1. Environment/Config Test
- [ ] Set `RISKRADAR_API_BASE_URL` and `RISKRADAR_API_PREFIX` to custom values in your environment or `config/config.local.php`.
- [ ] Start backend and PHP server.
- [ ] Open the map page in the browser.
- [ ] Confirm that map data loads from the configured URLs (inspect network requests in browser dev tools).
- [ ] Change config to a different backend URL/port, reload, and confirm map fetches from new endpoint.

## 2. Data Loading Test
- [ ] With backend running and valid data, confirm map loads alert and risk overlays (no fallback UI).
- [ ] With backend stopped or endpoints returning 500, confirm fallback UI appears ("Failed to load map data from the backend.").
- [ ] With backend returning empty arrays for alerts/risk, confirm fallback UI appears ("No valid map data to display.").
- [ ] With backend returning malformed JSON, confirm fallback UI appears ("Network error while loading map data.").

## 3. Data Validation Test
- [ ] Alerts with missing/invalid lat/lon are skipped (not shown on map).
- [ ] Risk zones with invalid polygons are skipped (not shown on map).

## 4. Manual/Edge Case Test
- [ ] Test with slow backend (simulate delay) and confirm loading UI is visible until data arrives.
- [ ] Test with CORS misconfigured on backend and confirm fallback UI appears.

## 5. Documentation/Code Review
- [ ] Confirm no hardcoded API URLs remain in JS (all are injected from PHP config).
- [ ] Confirm README documents config-driven integration and usage.

---
If any test fails, note the issue and update code or docs as needed.