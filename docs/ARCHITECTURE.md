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
				 │ stage work in progress    │
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

The architecture above is the active system baseline. CMPS 357 stage work extends this baseline by adding:

- A distinct web-app interface (in progress)
- Personalized risk scoring + alert prioritization (planned)
- Interactive risk map (planned)
- Predictive analytics + assistant workflows (planned)

---

## Database Architecture

The current backend ORM uses **4 primary operational tables**:

- `alerts`
- `summaries`
- `users`
- `scrape_log`

A legacy MariaDB schema snapshot (`riskradar_db.sql`) includes additional content/user tables from earlier project scope. The migration file in `backend/db/migrations/` aligns MariaDB structure to current scraper-facing ORM expectations.

For full table-level documentation and relationship details, see [DATA_MODEL.md](DATA_MODEL.md).

