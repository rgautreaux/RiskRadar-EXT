"""NOAA National Weather Service — active weather alerts.

API docs: https://www.weather.gov/documentation/services-web-api
No API key required, but a User-Agent header is mandatory.
"""

import json
import httpx

from config.settings import settings
from scrapers.base_scraper import BaseScraper

SEVERITY_MAP = {
    "Extreme": "critical",
    "Severe": "high",
    "Moderate": "moderate",
    "Minor": "low",
    "Unknown": "moderate",
}


class NWSScraper(BaseScraper):
    source_name = "nws"
    alert_type = "weather"

    def fetch_raw_data(self) -> list[dict]:
        url = "https://api.weather.gov/alerts/active"
        headers = {"User-Agent": settings.NWS_USER_AGENT, "Accept": "application/geo+json"}

        # Query all active alerts nationwide (status=actual, message_type=alert)
        params = {"status": "actual", "message_type": "alert"}
        resp = httpx.get(url, params=params, headers=headers, timeout=30)
        resp.raise_for_status()
        return resp.json().get("features", [])

    def normalize(self, raw: dict) -> dict:
        props = raw.get("properties", {})
        geometry = raw.get("geometry")

        lat, lon = None, None
        if geometry and geometry.get("coordinates"):
            coords = geometry["coordinates"]
            # GeoJSON polygon — take centroid of first ring
            if geometry["type"] == "Polygon":
                ring = coords[0]
                lon = sum(c[0] for c in ring) / len(ring)
                lat = sum(c[1] for c in ring) / len(ring)
            elif geometry["type"] == "MultiPolygon":
                all_coords = [
                    coord
                    for polygon in coords
                    for ring in polygon
                    for coord in ring
                ]
                if all_coords:
                    lon = sum(c[0] for c in all_coords) / len(all_coords)
                    lat = sum(c[1] for c in all_coords) / len(all_coords)
            elif geometry["type"] == "Point":
                lon, lat = coords[0], coords[1]

        return {
            "source": self.source_name,
            "source_id": props.get("id", ""),
            "alert_type": self.alert_type,
            "severity": SEVERITY_MAP.get(props.get("severity", "Unknown"), "moderate"),
            "title": props.get("headline", props.get("event", "Weather Alert")),
            "description": props.get("description", ""),
            "raw_data": json.dumps(props),
            "latitude": lat,
            "longitude": lon,
            "location_name": props.get("areaDesc", ""),
            "event_start": props.get("onset"),
            "event_end": props.get("expires"),
        }
