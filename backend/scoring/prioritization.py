
# --- Import MAX_RADIUS_KM first to avoid NameError in default args ---
# pylint: disable=pointless-string-statement
from . import MAX_RADIUS_KM

"""
RiskRadar Alert Risk Scoring & Ranking System
------------------------------------------------
This module computes a transparent, user-facing risk/priority score (0-100) for each alert, combining:
    - Distance from user      (35% weight)
    - Alert severity          (30% weight)
    - User health sensitivity (25% weight)
    - Recency / freshness     (10% weight)

Priority levels (urgency thresholds):
    - High:   70-100
    - Medium: 40-69
    - Low:    0-39

Tie-breaking order (deterministic):
    1. Priority score descending
    2. Severity rank descending  (critical > high > moderate > low)
    3. Distance ascending        (closer first)
    4. Fetched-at descending     (newest first)
    5. Alert ID ascending        (stable fallback)

The formula and factor breakdown are exposed for user transparency and explainability.
"""
# ---------------------------------------------------------------------------
# Imports
# ---------------------------------------------------------------------------

from typing import Any, Dict
import json
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from db.models import Alert, User
from schemas.alert import PrioritizedAlertListOut, PrioritizedAlertOut, PriorityFactors
from . import (
    haversine_km,
    CONDITION_ALERT_MAP,
    SEVERITY_SCORES,
)

# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def explain_alert_risk_formula() -> Dict[str, Any]:
    """
    Returns a human-readable explanation of the risk scoring formula and weights.
    """
    return {
        "formula": (
            "Risk Score = 0.35 * DistanceScore + 0.30 * SeverityScore + "
            "0.25 * SensitivityScore + 0.10 * RecencyScore"
        ),
        "weights": {
            "distance": DISTANCE_WEIGHT,
            "severity": SEVERITY_WEIGHT,
            "sensitivity": SENSITIVITY_WEIGHT,
            "recency": RECENCY_WEIGHT,
        },
        "factors": {
            "distance": "How close the alert is to the user (closer = higher risk)",
            "severity": "How severe the alert is (critical > high > moderate > low)",
            "sensitivity": "Whether the alert type matches the user's health conditions",
            "recency": "How recent the alert is (newer = higher risk)",
        },
        "priority_levels": {
            "high": "70-100",
            "medium": "40-69",
            "low": "0-39",
        },
    }

def compute_alert_risk_breakdown(alert: Alert, user: User, radius_km: float = MAX_RADIUS_KM) -> Dict[str, Any] | None:
    """
    Compute a detailed risk score breakdown for a single alert and user.
    Returns a dict with each factor's score, the overall score, and level.
    """
    if (
        user.latitude is None
        or user.longitude is None
        or alert.latitude is None
        or alert.longitude is None
    ):
        return None

    dist = haversine_km(user.latitude, user.longitude, alert.latitude, alert.longitude)
    if dist > radius_km:
        return None

    raw_conditions = user.health_conditions or "[]"
    try:
        user_conditions = json.loads(raw_conditions)
    except (json.JSONDecodeError, TypeError):
        user_conditions = []

    dist_score = _distance_priority(dist, radius_km)
    sev_score = _severity_priority(alert.severity)
    sens_score = _sensitivity_priority(user_conditions, alert.alert_type)
    rec_score = _recency_priority(alert.fetched_at)

    risk_score = round(
        DISTANCE_WEIGHT * dist_score
        + SEVERITY_WEIGHT * sev_score
        + SENSITIVITY_WEIGHT * sens_score
        + RECENCY_WEIGHT * rec_score,
        1,
    )
    risk_score = min(100.0, max(0.0, risk_score))
    risk_level = _level_from_priority(risk_score)

    return {
        "alert_id": alert.id,
        "risk_score": risk_score,
        "risk_level": risk_level,
        "distance_km": round(dist, 2),
        "factor_scores": {
            "distance": round(dist_score, 1),
            "severity": round(sev_score, 1),
            "sensitivity": round(sens_score, 1),
            "recency": round(rec_score, 1),
        },
        "formula": explain_alert_risk_formula()["formula"],
        "weights": explain_alert_risk_formula()["weights"],
    }


# ---------------------------------------------------------------------------
# Weights
# ---------------------------------------------------------------------------

DISTANCE_WEIGHT = 0.35
SEVERITY_WEIGHT = 0.30
SENSITIVITY_WEIGHT = 0.25
RECENCY_WEIGHT = 0.10

# Severity rank for deterministic tie-breaking (higher = more severe)
SEVERITY_RANK = {"critical": 4, "high": 3, "moderate": 2, "low": 1}

# Recency: alerts fetched within this many hours get maximum freshness score
RECENCY_MAX_HOURS = 48.0


# ---------------------------------------------------------------------------
# Per-alert factor calculators
# ---------------------------------------------------------------------------

def _distance_priority(distance_km: float, radius_km: float) -> float:
    """Score 0-100: closer alerts score higher."""
    if distance_km >= radius_km:
        return 0.0
    return max(0.0, 100.0 * (1.0 - distance_km / radius_km))


def _severity_priority(severity: str) -> float:
    """Score 0-100 based on alert severity label."""
    return float(SEVERITY_SCORES.get(severity, 25))


def _sensitivity_priority(user_conditions: list[str], alert_type: str) -> float:
    """Score 0-100 based on whether alert type matches user health conditions.

    Returns 100 if any condition maps to this alert type, 0 otherwise.
    A middle value (50) is returned when the user has conditions but none
    match the specific alert type, giving neutral weighting.
    """
    if not user_conditions:
        return 0.0

    for cond in user_conditions:
        amplified = CONDITION_ALERT_MAP.get(cond, [])
        if alert_type in amplified:
            return 100.0

    # User has conditions, but this alert type doesn't match any
    return 0.0


def _recency_priority(fetched_at: str | None) -> float:
    """Score 0-100: newer alerts score higher.

    Alerts fetched within the last RECENCY_MAX_HOURS get a linearly
    decreasing score from 100 (just now) to 0 (at the threshold).
    """
    if not fetched_at:
        return 0.0

    try:
        fetched_dt = datetime.fromisoformat(fetched_at)
        if fetched_dt.tzinfo is None:
            fetched_dt = fetched_dt.replace(tzinfo=timezone.utc)
    except (ValueError, TypeError):
        return 0.0

    now = datetime.now(timezone.utc)
    age_hours = (now - fetched_dt).total_seconds() / 3600.0

    if age_hours < 0:
        return 100.0
    if age_hours >= RECENCY_MAX_HOURS:
        return 0.0

    return max(0.0, 100.0 * (1.0 - age_hours / RECENCY_MAX_HOURS))


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def prioritize_alerts(
    user: User,
    db: Session,
    radius_km: float = MAX_RADIUS_KM,
    limit: int = 50,
) -> PrioritizedAlertListOut:
    """Return alerts ranked by personalized priority for the given user.

    Returns a PrioritizedAlertListOut with prioritized alert list and metadata.
    """
    user_lat = user.latitude
    user_lon = user.longitude

    if user_lat is None or user_lon is None:
        return PrioritizedAlertListOut(
            user_id=user.id,
            total_nearby=0,
            alerts=[],
            computed_at=datetime.now(timezone.utc).isoformat(),
        )

    # Parse user health conditions
    raw_conditions = user.health_conditions or "[]"
    try:
        user_conditions = json.loads(raw_conditions)
    except (json.JSONDecodeError, TypeError):
        user_conditions = []

    # Fetch all alerts with coordinates
    all_alerts: list[Alert] = (
        db.query(Alert)
        .filter(Alert.latitude.isnot(None), Alert.longitude.isnot(None))
        .all()
    )

    # Score each alert within radius
    scored: list[dict] = []
    for alert in all_alerts:
        dist = haversine_km(user_lat, user_lon, alert.latitude, alert.longitude)
        if dist > radius_km:
            continue

        dist_score = _distance_priority(dist, radius_km)
        sev_score = _severity_priority(alert.severity)
        sens_score = _sensitivity_priority(user_conditions, alert.alert_type)
        rec_score = _recency_priority(alert.fetched_at)

        priority_score = round(
            DISTANCE_WEIGHT * dist_score
            + SEVERITY_WEIGHT * sev_score
            + SENSITIVITY_WEIGHT * sens_score
            + RECENCY_WEIGHT * rec_score,
            1,
        )
        priority_score = min(100.0, max(0.0, priority_score))
        priority_level = _level_from_priority(priority_score)

        scored.append({
            "alert_id": alert.id,
            "source": alert.source,
            "source_id": alert.source_id,
            "alert_type": alert.alert_type,
            "severity": alert.severity,
            "title": alert.title,
            "description": alert.description,
            "latitude": alert.latitude,
            "longitude": alert.longitude,
            "location_name": alert.location_name,
            "event_start": alert.event_start,
            "event_end": alert.event_end,
            "fetched_at": alert.fetched_at,
            "created_at": alert.created_at,
            "priority_score": priority_score,
            "priority_level": priority_level,
            "distance_km": round(dist, 2),
            "priority_factors": {
                "distance": round(dist_score, 1),
                "severity": round(sev_score, 1),
                "sensitivity": round(sens_score, 1),
                "recency": round(rec_score, 1),
            },
        })

    # Deterministic sort using stable multi-pass approach.
    # Python's sort is stable, so we sort by least significant key first.
    # Final order: priority desc, severity rank desc, distance asc,
    # fetched_at desc, alert_id asc
    scored.sort(key=lambda a: a["alert_id"])                       # 5th: id asc
    scored.sort(key=lambda a: a["fetched_at"] or "", reverse=True) # 4th: fetched desc
    scored.sort(key=lambda a: a["distance_km"])                    # 3rd: distance asc
    scored.sort(key=lambda a: -SEVERITY_RANK.get(a["severity"], 0))# 2nd: severity desc
    scored.sort(key=lambda a: -a["priority_score"])                # 1st: priority desc

    # Apply limit
    scored = scored[:limit]

    # Convert scored dicts to PrioritizedAlertOut instances
    alert_outs: list[PrioritizedAlertOut] = []
    for item in scored:
        priority_factors = PriorityFactors(**item["priority_factors"])
        alert_out = PrioritizedAlertOut(
            alert_id=item["alert_id"],
            source=item["source"],
            source_id=item["source_id"],
            alert_type=item["alert_type"],
            severity=item["severity"],
            title=item["title"],
            description=item["description"],
            latitude=item["latitude"],
            longitude=item["longitude"],
            location_name=item["location_name"],
            event_start=item["event_start"],
            event_end=item["event_end"],
            fetched_at=item["fetched_at"],
            created_at=item["created_at"],
            priority_score=item["priority_score"],
            priority_level=item["priority_level"],
            distance_km=item["distance_km"],
            priority_factors=priority_factors,
        )
        alert_outs.append(alert_out)

    return PrioritizedAlertListOut(
        user_id=user.id,
        total_nearby=len(scored),
        alerts=alert_outs,
        computed_at=datetime.now(timezone.utc).isoformat(),
    )


def compute_alert_priority(
    alert: Alert,
    user: User,
    radius_km: float = MAX_RADIUS_KM,
) -> dict | None:
    """Compute priority metadata for a single alert relative to a user.

    Returns None if the alert is outside the user's radius or lacks coordinates.
    """
    if (
        user.latitude is None
        or user.longitude is None
        or alert.latitude is None
        or alert.longitude is None
    ):
        return None

    dist = haversine_km(user.latitude, user.longitude, alert.latitude, alert.longitude)
    if dist > radius_km:
        return None

    raw_conditions = user.health_conditions or "[]"
    try:
        user_conditions = json.loads(raw_conditions)
    except (json.JSONDecodeError, TypeError):
        user_conditions = []

    dist_score = _distance_priority(dist, radius_km)
    sev_score = _severity_priority(alert.severity)
    sens_score = _sensitivity_priority(user_conditions, alert.alert_type)
    rec_score = _recency_priority(alert.fetched_at)

    priority_score = round(
        DISTANCE_WEIGHT * dist_score
        + SEVERITY_WEIGHT * sev_score
        + SENSITIVITY_WEIGHT * sens_score
        + RECENCY_WEIGHT * rec_score,
        1,
    )
    priority_score = min(100.0, max(0.0, priority_score))

    return {
        "priority_score": priority_score,
        "priority_level": _level_from_priority(priority_score),
        "distance_km": round(dist, 2),
        "priority_factors": {
            "distance": round(dist_score, 1),
            "severity": round(sev_score, 1),
            "sensitivity": round(sens_score, 1),
            "recency": round(rec_score, 1),
        },
    }


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _level_from_priority(score: float) -> str:
    if score >= 70:
        return "high"
    if score >= 40:
        return "medium"
    return "low"


def _empty_result(user_id: int) -> dict:
    return {
        "user_id": user_id,
        "total_nearby": 0,
        "alerts": [],
        "computed_at": datetime.now(timezone.utc).isoformat(),
    }
