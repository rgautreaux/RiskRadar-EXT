# RiskRadar Datasets

---

## 1. Active Environmental Datasets (Currently Integrated)

These datasets are actively consumed by implemented scrapers in the backend runtime.

**1. National Weather Service (NWS) Alerts API**
- Source: https://api.weather.gov/alerts/active
- Supporting endpoint: https://api.weather.gov/points/{lat},{lon}
- Data provided:
	- Active weather alerts and advisories
	- Event timing (`onset`, `expires`)
	- Severity/urgency metadata
	- Area/location descriptions
- RiskRadar usage:
	- Produces `weather` alerts
	- Uses source event IDs for deduplication

**2. AirNow Current Observations API**
- Source: https://www.airnowapi.org/aq/observation/zipCode/current/
- Data provided:
	- Current AQI observations by ZIP code
	- Pollutant category and index
	- Air quality descriptors
- RiskRadar usage:
	- Produces `air_quality` alerts
	- Severity derived from AQI category/value interpretation

**3. EPA Envirofacts / TRI Facility Data Service**
- Source: https://data.epa.gov/efservice/tri_facility/state_abbr/CA/rows/0:24/JSON
- Data provided:
	- Facility identity and location data
	- Environmental reporting fields from TRI feed
- RiskRadar usage:
	- Produces `pollution` alerts
	- Captures location and source context for downstream summaries

**4. NASA FIRMS Fire Data API**
- Source family: https://firms.modaps.eosdis.nasa.gov/api/
- Data provided:
	- Satellite-detected fire points
	- Coordinates, acquisition dates/times, confidence indicators
- RiskRadar usage:
	- Produces `wildfire` alerts
	- Uses FIRMS map-key authenticated endpoint and geospatial normalization

**5. USGS Earthquake API (Config-Driven Source)**
- Source: https://earthquake.usgs.gov/fdsnws/event/1/query
- Data provided:
	- GeoJSON earthquake events
	- Magnitude, place, event timestamp, geometry coordinates
- RiskRadar usage:
	- Produces `earthquake` alerts via the generic API scraper
	- Severity mapped from magnitude thresholds in `sources.yaml`

---

## 2. Configurable/Extensible Dataset Support

RiskRadar supports adding new sources without changing core scheduler code.

**1. Config-Driven API Sources (`api_sources`)**
- Declared in `backend/config/sources.yaml`
- Supports:
	- Auth modes (`none`, query param key, header key, bearer token)
	- Flexible field mapping from nested response paths
	- Severity strategies (`fixed`, `mapping`, `threshold`)

**2. Config-Driven Web Sources (`web_sources`)**
- Also declared in `backend/config/sources.yaml`
- Uses Firecrawl + LLM extraction flow (when enabled)
- Intended for non-API pages where structured endpoints are unavailable

---

## 3. Dataset Processing in RiskRadar

For each data source, RiskRadar applies a consistent ingestion pipeline:

1. Fetch raw source payloads on scheduler interval.
2. Normalize each item into a common alert schema.
3. Deduplicate using (`source`, `source_id`).
4. Persist normalized alerts to the database.
5. Expose alerts through API filtering/stats endpoints.
6. Aggregate alerts into AI-generated digest summaries.

---

## 4. Data Characteristics and Constraints

### Geographic Scope
- Current defaults are US-centric and seeded by configured default ZIP/coordinates.
- Some source calls are location-scoped by defaults (for example NWS point resolution).

### Temporal Characteristics
- Data freshness depends on source availability and scraper intervals.
- Scheduler uses per-source intervals with staggered starts to reduce burst load.

### Quality and Reliability Considerations
- Upstream source outages and schema changes can affect ingestion.
- Heterogeneous payload formats are preserved in `raw_data` for traceability.
- Scrape outcomes are logged in `scrape_log` for diagnostics.

---

## 5. Planned Dataset Expansion (CMPS 357 Stages)

As stage work progresses, datasets are expected to expand to support:

- Personalized risk scoring inputs (user sensitivity + contextual environmental factors)
- Interactive map layers and richer geospatial context
- Forecasting features requiring historical feature extraction windows

These additions will build on the same normalized alert pipeline documented above.

