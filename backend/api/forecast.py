from collections import Counter
from datetime import datetime, timedelta, timezone
from math import atan2, cos, radians, sin, sqrt
from typing import Optional

import json
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from db.database import get_db
from db.models import Alert, User
from schemas.risk_score import ForecastPoint, MapRiskOverlayOut, MapRiskZone
from services.risk_scoring import RiskFactors, UserSensitivities, compute_risk_score

router = APIRouter(prefix="/forecast", tags=["Forecast"])
FORECAST_STEP_HOURS = 6

SEVERITY_SCORES = {
    "critical": 1.0,
    "high": 0.85,
    "moderate": 0.55,
    "low": 0.25,
}

TYPE_WEIGHTS = {
    "air_quality": 1.0,
    "weather": 0.82,
    "wildfire": 0.95,
    "pollution": 0.78,
    "fire": 0.95,
    "flood": 0.8,
    "earthquake": 0.65,
}


def _clamp(value: float, minimum: float, maximum: float) -> float:
    return max(minimum, min(maximum, value))


def _parse_datetime(value: Optional[str]) -> Optional[datetime]:
    if not value:
        return None

    if isinstance(value, datetime):
        # Defensive: Only call replace if value is a datetime instance
        try:
            if value.tzinfo is None:
                return datetime(
                    value.year, value.month, value.day,
                    value.hour, value.minute, value.second, value.microsecond,
                    tzinfo=timezone.utc
                )
            return value
        except Exception:
            return value

    cleaned = value.strip().replace("Z", "+00:00")
    try:
        parsed = datetime.fromisoformat(cleaned)
    except ValueError:
        return None

    if parsed.tzinfo is None:
        return parsed.replace(tzinfo=timezone.utc)
    return parsed


def _severity_score(alert: Alert) -> float:
    return SEVERITY_SCORES.get((alert.severity or "").lower(), 0.4)


def _type_weight(alert: Alert) -> float:
    return TYPE_WEIGHTS.get(_alert_type_key(alert), 0.8)


def _alert_type_key(alert: Alert) -> str:
    alert_type = (alert.alert_type or "").lower()
    if "air" in alert_type:
        return "air_quality"
    if "wild" in alert_type or "fire" in alert_type:
        return "wildfire"
    if "pollut" in alert_type:
        return "pollution"
    if "flood" in alert_type:
        return "flood"
    if "earth" in alert_type:
        return "earthquake"
    return "weather"


def _distance_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    radius_km = 6371.0
    d_lat = radians(lat2 - lat1)
    d_lon = radians(lon2 - lon1)
    a = sin(d_lat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(d_lon / 2) ** 2
    return 2 * radius_km * atan2(sqrt(a), sqrt(1 - a))


def _distance_factor(alert: Alert, lat: Optional[float], lon: Optional[float]) -> float:
    alert_lat = getattr(alert, "latitude", None)
    alert_lon = getattr(alert, "longitude", None)
    if lat is None or lon is None or alert_lat is None or alert_lon is None:
        return 0.78

    distance = _distance_km(lat, lon, float(alert_lat), float(alert_lon))
    return _clamp(1.0 / (1.0 + distance / 140.0), 0.2, 1.0)


def _recency_factor(alert: Alert, now: datetime) -> float:
    fetched_at = _parse_datetime(getattr(alert, "fetched_at", None))
    if not fetched_at:
        return 0.85

    age_hours = max((now - fetched_at).total_seconds() / 3600.0, 0.0)
    return _clamp(1.0 / (1.0 + age_hours / 72.0), 0.35, 1.0)


def _build_sensitivities(user: Optional[User]) -> UserSensitivities:
    if not user:
        return UserSensitivities()

    health = []
    raw_health = getattr(user, "health_conditions", None)
    if raw_health:
        try:
            health = [str(item).lower() for item in json.loads(raw_health)]
        except (TypeError, json.JSONDecodeError):
            health = []

    return UserSensitivities(
        air_quality=5 if "asthma" in health or "respiratory" in health else 0,
        weather=3 if "arthritis" in health else 0,
        wildfire=4 if "respiratory" in health else 0,
        pollution=5 if "heart" in health else 0,
    )


def _build_risk_factors(alerts: list[Alert]) -> RiskFactors:
    if not alerts:
        return RiskFactors()

    counts = Counter(_alert_type_key(alert) for alert in alerts)
    total = float(len(alerts))
    return RiskFactors(
        air_quality=counts.get("air_quality", 0) / total,
        weather=counts.get("weather", 0) / total,
        wildfire=counts.get("wildfire", 0) / total,
        pollution=counts.get("pollution", 0) / total,
    )


def _query_alerts(
    db: Session,
    lat: Optional[float],
    lon: Optional[float],
    location: Optional[str],
    hours: int,
) -> list[Alert]:
    now = datetime.now(timezone.utc)
    window_end = now + timedelta(hours=hours)
    latitude_column = getattr(Alert, "latitude")
    longitude_column = getattr(Alert, "longitude")
    location_name_column = getattr(Alert, "location_name")

    q = db.query(Alert)

    if lat is not None and lon is not None:
        lat_min, lat_max = lat - 1.0, lat + 1.0
        lon_min, lon_max = lon - 1.0, lon + 1.0
        q = q.filter(
            latitude_column >= lat_min,
            latitude_column <= lat_max,
            longitude_column >= lon_min,
            longitude_column <= lon_max,
        )
    elif location:
        q = q.filter(location_name_column.ilike(f"%{location}%"))

    alerts = q.order_by(Alert.fetched_at.desc()).all()
    active_alerts: list[Alert] = []

    for alert in alerts:
        event_start = _parse_datetime(getattr(alert, "event_start", None))
        event_end = _parse_datetime(getattr(alert, "event_end", None))

        if event_start is not None and event_start > window_end:
            continue
        if event_end is not None and event_end < now:
            continue

        active_alerts.append(alert)

    return active_alerts


def _forecast_points(base_score: float, alerts: list[Alert], hours: int) -> list[ForecastPoint]:
    step = FORECAST_STEP_HOURS if hours >= FORECAST_STEP_HOURS else hours
    steps = list(range(0, hours + 1, step))
    if steps[-1] != hours:
        steps.append(hours)

    type_counts = Counter(_alert_type_key(alert) for alert in alerts)
    dominant_type = type_counts.most_common(1)[0][0].replace("_", " ") if type_counts else None
    results: list[ForecastPoint] = []

    for hour_offset in steps:
        time_decay = _clamp(1.0 - (hour_offset / max(hours, 1)) * 0.45, 0.42, 1.0)
        alert_pressure = min(len(alerts) * 1.8, 14.0)
        adjusted_score = _clamp(base_score * time_decay + alert_pressure * (1.0 - time_decay), 0.0, 100.0)
        confidence = _clamp(0.9 - (hour_offset / max(hours, 1)) * 0.28 + min(len(alerts), 8) * 0.01, 0.35, 0.95)
        risk_level = "high" if adjusted_score >= 70 else "moderate" if adjusted_score >= 40 else "low"

        results.append(
            ForecastPoint(
                hour_offset=hour_offset,
                risk_score=round(adjusted_score, 2),
                risk_level=risk_level,
                confidence=round(confidence, 2),
                alert_count=len(alerts),
                dominant_type=dominant_type,
            )
        )

    return results


def _build_response(
    *,
    alerts: list[Alert],
    lat: Optional[float],
    lon: Optional[float],
    location: Optional[str],
    hours: int,
    user: Optional[User] = None,
    detailed: bool = False
) -> MapRiskOverlayOut:
    now = datetime.now(timezone.utc)
    sensitivities = _build_sensitivities(user)
    base_factors = _build_risk_factors(alerts)
    score_result = compute_risk_score(base_factors, sensitivities)
    base_score = score_result.score if alerts else 12.0
    points = _forecast_points(base_score, alerts, hours)

    first_score = points[0].risk_score if points else base_score
    last_score = points[-1].risk_score if points else base_score
    if last_score - first_score > 5:
        trend = "increasing"
    elif first_score - last_score > 5:
        trend = "decreasing"
    else:
        trend = "steady"

    risk_zones: list[MapRiskZone] = []
    for alert in alerts:
        alert_lat = getattr(alert, "latitude", None)
        alert_lon = getattr(alert, "longitude", None)
        centroid = {
            "lat": float(alert_lat) if alert_lat is not None else 0.0,
            "lon": float(alert_lon) if alert_lon is not None else 0.0,
        }
        zone_score = _clamp(
            base_score * _severity_score(alert) * _type_weight(alert) * _distance_factor(alert, lat, lon) * _recency_factor(alert, now),
            0.0,
            100.0,
        )
        zone = MapRiskZone(
            centroid=centroid,
            risk_level="high" if zone_score >= 70 else "moderate" if zone_score >= 40 else "low",
            risk_score=round(zone_score, 2),
        )
        risk_zones.append(zone)

    if alerts:
        top_type = Counter(_alert_type_key(alert) for alert in alerts).most_common(1)[0][0].replace("_", " ")
        summary = (
            f"{len(alerts)} active alerts in {location or 'the selected region'} suggest {score_result.level} risk "
            f"with {top_type} driving the outlook."
        )
    else:
        summary = f"No active alerts were found for {location or 'the selected region'}. Forecast remains low and stable."

    region_value = location or (f"{lat},{lon}" if lat is not None and lon is not None else "all")

    # Per-risk forecast breakdown (optional)
    per_risk_forecasts: dict[str, list[ForecastPoint]] = {}
    for risk_type in ["weather", "air_quality", "wildfire", "flood", "earthquake", "pollen", "pollution"]:
        risk_alerts = [a for a in alerts if _alert_type_key(a) == risk_type]
        if risk_alerts:
            per_risk_forecasts[risk_type] = _forecast_points(base_score, risk_alerts, hours)
    return MapRiskOverlayOut(
        risk_zones=risk_zones,
        region=region_value,
        generated_at=now.isoformat(),
        forecast_hours=hours,
        forecast_points=points,
        confidence=round(points[0].confidence if points else 0.45, 2),
        trend=trend,
        summary=summary,
        baseline_risk_score=round(base_score, 2),
        personalized=user is not None,
        per_risk_forecasts=per_risk_forecasts if detailed and per_risk_forecasts else None,
    )



@router.get("/personalized/{user_id}", response_model=MapRiskOverlayOut)
def get_personalized_forecast(
    user_id: int,
    lat: Optional[float] = Query(None, description="Latitude for location-based forecast"),
    lon: Optional[float] = Query(None, description="Longitude for location-based forecast"),
    location: Optional[str] = Query(None, description="Location string (ZIP or City, State)"),
    hours: int = Query(48, ge=1, le=72, description="Forecast window in hours (default 48)"),
    detailed: bool = Query(False, description="Include per-risk forecast breakdown"),
    db: Session = Depends(get_db),
):
    """Returns a personalized risk forecast for the next 24-48 hours for a given user and location."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    alerts = _query_alerts(db, lat, lon, location, hours)
    return _build_response(alerts=alerts, lat=lat, lon=lon, location=location, hours=hours, user=user, detailed=detailed)



@router.get("", response_model=MapRiskOverlayOut)
def get_forecast(
    lat: Optional[float] = Query(None, description="Latitude for location-based forecast"),
    lon: Optional[float] = Query(None, description="Longitude for location-based forecast"),
    location: Optional[str] = Query(None, description="Location string (ZIP or City, State)"),
    hours: int = Query(48, ge=1, le=72, description="Forecast window in hours (default 48)"),
    detailed: bool = Query(False, description="Include per-risk forecast breakdown"),
    db: Session = Depends(get_db),
):
    """Returns a risk forecast for the next 24-48 hours for a given location."""
    alerts = _query_alerts(db, lat, lon, location, hours)
    return _build_response(alerts=alerts, lat=lat, lon=lon, location=location, hours=hours, detailed=detailed)
