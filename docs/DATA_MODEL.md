# RiskRadar Data Model

---

## Overview

RiskRadar currently uses a relational model centered on real-time environmental alerts, AI-generated summaries, user preferences, and scraper run telemetry.

- Runtime ORM is implemented with **SQLAlchemy**.
- Default runtime database is **SQLite**, with optional **MariaDB** support.
- The actively used model contains **4 core tables**: `alerts`, `summaries`, `users`, and `scrape_log`.

---

## Entity-Relationship Overview

```
users (standalone)

alerts ─────────────┐
					├──> summaries (via summaries.alert_ids JSON list)
scrape_log          │
					└──> API output + LLM digest generation
```

> Note: `summaries.alert_ids` stores alert references as a JSON-encoded array rather than a normalized junction table.

---

## Alerts & AI Tables

### `alerts`

Stores normalized alerts from all scraper sources.

| Column | Type | Description |
|---|---|---|
| `id` | `INT` PK | Internal alert identifier |
| `source` | `TEXT` | Source key (e.g., `nws`, `airnow`, `epa`, `firms`, `usgs_earthquakes`) |
| `source_id` | `TEXT` | Source-provided dedup key |
| `alert_type` | `TEXT` | Domain type (weather, air quality, pollution, wildfire, earthquake) |
| `severity` | `TEXT` | Normalized severity label |
| `title` | `TEXT` | Alert headline/title |
| `description` | `TEXT` | Alert details |
| `raw_data` | `TEXT` | Raw payload serialized as JSON string |
| `latitude` | `FLOAT` | Alert latitude |
| `longitude` | `FLOAT` | Alert longitude |
| `location_name` | `TEXT` | Human-readable location |
| `event_start` | `TEXT` | Event start timestamp/text |
| `event_end` | `TEXT` | Event end timestamp/text |
| `fetched_at` | `TEXT` | Ingestion timestamp |
| `created_at` | `TEXT` | Record creation timestamp |
| `updated_at` | `TEXT` | Last update timestamp |

**Unique constraint**: (`source`, `source_id`)

### `summaries`

Stores generated digest summaries.

| Column | Type | Description |
|---|---|---|
| `id` | `INT` PK | Summary identifier |
| `title` | `TEXT` | Summary title |
| `content` | `TEXT` | LLM-generated markdown/content |
| `summary_type` | `TEXT` | Summary category (default `daily`) |
| `alert_ids` | `TEXT` | JSON array of related alert IDs |
| `region` | `TEXT` | Regional scope label |
| `generated_at` | `TEXT` | Generation timestamp |
| `model_used` | `TEXT` | LLM model identifier |
| `token_count` | `INT` | LLM token usage |
| `created_at` | `TEXT` | Record creation timestamp |

---

## User Tables

### `users`

Stores account identity and user preference fields used by API routes.

| Column | Type | Description |
|---|---|---|
| `id` | `INT` PK | User identifier |
| `device_token` | `TEXT` | Push token/device identifier |
| `display_name` | `TEXT` | Display name |
| `email` | `TEXT` | User email (unique) |
| `password_hash` | `TEXT` | SHA-256 hashed password |
| `zip_code` | `TEXT` | Location ZIP code |
| `latitude` | `FLOAT` | User latitude |
| `longitude` | `FLOAT` | User longitude |
| `alert_types` | `TEXT` | JSON array string of preferred alert types |
| `notify_severity` | `TEXT` | Minimum notification severity |
| `health_conditions` | `TEXT` | JSON array of health condition keys (e.g. `["respiratory","cardiovascular"]`) |
| `created_at` | `TEXT` | Account creation timestamp |
| `updated_at` | `TEXT` | Last update timestamp |

**Unique constraint**: `email`

---

## Operations Tables

### `scrape_log`

Tracks each scraper execution and ingestion outcome.

| Column | Type | Description |
|---|---|---|
| `id` | `INT` PK | Log identifier |
| `source` | `TEXT` | Scraper source key |
| `status` | `TEXT` | Run status (`success`, `failure`, `partial`) |
| `alerts_fetched` | `INT` | Count returned by source |
| `alerts_new` | `INT` | Newly inserted alerts |
| `error_message` | `TEXT` | Failure or warning details |
| `duration_ms` | `INT` | Runtime duration in milliseconds |
| `started_at` | `TEXT` | Run start timestamp |
| `completed_at` | `TEXT` | Run completion timestamp |

---

## Key Relationships

| Parent Table | Child Table | Relationship | Join Column(s) |
|---|---|---|---|
| `summaries` | `summary_alerts` | One-to-many | `summary_alerts.summary_id` |
| `alerts` | `summary_alerts` | One-to-many | `summary_alerts.alert_id` |
| `alerts` | `summaries` | Many-to-many (logical, JSON-linked) | `summaries.alert_ids` stores array of `alerts.id` |

`users` and `scrape_log` are currently standalone relative to ORM foreign-key constraints.

---

## Normalization Analysis

The active runtime schema is intentionally lightweight and **not fully normalized to 3NF**.

### First Normal Form (1NF) / Relational Design Tradeoffs

- **`alerts.raw_data`** stores semi-structured source payloads as serialized JSON text.
- **`summaries.alert_ids`** stores array-style references instead of a junction table.
- **`users.alert_types`** stores preference lists as JSON text.
- **`users.health_conditions`** stores health sensitivity condition keys as JSON text.

### Current normalization progress

- `summary_alerts` now provides a relational mapping for summary-to-alert links while preserving `summaries.alert_ids` for backward compatibility.
- `feedback.user_id` now has an explicit foreign key to `users.id`.

### Implications

- Faster iteration for heterogeneous external APIs.
- Simpler ingestion for source-specific payload shapes.
- More application-side parsing and less strict relational enforcement.

### Planned Evolution (Aligned with Stage 2+ Goals)

- Introduce normalized preference and risk-profile tables.
- Replace JSON-linked summary mappings with a dedicated junction table.
- Add explicit foreign keys for stronger data integrity as scoring/prioritization features mature.

