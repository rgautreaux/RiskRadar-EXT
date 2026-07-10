# RiskRadar Architecture

---

## System Overview

RiskRadar currently follows a backend-centered architecture with scheduled ingestion, relational storage, and API delivery to clients.

```
┌─────────────────────────┐
│ External Data Providers │
│ NWS, AirNow, EPA, FIRMS │
│ USGS (+ config-driven)  │
└─────────────┬───────────┘
			  │
			  ▼
┌────────────────────────────────────────────┐
│ Back End (FastAPI + Python)               │
│                                            │
│  ┌───────────────┐   ┌──────────────────┐  │
│  │ APScheduler   │──>│ Scraper Registry │  │
│  │ (intervals)   │   │ + Scrapers       │  │
│  └───────────────┘   └─────────┬────────┘  │
│                                 │           │
│  ┌──────────────────────────────▼────────┐  │
│  │ SQLAlchemy ORM (alerts, users,        │  │
│  │ summaries, scrape_log)                │  │
│  └──────────────────────────────┬────────┘  │
│                                 │           │
│  ┌──────────────────────────────▼────────┐  │
│  │ API Layer (/api/v1)                  │  │
│  │ alerts, summaries, users             │  │
│  └──────────────────────────────┬────────┘  │
│                                 │           │
│  ┌──────────────────────────────▼────────┐  │
│  │ LLM Summarizer                        │  │
│  │ (OpenAI-compatible / Anthropic)       │  │
│  └───────────────────────────────────────┘  │
└──────────────────────────┬───────────────────┘
						   │
						   ▼
				 ┌───────────────────────────┐
				 │ Database                  │
				 │ SQLite (default runtime)  │
				 │ or MariaDB via DATABASE_URL│
				 └──────────────┬────────────┘
								│
								▼
				 ┌───────────────────────────┐
				 │ Client Surfaces           │
				 │ Mobile app + web extension│
				 │ Stages 1-3 web complete   │
				 └───────────────────────────┘
```

### Data Flow

1. **Scheduling**: App startup initializes DB and starts APScheduler jobs.
2. **Ingestion**: Legacy scrapers (NWS, AirNow, EPA, FIRMS) and config-driven scrapers (e.g., USGS) fetch source data.
3. **Normalization + Deduplication**: Raw records are normalized into alert payloads and deduplicated by (`source`, `source_id`).
4. **Persistence**: Alerts and scrape metrics are stored via SQLAlchemy models.
5. **Summarization**: Daily digest summaries are generated from recent alerts through the LLM summarizer.
6. **Presentation**: FastAPI routes expose alert, summary, and user endpoints for frontend clients.

### Runtime Configuration

- **Default DB**: SQLite (`backend/riskradar.db`) when `DATABASE_URL` is not set.
- **Optional DB**: MariaDB via SQLAlchemy driver in `DATABASE_URL`.
- **Source registry**: `backend/config/sources.yaml` controls config-driven API/web scrapers.
- **Default location context**: Zip and coordinates from environment-backed settings.

### Current CMPS 357 Extension Direction

The architecture above is the active system baseline. CMPS 357 stage work extends this baseline:

- **Stage 1 (Completed):** Distinct web-app interface connected to backend APIs (dashboard, alerts, summaries, profile).
- **Stage 2 (Completed):** Personalized risk scoring engine (`/api/v1/risk/score/{user_id}`) and smart alert prioritization (`/api/v1/alerts/prioritized/{user_id}`) with deterministic scoring and tie-break policy.
- **Stage 3 (Completed):** Interactive risk map with geospatial overlays (`/api/v1/alerts/map`, `/api/v1/risk/map`, `/api/v1/risk/map/personalized/{user_id}`), personalized risk layers, overlay toggles, accessibility support, and responsive design.
- **Stage 4 (Not Started):** Predictive analytics and AI-driven assistant workflows (planned if time permits).

---

## Database Architecture

The current backend ORM uses **4 primary operational tables**:

- `alerts`
- `summaries`
- `users`
- `scrape_log`

A legacy MariaDB schema snapshot (`riskradar_db.sql`) includes additional content/user tables from earlier project scope. The migration file in `backend/db/migrations/` aligns MariaDB structure to current scraper-facing ORM expectations.

For full table-level documentation and relationship details, see [DATA_MODEL.md](DATA_MODEL.md).

---

## Stage 3: Risk Map Overlay Architecture (S3-01)

### Overview
The Risk Map feature provides an interactive geospatial visualization of environmental risk zones and alerts. It leverages backend APIs to deliver map-ready data for frontend rendering using Plotly or similar libraries.

### Data Flow
1. **Backend Aggregation**: Risk and alert data are aggregated and normalized in the backend, using models such as `MapRiskZone` and `MapRiskOverlayOut` (see backend/schemas/risk_score.py).
2. **API Delivery**: Map data is exposed via endpoints such as:
	 - `/api/v1/alerts/map`
	 - `/api/v1/risk/map`
	 - `/api/v1/risk/map/personalized/{user_id}`
3. **Frontend Rendering**: The frontend fetches map data and renders overlays, supporting zoom, pan, and click interactions.

### Geospatial Data Schema
The map overlay data follows a GeoJSON-inspired structure:

```
{
	"risk_zones": [
		{
			"centroid": {"lat": float, "lon": float},
			"risk_level": "low" | "moderate" | "high",
			"risk_score": float,
			"polygon": [ {"lat": float, "lon": float}, ... ] | null
		},
		...
	],
	"region": str | object,
	"generated_at": str (ISO8601)
}
```

**Alert overlays** use similar structures, with each alert containing at minimum:

| Field         | Type   | Description                       |
|---------------|--------|-----------------------------------|
| latitude      | float  | Alert centroid latitude            |
| longitude     | float  | Alert centroid longitude           |
| severity      | str    | Normalized severity label          |
| alert_type    | str    | Domain type (weather, air, etc.)   |
| title         | str    | Alert headline/title               |
| description   | str    | Alert details                      |
| event_start   | str    | Event start timestamp              |
| event_end     | str    | Event end timestamp                |

### Implementation Notes
- Use GeoJSON for extensibility if future polygon/region overlays are needed.
- All map endpoints return data in the above schema, ready for direct frontend consumption.
- The frontend should support overlay toggles, accessibility features, and responsive design.

### Verification
- Unit tests for schema validation and sample data rendering.
- Manual map rendering with test overlays.
- Accessibility and responsive design checks.

