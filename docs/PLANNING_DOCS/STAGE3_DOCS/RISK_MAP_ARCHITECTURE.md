# Stage 3 Risk Map Architecture and Geospatial Field Definition

**Purpose:**
Define the technical architecture for the interactive risk map (Plotly-based) and specify the required geospatial fields for backend/frontend integration.

## 1. Map Architecture Overview
- **Frontend:** Uses Plotly.js for rendering an interactive map (pan, zoom, click, overlays).
- **Backend:** Provides two main endpoints:
  - `/api/v1/alerts/map` (returns alert markers with geospatial data)
  - `/api/v1/risk/map` (returns risk zone polygons/overlays)
- **Data Flow:**
  1. User loads map page; JS fetches data from both endpoints.
  2. Alerts are plotted as markers (lat/lon, severity, type, etc.).
  3. Risk zones are plotted as polygons (GeoJSON or array of coordinates).
  4. Overlay toggles control visibility of each layer.
  5. Region filter and user ID personalize overlays.

## 2. Required Geospatial Fields

### Alerts (per marker):
- `id`: unique alert identifier
- `latitude`: float (required)
- `longitude`: float (required)
- `type`: string (e.g., AQI, wildfire, weather)
- `severity`: string or int (e.g., Low/Medium/High or 1-5)
- `source`: string
- `timestamp`: ISO8601 string
- `title`/`description`: string

### Risk Zones (per polygon):
- `id`: unique risk zone identifier
- `region`: string (e.g., LA, TX, MS)
- `polygon`: array of [lat, lon] pairs or GeoJSON Polygon
- `risk_level`: string or int
- `label`: string
- `color`: string (for overlay)

## 3. Plotly Layer Structure
- **Base map:** OpenStreetMap or similar
- **Alert markers:** Plotly scattermapbox layer
- **Risk zones:** Plotly choroplethmapbox or filled polygon layer
- **Other overlays:** AQI, wildfire, etc. as additional layers

## 4. Accessibility & Responsiveness
- All controls must be keyboard and screen reader accessible
- Map must be responsive (mobile/desktop)

## 5. Next Steps
- Implement data transformation pipeline (S3-02)
- Integrate Plotly map in frontend (S3-03)
- Connect overlays to backend endpoints
- Add tests and accessibility checks
