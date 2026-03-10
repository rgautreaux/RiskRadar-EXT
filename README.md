# RiskRadar Backend

Environmental alert monitoring and AI-powered summarization platform.

RiskRadar scrapes real-time data from government APIs and websites (weather, air quality, wildfires, pollution, earthquakes), stores alerts in a local database, and uses LLMs to generate human-readable daily digests.

---

## Architecture Overview

```
                         +---------------------+
                         |   Web Frontend       |
                         |  (Jinja2 templates)  |
                         +----------+----------+
                                    |
                         localStorage JWT token
                              fetch() calls
                                    |
                         +----------v----------+
                         |    FastAPI Server    |
                         |     (main.py)        |
                         +----+-----+-----+----+
                              |     |     |
               +--------------+     |     +---------------+
               |                    |                     |
      +--------v-------+  +--------v--------+  +---------v--------+
      |  /api/v1/alerts |  | /api/v1/summaries|  | /api/v1/users   |
      |  (alerts.py)    |  | (summaries.py)   |  | (users.py)      |
      +--------+-------+  +--------+---------+  +---------+-------+
               |                    |                      |
               +----------+---------+-----+----------------+
                          |               |
                 +--------v--------+  +---v-------------+
                 |    SQLAlchemy    |  | auth/security.py|
                 |   ORM Layer     |  | bcrypt + JWT    |
                 +--------+--------+  +-----------------+
                          |
                 +--------v--------+
                 |   SQLite DB     |
                 | (riskradar.db)  |
                 +-----------------+
```

---

## How the Frontend Connects to the Backend

The web frontend is built with **Jinja2 HTML templates** served by FastAPI. Here is the connection flow:

```
1. User opens http://localhost:8000 -> sees login page (templates/login.html)

2. User submits login form:
   Browser JS -> POST /api/v1/users/login { email, password }
   Backend (api/users.py) -> verify_password(password, user.password_hash)
                           -> create_access_token({ sub: user.id })
                           -> returns { access_token: "eyJ...", token_type: "bearer" }
   Browser JS -> localStorage.setItem('riskradar_token', token)
              -> redirect to /dashboard

3. All subsequent API calls include the JWT:
   Browser JS -> fetch('/api/v1/alerts', {
                   headers: { 'Authorization': 'Bearer eyJ...' }
                 })
   Backend (auth/security.py) -> decode JWT -> load User from DB
                               -> return data if valid
                               -> return 401 if expired/invalid

4. If 401 received -> clear token -> redirect to login
```

### Key Files for Frontend-Backend Connection

| File | Purpose |
|------|---------|
| `templates/base.html` | Shared layout + `apiFetch()` JS helper that adds JWT to all requests |
| `templates/login.html` | Login form -> calls POST `/api/v1/users/login` |
| `templates/register.html` | Registration form -> calls POST `/api/v1/users/register` |
| `templates/dashboard.html` | Alerts view -> calls GET `/api/v1/alerts` + `/alerts/stats` |
| `templates/summaries.html` | Summary view -> calls GET/POST `/api/v1/summaries` |
| `templates/settings.html` | Settings -> calls GET `/api/v1/users/me` + PUT `/preferences` |
| `auth/security.py` | Password hashing (bcrypt) + JWT create/verify + `get_current_user` dependency |
| `config/settings.py` | JWT_SECRET_KEY, JWT_ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES |
| `static/css/style.css` | All frontend styling |

---

## Scraper Pipeline

Every scraper follows the same fetch-normalize-dedup-store pipeline defined in `BaseScraper`:

```
  +------------------+
  | External Source   |    NWS API, AirNow, EPA, NASA FIRMS,
  | (API / Website)   |    USGS, config-driven sources
  +---------+--------+
            |
            v
  +---------+--------+
  | fetch_raw_data() |    Hit API or scrape website
  | Returns raw JSON  |    (httpx GET/POST, Firecrawl)
  +---------+--------+
            |
            v
  +---------+--------+
  |   normalize()    |    Map raw fields to Alert schema
  |  per raw item     |    Compute severity, extract coords
  +---------+--------+
            |
            v
  +---------+--------+
  | Deduplication     |    Check (source, source_id) unique
  | Skip if exists    |    constraint in DB
  +---------+--------+
            |
            v
  +---------+--------+
  |  Store in DB      |    INSERT new Alert rows
  |  + ScrapeLog      |    Log fetch count, duration, status
  +------------------+
```

### Three Types of Scrapers

| Type | When to Use | How to Add |
|------|-------------|------------|
| **Legacy** | Complex parsing logic | Write a Python file, register in `registry.py` |
| **GenericAPI** | Standard REST APIs | Add YAML entry to `sources.yaml` |
| **WebScraper** | Arbitrary websites | Add YAML entry to `sources.yaml` |

---

## API Endpoints

### Authentication

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/api/v1/users/register` | Public | Create account (bcrypt hashes password) |
| POST | `/api/v1/users/login` | Public | Authenticate -> returns JWT token |

### Alerts

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | `/api/v1/alerts` | Public | List alerts (paginated, filterable) |
| GET | `/api/v1/alerts/stats` | Public | Count by type and severity |
| GET | `/api/v1/alerts/{id}` | Public | Get single alert |

**Query params:** `alert_type`, `severity`, `source`, `limit` (default 50), `offset` (default 0)

### Summaries

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | `/api/v1/summaries` | Public | List summaries |
| GET | `/api/v1/summaries/latest` | Public | Most recent summary |
| POST | `/api/v1/summaries/generate` | Public | Generate daily digest via LLM |

### Users (Protected - requires Bearer token)

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | `/api/v1/users/me` | JWT | Get current user profile |
| GET | `/api/v1/users/{id}/preferences` | JWT | Get user preferences |
| PUT | `/api/v1/users/{id}/preferences` | JWT | Update preferences |
| GET | `/api/v1/users/notifications` | JWT | Get notification settings |
| PUT | `/api/v1/users/notifications` | JWT | Update notification settings |

### System

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | `/api/v1/health` | Public | Health check + DB stats |
| POST | `/api/v1/scrape/trigger` | JWT | Manually trigger all scrapers |

---

## Project Structure

```
backend/
  main.py                       # FastAPI app + lifespan (startup/shutdown)
  requirements.txt
  pytest.ini
  riskradar.db                  # SQLite database (auto-created)

  auth/                         # NEW - Authentication module
    security.py                 # bcrypt hashing, JWT create/verify, get_current_user

  api/
    router.py                   # Mounts all sub-routers under /api/v1
    alerts.py                   # GET /alerts, /alerts/stats, /alerts/{id}
    summaries.py                # GET/POST /summaries
    users.py                    # POST /register, /login, GET /me, preferences, notifications
    system.py                   # GET /health, POST /scrape/trigger

  db/
    database.py                 # SQLAlchemy engine + SessionLocal + Base
    init_db.py                  # create_all() on startup
    models.py                   # Alert, Summary, User, ScrapeLog

  config/
    settings.py                 # Pydantic BaseSettings (.env loader) - includes JWT config
    sources.yaml                # Config-driven scraper definitions

  schemas/
    alert.py                    # AlertOut, AlertStats Pydantic models
    summary.py                  # SummaryOut
    user.py                     # UserCreate, UserLogin, TokenOut, UserOut, etc.

  scrapers/
    base_scraper.py             # Abstract base: fetch -> normalize -> dedup -> store
    scheduler.py                # APScheduler job registration
    registry.py                 # Loads legacy + YAML-configured scrapers
    nws_scraper.py              # NOAA National Weather Service
    airnow_scraper.py           # EPA AirNow (air quality)
    epa_scraper.py              # EPA Envirofacts (TRI facilities)
    firms_scraper.py            # NASA FIRMS (wildfires)
    generic_api_scraper.py      # Config-driven REST API scraper
    web_scraper.py              # Firecrawl + LLM web scraper

  llm/
    summarizer.py               # Daily digest + breaking alert generation
    prompts.py                  # System/user prompt templates

  frontend/                     # NEW - HTML frontend routes
    routes.py                   # Jinja2 page routes (/, /dashboard, /summaries, /settings)

  templates/                    # NEW - Jinja2 HTML templates
    base.html                   # Shared layout + apiFetch() JS helper
    login.html                  # Login page
    register.html               # Registration page
    dashboard.html              # Alerts dashboard
    summaries.html              # AI summaries page
    settings.html               # User settings page

  static/                       # NEW - Static assets
    css/style.css               # Main stylesheet

  tests/
    conftest.py                 # Shared fixtures (in-memory DB, test client)
    test_models.py              # ORM model tests
    test_api_alerts.py          # Alert endpoint tests
    test_api_summaries.py       # Summary endpoint tests
    test_api_users.py           # User endpoint tests
    test_scrapers.py            # Scraper logic tests
    test_registry.py            # Registry loader tests
```

---

## Quick Start

### 1. Install dependencies

```bash
cd backend
python3 -m venv ../.venv
source ../.venv/bin/activate      # Linux/Mac
# ..\.venv\Scripts\activate       # Windows

pip install -r requirements.txt
```

### 2. Configure environment

Copy the example env file and fill in your keys:

```bash
cp .env.example .env
# Then edit .env with your values
```

**Minimum required settings:**

```env
# Generate a secret: python -c "import secrets; print(secrets.token_hex(32))"
JWT_SECRET_KEY=your-random-secret-here

# For summary generation (pick one provider):
LLM_PROVIDER=deepseek
LLM_MODEL=deepseek-chat
LLM_API_KEY=your-llm-api-key
```

See `.env.example` for all available settings.

### 3. Run the server

```bash
cd backend
python -m uvicorn main:app --reload --port 8000
```

The server will:
1. Create the SQLite database (`riskradar.db`)
2. Start background scrapers on staggered intervals
3. Serve the **Web Frontend** at `http://localhost:8000`
4. Serve the **REST API** at `http://localhost:8000/api/v1/`
5. Show **Swagger docs** at `http://localhost:8000/docs`

### 4. Use the web frontend

1. Open `http://localhost:8000` in your browser
2. Click "Register here" to create an account
3. Log in with your email and password
4. Browse alerts on the dashboard, view AI summaries, update settings

### 5. Use the API directly (curl examples)

```bash
# Register a new user
curl -X POST http://localhost:8000/api/v1/users/register \
  -H "Content-Type: application/json" \
  -d '{"display_name": "Test User", "email": "test@example.com", "password": "secret123"}'

# Login - get a JWT token
curl -X POST http://localhost:8000/api/v1/users/login \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "secret123"}'
# Response: { "access_token": "eyJ...", "token_type": "bearer" }

# Use the token for protected endpoints
TOKEN="eyJ..."
curl http://localhost:8000/api/v1/users/me \
  -H "Authorization: Bearer $TOKEN"

# Get alerts (public)
curl http://localhost:8000/api/v1/alerts?limit=10

# Check system health
curl http://localhost:8000/api/v1/health
```

---

## Connecting a React Native / Mobile Frontend

If building a mobile app instead of using the web frontend:

1. **Base URL**: Set your API base URL to `http://<your-ip>:8000`
2. **Login**: POST to `/api/v1/users/login` with `{ email, password }`
3. **Store token**: Save the `access_token` from the response using `expo-secure-store`
4. **Attach to requests**: Add `Authorization: Bearer <token>` header to all API calls
5. **Handle 401**: If any call returns 401, clear the stored token and redirect to login

```typescript
// Example: services/api.ts
const API_BASE = 'http://192.168.1.100:8000';

async function apiFetch(path: string, options: RequestInit = {}) {
  const token = await SecureStore.getItemAsync('jwt_token');
  const headers = {
    'Content-Type': 'application/json',
    ...(token ? { 'Authorization': `Bearer ${token}` } : {}),
    ...options.headers,
  };
  const res = await fetch(`${API_BASE}${path}`, { ...options, headers });
  if (res.status === 401) {
    await SecureStore.deleteItemAsync('jwt_token');
    // Navigate to login screen
  }
  return res;
}
```

---

## Adding a New Data Source

### Option A: REST API (no code needed)

Edit `config/sources.yaml` and add an entry under `api_sources`.

### Option B: Website (no code needed)

Add an entry under `web_sources` in `config/sources.yaml`.
Requires `FIRECRAWL_API_KEY` and `LLM_API_KEY` in `.env`.

### Option C: Custom scraper (Python)

1. Create `scrapers/my_scraper.py` extending `BaseScraper`
2. Register in `scrapers/registry.py`

See existing scrapers (nws, airnow, epa) for examples.

---

## Running Tests

```bash
cd backend
source ../.venv/bin/activate
pip install pytest pytest-mock

# Run all tests
python -m pytest -v

# Run specific test file
python -m pytest tests/test_api_alerts.py -v
```

Tests use an in-memory SQLite database and mock all external calls. No API keys needed.

---

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `JWT_SECRET_KEY` | **Yes** | Secret for signing JWT tokens |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | No | Token lifetime (default: 60) |
| `LLM_API_KEY` | For summaries | OpenAI, Anthropic, or DeepSeek API key |
| `LLM_PROVIDER` | No | `deepseek` (default), `openai`, or `anthropic` |
| `LLM_MODEL` | No | `deepseek-chat` (default) |
| `AIRNOW_API_KEY` | For air quality | AirNow API key |
| `NASA_FIRMS_MAP_KEY` | For FIRMS | NASA FIRMS MAP key |
| `FIRECRAWL_API_KEY` | For web scraping | Firecrawl API key |
| `SCRAPE_INTERVAL_MINUTES` | No | Default interval (30) |
| `DEFAULT_ZIP_CODE` | No | Default location ZIP (90001) |
| `DEFAULT_LAT` | No | Default latitude (34.0522) |
| `DEFAULT_LON` | No | Default longitude (-118.2437) |

---

## Tech Stack

| Layer | Technology |
|-------|------------|
| Framework | FastAPI + Uvicorn |
| Database | SQLite + SQLAlchemy ORM |
| Authentication | bcrypt (passlib) + JWT (python-jose) |
| Frontend | Jinja2 templates + vanilla JS |
| Scheduler | APScheduler |
| HTTP Client | httpx |
| Web Scraping | Firecrawl API |
| LLM | OpenAI / Anthropic / DeepSeek |
| Validation | Pydantic |
| Config | YAML + python-dotenv |
| Testing | pytest + pytest-mock |
