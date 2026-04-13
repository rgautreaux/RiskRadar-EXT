"""On-demand location-based data fetching.

When a user enters a zip code or city name, this module resolves it to
coordinates, fetches fresh alerts from NWS and AirNow, stores them in the DB,
and returns them.
"""

import re
import math
import logging
from datetime import datetime, timedelta, timezone
from typing import Optional

import httpx
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from config.settings import settings
from db.database import get_db
from db.models import Alert
from schemas.alert import AlertOut

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/location", tags=["Location"])


# ── Zip-to-coordinates lookup using a free API ──────────────────────

def _zip_to_coords(zip_code: str) -> tuple[float, float, str, str] | None:
    """Convert zip code to (lat, lon, city, state) using the zippopotam.us API."""
    try:
        resp = httpx.get(f"https://api.zippopotam.us/us/{zip_code}", timeout=10)
        if resp.status_code != 200:
            return None
        data = resp.json()
        place = data["places"][0]
        lat = float(place["latitude"])
        lon = float(place["longitude"])
        city = place["place name"]
        state = place["state abbreviation"]
        return lat, lon, city, state
    except Exception:
        return None


# ── City name geocoding using Nominatim (OpenStreetMap) ──────────────

# US state abbreviation → full name mapping for parsing Nominatim results
_STATE_ABBREVS = {
    "Alabama": "AL", "Alaska": "AK", "Arizona": "AZ", "Arkansas": "AR",
    "California": "CA", "Colorado": "CO", "Connecticut": "CT", "Delaware": "DE",
    "Florida": "FL", "Georgia": "GA", "Hawaii": "HI", "Idaho": "ID",
    "Illinois": "IL", "Indiana": "IN", "Iowa": "IA", "Kansas": "KS",
    "Kentucky": "KY", "Louisiana": "LA", "Maine": "ME", "Maryland": "MD",
    "Massachusetts": "MA", "Michigan": "MI", "Minnesota": "MN",
    "Mississippi": "MS", "Missouri": "MO", "Montana": "MT", "Nebraska": "NE",
    "Nevada": "NV", "New Hampshire": "NH", "New Jersey": "NJ",
    "New Mexico": "NM", "New York": "NY", "North Carolina": "NC",
    "North Dakota": "ND", "Ohio": "OH", "Oklahoma": "OK", "Oregon": "OR",
    "Pennsylvania": "PA", "Rhode Island": "RI", "South Carolina": "SC",
    "South Dakota": "SD", "Tennessee": "TN", "Texas": "TX", "Utah": "UT",
    "Vermont": "VT", "Virginia": "VA", "Washington": "WA",
    "West Virginia": "WV", "Wisconsin": "WI", "Wyoming": "WY",
    "District of Columbia": "DC",
}


def _city_to_coords(query: str) -> tuple[float, float, str, str, str | None] | None:
    """Geocode a city name to (lat, lon, city, state, zip_code) using Nominatim."""
    try:
        resp = httpx.get(
            "https://nominatim.openstreetmap.org/search",
            params={
                "q": query,
                "countrycodes": "us",
                "format": "json",
                "limit": 1,
                "addressdetails": 1,
            },
            headers={"User-Agent": "RiskRadar/1.0 (school-project)"},
            timeout=10,
        )
        if resp.status_code != 200:
            return None
        results = resp.json()
        if not results:
            return None

        hit = results[0]
        lat = float(hit["lat"])
        lon = float(hit["lon"])

        addr = hit.get("address", {})
        city = addr.get("city") or addr.get("town") or addr.get("village") or query.split(",")[0].strip()
        state_full = addr.get("state", "")
        state = _STATE_ABBREVS.get(state_full, state_full[:2].upper() if state_full else "")

        # Extract zip code from address details (Nominatim often includes it)
        zip_code = addr.get("postcode")
        # Nominatim may return extended zip (e.g. "10001:10299"), take the first 5 digits
        if zip_code and len(zip_code) >= 5:
            zip_code = zip_code[:5] if zip_code[:5].isdigit() else None
        else:
            zip_code = None

        return lat, lon, city, state, zip_code
    except Exception:
        logger.exception("City geocoding failed for query: %s", query)
        return None


def _is_zip(q: str) -> bool:
    """Check if a query string looks like a US zip code."""
    return bool(re.match(r"^\d{5}$", q.strip()))


# ── NWS on-demand fetch ──────────────────────────────────────────────

SEVERITY_MAP = {
    "Extreme": "critical",
    "Severe": "high",
    "Moderate": "moderate",
    "Minor": "low",
    "Unknown": "moderate",
}


def _fetch_nws_alerts(lat: float, lon: float, state: str) -> list[dict]:
    """Fetch active NWS weather alerts for a location."""
    url = "https://api.weather.gov/alerts/active"
    headers = {
        "User-Agent": "RiskRadar/1.0 (school-project)",
        "Accept": "application/geo+json",
    }

    # Try point-based first (NWS needs max 4 decimal places)
    resp = httpx.get(url, params={"point": f"{round(lat, 4)},{round(lon, 4)}"}, headers=headers, timeout=30)
    resp.raise_for_status()
    features = resp.json().get("features", [])

    # If none, try state-wide but cap to 25 to avoid flooding for large states
    if not features:
        resp2 = httpx.get(url, params={"area": state}, headers=headers, timeout=30)
        resp2.raise_for_status()
        features = resp2.json().get("features", [])[:25]

    results = []
    for raw in features:
        props = raw.get("properties", {})
        geometry = raw.get("geometry")
        alert_lat, alert_lon = None, None
        if geometry and geometry.get("coordinates"):
            coords = geometry["coordinates"]
            if geometry["type"] == "Polygon":
                ring = coords[0]
                alert_lon = sum(c[0] for c in ring) / len(ring)
                alert_lat = sum(c[1] for c in ring) / len(ring)
            elif geometry["type"] == "Point":
                alert_lon, alert_lat = coords[0], coords[1]

        results.append({
            "source": "nws",
            "source_id": props.get("id", ""),
            "alert_type": "weather",
            "severity": SEVERITY_MAP.get(props.get("severity", "Unknown"), "moderate"),
            "title": props.get("headline", props.get("event", "Weather Alert")),
            "description": props.get("description", ""),
            "latitude": alert_lat,
            "longitude": alert_lon,
            "location_name": props.get("areaDesc", ""),
            "event_start": props.get("onset"),
            "event_end": props.get("expires"),
        })
    return results


# ── AirNow on-demand fetch ───────────────────────────────────────────

def _aqi_to_severity(aqi: int) -> str:
    if aqi <= 50:
        return "low"
    if aqi <= 100:
        return "moderate"
    if aqi <= 200:
        return "high"
    return "critical"


def _fetch_airnow(zip_code: str) -> list[dict]:
    """Fetch current air quality for a zip code from AirNow."""
    api_key = settings.AIRNOW_API_KEY
    if not api_key:
        return []

    url = "https://www.airnowapi.org/aq/observation/zipCode/current/"
    params = {
        "format": "application/json",
        "zipCode": zip_code,
        "distance": 50,
        "API_KEY": api_key,
    }

    try:
        resp = httpx.get(url, params=params, timeout=30)
        resp.raise_for_status()
        raw_items = resp.json()
    except Exception:
        return []

    results = []
    for raw in raw_items:
        aqi = raw.get("AQI", 0)
        param = raw.get("ParameterName", "Unknown")
        date = raw.get("DateObserved", "").strip()
        area = raw.get("ReportingArea", "")
        state = raw.get("StateCode", "")
        category = raw.get("Category", {}).get("Name", "")

        results.append({
            "source": "airnow",
            "source_id": f"{zip_code}_{param}_{date}",
            "alert_type": "air_quality",
            "severity": _aqi_to_severity(aqi),
            "title": f"{param} AQI: {aqi} ({category})",
            "description": f"Air quality in {area}, {state}: {param} AQI is {aqi} ({category}). Observed {date}.",
            "latitude": raw.get("Latitude"),
            "longitude": raw.get("Longitude"),
            "location_name": f"{area}, {state}",
            "event_start": date or None,
            "event_end": None,
        })
    return results


# ── Endpoint ─────────────────────────────────────────────────────────

@router.get("/alerts", response_model=list[AlertOut])
def get_alerts_for_location(
    zip_code: Optional[str] = None,
    lat: Optional[float] = None,
    lon: Optional[float] = None,
    state: Optional[str] = None,
    limit: int = Query(default=50, ge=1, le=200),
    db: Session = Depends(get_db),
):
    """Fetch fresh alerts from NWS and AirNow.
    Accepts either a zip_code OR lat+lon+state coordinates."""
    if zip_code:
        if len(zip_code) != 5 or not zip_code.isdigit():
            raise HTTPException(status_code=400, detail="Invalid zip code")
        location = _zip_to_coords(zip_code)
        if not location:
            raise HTTPException(status_code=404, detail=f"Could not find location for zip code {zip_code}")
        lat, lon, _city, state = location
    elif lat is not None and lon is not None and state:
        pass  # Use provided coordinates directly
    else:
        raise HTTPException(status_code=400, detail="Provide either zip_code or lat+lon+state")

    # Check for cached alerts near these coordinates (within ~50km box)
    ttl = settings.LOCATION_CACHE_TTL_MINUTES
    cutoff = datetime.now(timezone.utc) - timedelta(minutes=ttl)
    cached = (
        db.query(Alert)
        .filter(
            Alert.fetched_at >= cutoff,
            Alert.source.in_(["nws", "airnow"]),
            Alert.latitude.isnot(None),
            Alert.latitude.between(lat - 0.5, lat + 0.5),
            Alert.longitude.between(lon - 0.5, lon + 0.5),
        )
        .order_by(Alert.fetched_at.desc())
        .limit(limit)
        .all()
    )
    if cached:
        return cached

    # No fresh cache — fetch from external APIs
    all_alerts: list[dict] = []
    all_alerts.extend(_fetch_nws_alerts(lat, lon, state))
    if zip_code:
        all_alerts.extend(_fetch_airnow(zip_code))

    # Store in DB (dedup by source + source_id)
    stored = []
    for alert_data in all_alerts:
        existing = (
            db.query(Alert)
            .filter_by(source=alert_data["source"], source_id=alert_data["source_id"])
            .first()
        )
        if existing:
            stored.append(existing)
        else:
            alert = Alert(**alert_data)
            db.add(alert)
            stored.append(alert)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        # Re-fetch all matching alerts in one query instead of per-item lookups
        source_ids = [(d["source"], d["source_id"]) for d in all_alerts]
        stored = (
            db.query(Alert)
            .filter(
                Alert.fetched_at >= cutoff,
                Alert.source.in_(["nws", "airnow"]),
                Alert.latitude.isnot(None),
                Alert.latitude.between(lat - 0.5, lat + 0.5),
                Alert.longitude.between(lon - 0.5, lon + 0.5),
            )
            .order_by(Alert.fetched_at.desc())
            .all()
        )

    # Refresh to get IDs
    for a in stored:
        db.refresh(a)

    return stored[:limit]


@router.get("/search")
def search_location(q: str = Query(..., min_length=2, description="City name or 5-digit zip code")):
    """Unified search: accepts a city name (e.g. 'Houston, TX') or a zip code (e.g. '70506').
    Returns city, state, coordinates, and zip_code (if known)."""
    q = q.strip()

    if _is_zip(q):
        location = _zip_to_coords(q)
        if not location:
            raise HTTPException(status_code=404, detail=f"Could not find location for zip code {q}")
        lat, lon, city, state = location
        return {"city": city, "state": state, "zip_code": q, "latitude": lat, "longitude": lon}

    # City name search
    location = _city_to_coords(q)
    if not location:
        raise HTTPException(status_code=404, detail=f"Could not find location for '{q}'")
    lat, lon, city, state, zip_code = location
    return {"city": city, "state": state, "zip_code": zip_code, "latitude": lat, "longitude": lon}


@router.get("/autocomplete")
def autocomplete_location(q: str = Query(..., min_length=2, description="Partial city name")):
    """Return up to 5 city suggestions for typeahead search."""
    if _is_zip(q):
        # No autocomplete for zip codes
        return []

    try:
        resp = httpx.get(
            "https://nominatim.openstreetmap.org/search",
            params={
                "q": q,
                "countrycodes": "us",
                "format": "json",
                "limit": 5,
                "addressdetails": 1,
            },
            headers={"User-Agent": settings.NWS_USER_AGENT},
            timeout=5,
        )
        if resp.status_code != 200:
            return []

        results = []
        for hit in resp.json():
            addr = hit.get("address", {})
            city = addr.get("city") or addr.get("town") or addr.get("village")
            if not city:
                continue
            state_full = addr.get("state", "")
            state = _STATE_ABBREVS.get(state_full, state_full[:2].upper() if state_full else "")
            label = f"{city}, {state}" if state else city
            # Avoid duplicate labels
            if not any(r["label"] == label for r in results):
                results.append({"label": label, "city": city, "state": state})

        return results
    except Exception:
        return []


@router.get("/info")
def get_location_info(zip_code: str):
    """Return city, state, and coordinates for a zip code."""
    if len(zip_code) != 5 or not zip_code.isdigit():
        raise HTTPException(status_code=400, detail="Invalid zip code")

    location = _zip_to_coords(zip_code)
    if not location:
        raise HTTPException(status_code=404, detail=f"Could not find location for zip code {zip_code}")

    lat, lon, city, state = location
    return {"zip_code": zip_code, "city": city, "state": state, "latitude": lat, "longitude": lon}
