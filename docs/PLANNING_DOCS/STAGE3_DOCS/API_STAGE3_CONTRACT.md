# Stage 3: Data Visualization and User Experience API Contract Matrix

This document defines the backend and frontend contracts for Stage 3, focused on interactive risk map visualization and enhanced user experience features.


## Progress (as of 2026-03-24)
- Backend endpoints `/api/v1/alerts/map` and `/api/v1/risk/map`: implemented and CORS-enabled
- API client helpers: implemented in PHP
- Web frontend: **Dynamic data integration (Phase 1) is complete. The map page fetches and renders live alert and risk data from backend endpoints.**
- Dynamic Plotly overlays, interactivity, and accessibility: in progress

- Base URL: configured by each client runtime.
- API prefix: `/api/v1`
- Content type for write requests: `application/json`
- Error-handling baseline: timeout/network failure returns normalized error object and triggers fallback UI; non-2xx response surfaces safe message; malformed/empty JSON fails closed to safe defaults.

## Stage 3 Architecture and Route Usage Flow

### Request flow (web/mobile to backend)

1. Clients call Stage 3 routes via existing or new API wrappers/services.
2. Backend computes and returns geospatial risk/alert data for map rendering.
3. API handlers return normalized payloads for map data, risk overlays, and metadata.
4. Clients render map, overlays, and fallback-safe empty states if Stage 3 routes are unavailable.

### Client integration mapping

| Client Surface         | Integration Module(s)                                   | Planned/Target Backend Routes                |
|-----------------------|--------------------------------------------------------|----------------------------------------------|
| Web risk map page     | `frontend/web/public/risk_map.php`, `api_client.php`    | `GET /api/v1/alerts/map`, `GET /api/v1/risk/map` | **Phase 1 complete: Live data integration and rendering implemented** |
| Mobile risk map view  | `frontend/mobile/RiskRadar/screens/RiskMapScreen.tsx`   | `GET /api/v1/alerts/map`, `GET /api/v1/risk/map` |

## URL and Environment Configuration

- `RISKRADAR_API_BASE_URL`
- `RISKRADAR_API_PREFIX`
- `RISKRADAR_API_TIMEOUT`

## Endpoint Matrix

| Route                  | Method | Request Inputs                | Target Success Response   | Common Error Cases         | Frontend/Mobile Fallback Expectation           |
|------------------------|--------|------------------------------|--------------------------|----------------------------|------------------------------------------------|
| `/api/v1/alerts/map`   | GET    | Query: `region?`, `bbox?`, `alert_type?`, `severity?` | `MapAlertListOut`         | invalid params, timeout, malformed JSON | Return empty map overlay, show fallback message |
| `/api/v1/risk/map`     | GET    | Query: `region?`, `bbox?`, `risk_level?`              | `MapRiskOverlayOut`       | invalid params, timeout, malformed JSON | Return empty risk overlay, show fallback message |

## Request/Response Schema Snapshot

### `MapAlertListOut`
- `alerts`: list of alert objects with lat/lon, type, severity, and metadata
- `region`: string or geo-bounds
- `generated_at`: ISO timestamp

### `MapRiskOverlayOut`
- `risk_zones`: list of geo-polygons or grid cells with risk level and score
- `region`: string or geo-bounds
- `generated_at`: ISO timestamp

## Notes
- All endpoints must support CORS for web map embedding.
- Map data should be optimized for reasonable payload size (e.g., clustering, tiling, or bounding box queries).
- Fallbacks must keep the map UI interactive even if overlays fail to load.

**Next Steps:**
- Complete frontend dynamic rendering of overlays and interactivity
- Add accessibility and fallback enhancements
- Update contract and evidence docs as features are finalized
