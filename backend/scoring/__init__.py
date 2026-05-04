"""Personal Risk Scoring Engine for RiskRadar.

Computes a personalized environmental risk score (0-100) based on:
  - Proximity to nearby alerts (40% weight)
  - Severity of nearby alerts (30% weight)
  - User health sensitivity match (20% weight)
  - Alert density near user (10% weight)

Risk levels:
  - Low:      0-25
  - Moderate: 26-50
  - High:     51-75
  - Critical: 76-100
"""

import json
import math
from datetime import datetime, timezone

from sqlalchemy.orm import Session

from db.models import Alert, User
from schemas.risk_score import RiskScoreOut, RiskFactor

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

PROXIMITY_WEIGHT = 0.40
SEVERITY_WEIGHT = 0.30
SENSITIVITY_WEIGHT = 0.20
DENSITY_WEIGHT = 0.10

# Maximum radius (km) for alerts to be considered "nearby"
MAX_RADIUS_KM = 150.0

# Severity scores (normalized 0-100)
SEVERITY_SCORES = {
    "critical": 100,
    "high": 75,
    "moderate": 50,
    "low": 25,
}

# Maps health conditions to the alert types they amplify
CONDITION_ALERT_MAP = {
    "respiratory": ["air_quality", "wildfire"],
    "cardiovascular": ["air_quality", "weather"],
    "allergies": ["air_quality"],
    "immune_compromised": ["air_quality", "pollution", "weather"],
    "mobility_limited": ["weather", "earthquake", "wildfire"],
}

# Alert density thresholds — number of alerts within radius that maps to score
DENSITY_THRESHOLDS = [
    (20, 100),
    (10, 75),
    (5, 50),
    (2, 25),
    (0, 0),
]


# ---------------------------------------------------------------------------
# Geo helpers
# ---------------------------------------------------------------------------

def haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Great-circle distance between two points in kilometres."""
    r = 6371.0  # Earth radius in km
    d_lat = math.radians(lat2 - lat1)
    d_lon = math.radians(lon2 - lon1)
    a = (
        math.sin(d_lat / 2) ** 2
        + math.cos(math.radians(lat1))
        * math.cos(math.radians(lat2))
        * math.sin(d_lon / 2) ** 2
    )
    return r * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


# ---------------------------------------------------------------------------
# Factor calculators
# ---------------------------------------------------------------------------

def _proximity_score(distances_km: list[float]) -> float:
    """Score 0-100 based on how close the nearest alerts are.

    Closer alerts produce a higher score.  The closest alert dominates,
    but additional close alerts contribute through an average blend.
    """
    if not distances_km:
        return 0.0

    # Score each alert: 100 at 0 km, 0 at MAX_RADIUS_KM
    scores = [max(0.0, 100.0 * (1.0 - d / MAX_RADIUS_KM)) for d in distances_km]
    # Blend: 60 % from closest alert, 40 % from average of top-5
    top = sorted(scores, reverse=True)[:5]
    best = top[0]
    avg_top = sum(top) / len(top)
    return min(100.0, 0.6 * best + 0.4 * avg_top)


def _severity_score(alerts: list[Alert]) -> float:
    """Weighted severity of nearby alerts (highest dominates)."""
    if not alerts:
        return 0.0

    scores = [SEVERITY_SCORES.get(a.severity, 25) for a in alerts]
    top = sorted(scores, reverse=True)[:5]
    best = top[0]
    avg_top = sum(top) / len(top)
    return min(100.0, 0.6 * best + 0.4 * avg_top)


def _sensitivity_score(
    user_conditions: list[str],
    alert_types: list[str],
) -> float:
    """Score based on overlap between user health conditions and alert types."""
    if not user_conditions:
        return 0.0

    matched = 0
    total_possible = 0
    for cond in user_conditions:
        amplified_types = CONDITION_ALERT_MAP.get(cond, [])
        if not amplified_types:
            continue
        total_possible += len(amplified_types)
        for at in amplified_types:
            if at in alert_types:
                matched += 1

    if total_possible == 0:
        return 0.0
    return min(100.0, (matched / total_possible) * 100.0)


def _density_score(count: int) -> float:
    """Score based on how many alerts are nearby."""
    for threshold, score in DENSITY_THRESHOLDS:
        if count >= threshold:
            return float(score)
    return 0.0


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def compute_risk_score(
    user: User,
    db: Session,
    radius_km: float = MAX_RADIUS_KM,
) -> RiskScoreOut:
    """Compute a personalized risk score for the given user.

    Returns a RiskScoreOut Pydantic model.
    """
    user_lat = user.latitude
    user_lon = user.longitude
    if user_lat is None or user_lon is None:
        return _zero_score(user.id, reason="User location not set")

    # Fetch all alerts that have coordinates
    all_alerts: list[Alert] = (
        db.query(Alert)
        .filter(Alert.latitude.isnot(None), Alert.longitude.isnot(None))
        .all()
    )

    # Filter to nearby alerts
    nearby: list[tuple[Alert, float]] = []
    for alert in all_alerts:
        dist = haversine_km(user_lat, user_lon, alert.latitude, alert.longitude)
        if dist <= radius_km:
            nearby.append((alert, dist))

    nearby_alerts = [a for a, _ in nearby]
    distances = [d for _, d in nearby]

    # Parse user health conditions
    raw_conditions = user.health_conditions or "[]"
    try:
        user_conditions = json.loads(raw_conditions)
    except (json.JSONDecodeError, TypeError):
        user_conditions = []

    nearby_alert_types = list({a.alert_type for a in nearby_alerts})

    # Calculate individual factors
    prox = _proximity_score(distances)
    sev = _severity_score(nearby_alerts)
    sens = _sensitivity_score(user_conditions, nearby_alert_types)
    dens = _density_score(len(nearby_alerts))

    overall = (
        PROXIMITY_WEIGHT * prox
        + SEVERITY_WEIGHT * sev
        + SENSITIVITY_WEIGHT * sens
        + DENSITY_WEIGHT * dens
    )
    overall = round(min(100.0, max(0.0, overall)), 1)

    risk_level = _level_from_score(overall)

    factors = [
        RiskFactor(
            name="proximity",
            value=round(prox, 1),
            weight=PROXIMITY_WEIGHT,
            description=f"Based on distance to {len(nearby_alerts)} nearby alert(s)",
        ),
        RiskFactor(
            name="severity",
            value=round(sev, 1),
            weight=SEVERITY_WEIGHT,
            description="Weighted severity of nearby alerts",
        ),
        RiskFactor(
            name="health_sensitivity",
            value=round(sens, 1),
            weight=SENSITIVITY_WEIGHT,
            description=f"Match between conditions {user_conditions} and alert types {nearby_alert_types}",
        ),
        RiskFactor(
            name="alert_density",
            value=round(dens, 1),
            weight=DENSITY_WEIGHT,
            description=f"{len(nearby_alerts)} alert(s) within {radius_km} km",
        ),
    ]

    result_model = RiskScoreOut(
        user_id=user.id,
        overall_score=overall,
        risk_level=risk_level,
        factors=factors,
        nearby_alert_count=len(nearby_alerts),
        computed_at=datetime.now(timezone.utc).isoformat(),
    )
    return result_model.model_dump()


def _level_from_score(score: float) -> str:
    if score >= 76:
        return "critical"
    if score >= 51:
        return "high"
    if score >= 26:
        return "moderate"
    return "low"


def _zero_score(user_id: int, reason: str = "") -> RiskScoreOut:
    factors = [
        RiskFactor(
            name="proximity",
            value=0.0,
            weight=PROXIMITY_WEIGHT,
            description=reason or "No data available",
        ),
        RiskFactor(
            name="severity",
            value=0.0,
            weight=SEVERITY_WEIGHT,
            description=reason or "No data available",
        ),
        RiskFactor(
            name="health_sensitivity",
            value=0.0,
            weight=SENSITIVITY_WEIGHT,
            description=reason or "No data available",
        ),
        RiskFactor(
            name="alert_density",
            value=0.0,
            weight=DENSITY_WEIGHT,
            description=reason or "No data available",
        ),
    ]
    result_model = RiskScoreOut(
        user_id=user_id,
        overall_score=0.0,
        risk_level="low",
        factors=factors,
        nearby_alert_count=0,
        computed_at=datetime.now(timezone.utc).isoformat(),
    )
    return result_model.model_dump()
