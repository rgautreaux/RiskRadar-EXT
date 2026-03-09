# RiskRadar Examples

---

## Overview

This document provides practical examples of how RiskRadar currently works and how CMPS 357 stage extensions will be surfaced to users.

Examples are divided into:

- **Current implemented behavior** (active backend + API capabilities)
- **Planned stage behavior** (features defined in CMPS 357 stages)

---

## 1. Current API Examples (Implemented)

### Example A: Get Recent Alerts

**Request**

```http
GET /api/v1/alerts?limit=10
```

**Example Response**

```json
[
	{
		"id": 148,
		"source": "nws",
		"source_id": "NWS-2026-03-09-ABC123",
		"alert_type": "weather",
		"severity": "high",
		"title": "High Wind Warning",
		"description": "Strong winds expected through this evening.",
		"latitude": 34.05,
		"longitude": -118.24,
		"location_name": "Los Angeles County",
		"event_start": "2026-03-09T12:00:00Z",
		"event_end": "2026-03-09T23:00:00Z",
		"fetched_at": "2026-03-09T18:32:10Z",
		"created_at": "2026-03-09T18:32:10Z"
	}
]
```

### Example B: Get Alert Statistics

**Request**

```http
GET /api/v1/alerts/stats
```

**Example Response**

```json
{
	"total": 412,
	"by_type": {
		"weather": 160,
		"air_quality": 122,
		"wildfire": 83,
		"pollution": 31,
		"earthquake": 16
	},
	"by_severity": {
		"critical": 18,
		"high": 96,
		"moderate": 211,
		"low": 87
	}
}
```

### Example C: Generate Daily Summary

**Request**

```http
POST /api/v1/summaries/generate
```

**Example Response**

```json
{
	"id": 22,
	"title": "Environmental Digest — Mar 09, 2026",
	"content": "Today’s top risks include elevated AQI and active weather advisories...",
	"summary_type": "daily",
	"region": "US",
	"generated_at": "2026-03-09T19:10:05Z",
	"model_used": "deepseek-chat"
}
```

### Example D: Register User

**Request**

```http
POST /api/v1/users/register
Content-Type: application/json
```

```json
{
	"display_name": "Rebecca",
	"email": "rebecca@example.com",
	"password": "example-password",
	"zip_code": "90001"
}
```

**Example Response**

```json
{
	"id": 7,
	"display_name": "Rebecca",
	"email": "rebecca@example.com",
	"zip_code": "90001",
	"alert_types": "[\"all\"]",
	"notify_severity": "high",
	"created_at": "2026-03-09T19:16:44Z"
}
```

---

## 2. Current Workflow Examples (Implemented)

### Example E: Scraper Run Lifecycle

1. Scheduler starts on backend launch.
2. Registry loads legacy and config-driven scrapers.
3. Source data is fetched and normalized.
4. Alerts are deduplicated by (`source`, `source_id`).
5. New records are saved to `alerts`.
6. Run metadata is saved to `scrape_log`.

### Example F: Summary Generation Lifecycle

1. API call triggers summary generation.
2. Alerts from the recent time window are loaded.
3. Prompt templates and alert context are sent to configured LLM provider.
4. Output is persisted to `summaries`.
5. Summary is returned to client for display.

---

## 3. Stage Extension Examples (Planned)

### Example G: Personalized Risk Score (Stage 2)

**Illustrative Response Shape**

```json
{
	"user_id": 7,
	"risk_score": 72,
	"risk_level": "high",
	"factors": {
		"air_quality": "unhealthy",
		"weather": "advisory",
		"wildfire_proximity": "moderate"
	},
	"recommendation": "Limit prolonged outdoor activity today."
}
```

### Example H: Prioritized Alerts (Stage 2)

**Illustrative Ordered Output**

1. Wildfire smoke alert near user (Critical)
2. Air quality alert in user ZIP region (High)
3. Non-local weather advisory (Moderate)

### Example I: Interactive Risk Map (Stage 3)

User actions expected in the map interface:

- Zoom/pan across affected regions
- Click point/region markers for local risk detail
- View real-time severity coloring and hover metadata

### Example J: 24-48h Forecast and AI Assistant (Stage 4)

Planned user outcomes:

- Short-horizon risk trend card (next 24-48 hours)
- Forecast chart with confidence indicators
- Assistant-generated explanation of what the forecast means for travel/outdoor plans

