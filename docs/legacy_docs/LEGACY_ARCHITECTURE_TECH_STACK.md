# RiskRadar — Legacy Architecture & Tech Stack

> **Source:** CMPS490_docs/ARCHITECTURE.md, CMPS490_docs/PROJECT_DESCRIPTION.md,
> CMPS490_SecurityDocs/Tech Stack Reference/RiskRadar_Tech_Stack_Reference.md (post-meeting, authoritative),
> Tech Stack Pre 3_2_26 Meeting/RiskRadar_Tech_Stack_Reference.md

---

## System Overview

RiskRadar follows a three-tier architecture: a **React Native + Expo mobile frontend**, a **FastAPI Python backend** with a background scraper scheduler, and a **SQLite (dev) / MySQL (production) data layer**. An LLM layer generates plain-language risk summaries from collected alerts on demand.

```
User (Mobile Device)
       │
       │ location / zip input    display results
       ▼
┌─────────────────────────┐      ┌────────────────────────┐
│  Frontend               │      │  Background Scheduler  │
│  React Native + Expo    │      │  APScheduler (30-min)  │
│  (TypeScript)           │      └──────────┬─────────────┘
└────────────┬────────────┘                 │ fetch / scrape
             │ HTTPS /api/v1/...            ▼
             ▼                  ┌──────────────────────────────────────┐
┌─────────────────────┐        │        Environmental Data Sources    │
│  Backend API        │        │  NOAA/NWS │ AirNow │ EPA │ USGS     │
│  FastAPI (Uvicorn)  │        │  Firecrawl (web scraping + LLM)     │
└──────────┬──────────┘        └───────────────────┬──────────────────┘
           │ query / store                          │ store alerts
           ▼                                        ▼
┌──────────────────────────────────────────────────────┐
│  Data Layer: SQLite (dev) → MySQL (prod)             │
│  SQLAlchemy ORM                                       │
└──────────────────────────────────────────────────────┘
           │
           │ generate summary
           ▼
┌──────────────────────────────────────────────────┐
│  LLM Layer (configurable)                        │
│  DeepSeek (default) │ OpenAI │ Anthropic         │
└──────────────────────────────────────────────────┘
```

---

## Confirmed Tech Stack (Post-Meeting, March 2, 2026)

### Platform
Cross-platform mobile application targeting iOS and Android. Delivered via React Native with Expo managed workflow. Web output is configured (static export) but is not the primary target.

### Frontend

| Component | Value |
|---|---|
| Framework | React Native 0.81.5 |
| Build toolchain | Expo ~54.0.33 (managed workflow) |
| Language | TypeScript ~5.9.2 |
| Routing | expo-router ~6.0.23 |
| Navigation | @react-navigation/native, @react-navigation/bottom-tabs |
| Animations | react-native-reanimated ~4.1.1 |
| Runtime (dev) | Node.js (Metro bundler) |
| Testing device | Android SDK (VM) |
| New Architecture | Enabled (`newArchEnabled: true`) |

### Backend

| Component | Value |
|---|---|
| Framework | FastAPI |
| Server | Uvicorn (ASGI) |
| Language | Python |
| Background scheduler | APScheduler — 30-minute scrape interval |
| Password hashing | SHA-256 (current) — **must be upgraded before production** |
| Auth mechanism | JWT (JSON Web Tokens) |
| Message queue | Not implemented — RabbitMQ is under consideration |

### Database

| Environment | Database |
|---|---|
| Development | SQLite |
| Production (target) | MySQL |
| ORM | SQLAlchemy |
| Schema | 13-table MariaDB-compatible schema |

> **Meeting decision (3/2/26):** "We are going to be using MySQL instead of SQLite." SQLite is dev-only and temporary. The `DATABASE_URL` environment variable switches the backend between databases without code changes.

### LLM Layer

| Role | Provider | Model |
|---|---|---|
| Default | DeepSeek | `deepseek-chat` |
| Fallback | OpenAI | Configurable |
| Fallback | Anthropic | Configurable |

> **Meeting note (3/2/26):** OpenAI API costs are a bottleneck. DeepSeek was adopted as the default (`LLM_PROVIDER = "deepseek"` in `settings.py`).

### Data Sources

| Source | Data Type | Status |
|---|---|---|
| NOAA / NWS | Weather alerts | Active |
| AirNow API | Air quality (AQI) | Active |
| EPA API | Pollution data | Active |
| USGS API | Earthquakes | Active (added post-meeting) |
| Firecrawl | Web scraping + LLM extraction | Active — confirmed in-meeting |
| NASA FIRMS | Wildfire data | In codebase — **may be removed** |

> **Meeting note (3/2/26):** "We may be adding more websites as well as removing the NASA wildfire API."

### Hosting

AWS (confirmed). Specific services (EC2, Lambda, RDS, etc.) are to be determined.

---

## API Endpoints

Base path: `/api/v1/` — all served over HTTPS.

| Endpoint | Method | Description |
|---|---|---|
| `/api/v1/alerts` | GET | Retrieve stored alerts (filterable by location/type) |
| `/api/v1/alerts/{id}` | GET | Retrieve a single alert by ID |
| `/api/v1/alerts/stats` | GET | Count by type and severity |
| `/api/v1/summaries` | GET | Retrieve AI-generated summaries |
| `/api/v1/summaries/latest` | GET | Most recent summary |
| `/api/v1/summaries/generate` | POST | Trigger on-demand LLM digest |
| `/api/v1/users/register` | POST | Create a new user account |
| `/api/v1/users/login` | POST | Authenticate and receive JWT |
| `/api/v1/users/preferences` | GET/PUT | Retrieve or update alert preferences |
| `/api/v1/users/notifications` | GET/PUT | Retrieve or update notification settings |
| `/api/v1/scrape/trigger` | POST | Manually trigger a scrape run (admin) |
| `/api/v1/health` | GET | Service health check |

**Query parameters for `/api/v1/alerts`:** `alert_type`, `severity`, `source`, `limit` (default 50), `offset` (default 0)

---

## Scraper Architecture

All scrapers follow the same **fetch → normalize → deduplicate → store** pipeline defined in `BaseScraper`:

```
External Source (API / Website)
         │
         ▼ fetch_raw_data()
         │  Hit API or scrape website (httpx GET, Firecrawl)
         ▼ normalize()
         │  Map raw fields to Alert schema; compute severity, extract coords
         ▼ Deduplication
         │  Check (source, source_id) unique constraint in DB; skip if exists
         ▼ Store in DB
            INSERT new Alert rows + write ScrapeLog row
```

### Three Scraper Types

| Type | When to Use | How to Add |
|---|---|---|
| Legacy | Complex parsing logic | Write Python file, register in `registry.py` |
| GenericAPIScraper | Standard REST APIs | Add YAML entry to `config/sources.yaml` |
| WebScraper | Arbitrary websites | Add YAML entry to `config/sources.yaml` |

### Scheduler Timing

```
Time ──────────────────────────────────────────>
  t+0m   t+1m   t+3m   t+5m   t+7m
  NWS    AirNow EPA    FIRMS  USGS      (first run)
  30min  30min  60min  30min  30min     (interval)
```

---

## Data Collected

| Category | Data Points |
|---|---|
| Location | ZIP code, latitude, longitude (user-provided at registration) |
| Account | Display name, email, hashed password |
| Device | Push notification token, platform (iOS / Android) |
| Preferences | Alert type preferences (JSON), category preferences, notification settings, quiet hours |
| Behavior | Articles read, read timestamps, reading progress percentage |
| Environmental | Weather alerts, AQI readings, pollution data, seismic events, scraped web content |
| AI Output | Generated summaries, model identifier, token counts |

---

## Security Notes

### Password Hashing — SHA-256 (Must Be Upgraded)
SHA-256 is a fast general-purpose hash, which is the wrong property for password storage. A modern GPU can compute billions of SHA-256 hashes per second, making brute-force trivial. The current implementation also hashes without a per-password salt, meaning two users with the same password produce identical hashes.

**Required before production:** Migrate to `bcrypt` or `Argon2` — both are deliberately slow, include automatic per-password salting, and Argon2 adds memory-hardness defeating GPU/ASIC attacks. This is a one-line fix in `users.py`.

### CORS — Wildcard Origin (Must Be Restricted)
CORS is currently `allow_origins=["*"]` in `main.py`. This permits any domain to make cross-origin requests to the API, enabling CSRF-style attacks from arbitrary web origins.

**Required before deployment:** Lock `allow_origins` to the specific domains the application will be served from. One-line change in `main.py`.

### Rate Limiting — Not Implemented
No rate limiting exists on any endpoint. The API is vulnerable to brute-force attacks on `/login`, scraper abuse, and unintentional DoS from misbehaving clients. Each `/summaries/generate` call also directly incurs LLM billing cost.

**Required before production:** Add rate limiting via `slowapi` (Starlette-compatible). At minimum, rate-limit `/summaries/generate` and `/users/register`.

### Input Validation
Handled by Pydantic schemas on all API routes.

### API Key Management
All API keys (AirNow, NASA FIRMS, Firecrawl, LLM providers) are loaded from a `.env` file via `pydantic-settings`. Confirm `.env` is excluded from version control.

---

## Architecture Notes

### Scraper Registry
The backend uses a config-driven scraper registry (`backend/config/sources.yaml`) alongside legacy hardcoded scrapers. New API data sources can be added by extending `sources.yaml` without modifying Python code.

### RabbitMQ
RabbitMQ appears in early architecture planning but is **not implemented** in the current codebase. Background jobs run in-process via APScheduler. Per meeting (3/2/26): "Need to look into using RabbitMQ, currently localized."

### Database Migration Path
SQLAlchemy ORM abstracts the database layer; the SQLite → MySQL switch is a configuration change (`DATABASE_URL` env variable), not a code rewrite. The `2026-03-03_mariadb_scraper_alignment.sql` migration in `backend/db/migrations/` aligns the legacy MariaDB schema dump with ORM expectations.

### Antimatter (Planned, Not Implemented)
Early architecture diagrams included **Antimatter** for data security and access policy enforcement. This was a planning artifact and is not present in the codebase.

---

## Known Gaps / Open Items

| Item | Status | Note |
|---|---|---|
| SHA-256 → bcrypt/Argon2 | **Open** | Required before production |
| CORS wildcard restriction | **Open** | Required before deployment |
| Rate limiting | **Open** | Required before production |
| RabbitMQ integration | **Aspirational** | Under consideration, not started |
| NASA FIRMS removal | **Pending decision** | May be removed per meeting |
| Additional Firecrawl web sources | **TBD** | `web_sources: []` in `sources.yaml` is empty but ready |
| AWS service specifics | **TBD** | EC2, RDS, Lambda — not yet decided |
| Push notification delivery | **TBD** | Device tokens collected; delivery mechanism not confirmed |
| Role-based access control | **Not present** | Not in current schema or endpoints |

---

## Pre-Meeting vs. Post-Meeting Stack Changes (as of 3/2/26)

| Component | Before 3/2/26 | After 3/2/26 |
|---|---|---|
| LLM default | OpenAI gpt-4o-mini | DeepSeek `deepseek-chat` |
| Database (prod) | SQLite (assumed) | MySQL confirmed |
| NASA FIRMS | Active | Pending removal decision |
| USGS Earthquakes | Not present | Added |
| RabbitMQ | In architecture plans | Confirmed not implemented yet |
