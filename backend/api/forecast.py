"""7-day weather forecast from the National Weather Service API.

NWS forecast flow:
  1. GET https://api.weather.gov/points/{lat},{lon}  → gives a forecast URL
  2. GET {forecast_url}                               → gives 14 half-day periods
"""

import logging
import time

import httpx
from fastapi import APIRouter, HTTPException, Query

from config.settings import settings
from schemas.forecast import ForecastPeriodOut

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/forecast", tags=["Forecast"])

# Simple in-memory cache: key → (timestamp, data)
_cache: dict[str, tuple[float, list[dict]]] = {}
_CACHE_TTL = 30 * 60  # 30 minutes in seconds


def _cache_key(lat: float, lon: float) -> str:
    return f"{round(lat, 2)},{round(lon, 2)}"


def _fetch_nws_forecast(lat: float, lon: float) -> list[dict]:
    """Fetch 7-day forecast from NWS (two-step API call)."""
    headers = {
        "User-Agent": settings.NWS_USER_AGENT,
        "Accept": "application/geo+json",
    }

    # Step 1: Get the forecast URL from the points endpoint
    # NWS requires max 4 decimal places for coordinates
    point_url = f"https://api.weather.gov/points/{round(lat, 4)},{round(lon, 4)}"
    point_resp = httpx.get(point_url, headers=headers, timeout=15)
    point_resp.raise_for_status()

    forecast_url = point_resp.json().get("properties", {}).get("forecast")
    if not forecast_url:
        raise ValueError("NWS points response missing forecast URL")

    # Step 2: Fetch the actual forecast
    forecast_resp = httpx.get(forecast_url, headers=headers, timeout=15)
    forecast_resp.raise_for_status()

    periods = forecast_resp.json().get("properties", {}).get("periods", [])

    results = []
    for p in periods:
        precip = p.get("probabilityOfPrecipitation", {})
        precip_value = precip.get("value") if isinstance(precip, dict) else None

        results.append({
            "name": p.get("name", ""),
            "temperature": p.get("temperature", 0),
            "temperature_unit": p.get("temperatureUnit", "F"),
            "wind_speed": p.get("windSpeed", ""),
            "wind_direction": p.get("windDirection", ""),
            "short_forecast": p.get("shortForecast", ""),
            "detailed_forecast": p.get("detailedForecast", ""),
            "is_daytime": p.get("isDaytime", True),
            "start_time": p.get("startTime", ""),
            "end_time": p.get("endTime", ""),
            "icon": p.get("icon", ""),
            "precipitation_chance": precip_value,
        })

    return results


@router.get("", response_model=list[ForecastPeriodOut])
def get_forecast(
    lat: float = Query(..., description="Latitude"),
    lon: float = Query(..., description="Longitude"),
):
    """Return the 7-day (14-period) NWS forecast for a location."""
    key = _cache_key(lat, lon)

    # Check cache
    if key in _cache:
        ts, data = _cache[key]
        if time.time() - ts < _CACHE_TTL:
            return data

    try:
        data = _fetch_nws_forecast(lat, lon)
    except httpx.HTTPStatusError as exc:
        logger.error("NWS forecast HTTP error: %s", exc)
        raise HTTPException(status_code=502, detail="NWS API returned an error")
    except Exception as exc:
        logger.exception("NWS forecast fetch failed")
        raise HTTPException(status_code=502, detail="Could not fetch forecast from NWS")

    _cache[key] = (time.time(), data)
    return data
