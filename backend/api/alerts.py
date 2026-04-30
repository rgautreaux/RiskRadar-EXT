



from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
 
from datetime import datetime, timezone
from typing import Any
from ..db.database import get_db
from ..db.models import Alert, User
from ..schemas.alert import AlertOut, AlertStats, PrioritizedAlertListOut, MapAlertListOut
from ..scoring.prioritization import (
    prioritize_alerts as build_prioritized_alerts,
    compute_alert_risk_breakdown,
    explain_alert_risk_formula,
)

router = APIRouter(prefix="/alerts", tags=["Alerts"])

# Stage 4: Risk Score Formula Explanation Endpoint
from typing import Any, Dict

@router.get("/risk_formula", response_model=dict)
def get_risk_formula() -> dict[str, Any]:
    """Return a human-readable explanation of the risk scoring formula."""
    return explain_alert_risk_formula()

# Stage 4: Per-Alert Risk Score Breakdown Endpoint
@router.get("/risk_breakdown/{alert_id}/{user_id}", response_model=dict)
def get_alert_risk_breakdown(alert_id: int, user_id: int, db: Session = Depends(get_db)) -> dict[str, Any]:
    """Return a detailed risk score breakdown for a single alert and user."""
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    user = db.query(User).filter(User.id == user_id).first()
    if not alert or not user:
        raise HTTPException(status_code=404, detail="Alert or user not found")
    breakdown = compute_alert_risk_breakdown(alert, user)
    if not breakdown:
        raise HTTPException(status_code=400, detail="Cannot compute risk breakdown (missing location or out of range)")
    return breakdown

# Stage 3: Map Alerts Endpoint
@router.get("/map", response_model=MapAlertListOut)
def map_alerts(
    region: str | None = None,
    bbox: str | None = None,
    alert_type: str | None = None,
    severity: str | None = None,
    db: Session = Depends(get_db),
    # Removed unused argument 'request'
):
    q = db.query(Alert)
    if alert_type:
        q = q.filter(Alert.alert_type == alert_type)
    if severity:
        q = q.filter(Alert.severity == severity)
    # Region filtering (example: filter by location_name or custom logic)
    if region and region.lower() != "all":
        q = q.filter(Alert.location_name.ilike(f"%{region}%"))
    # BBox filtering: bbox="minLon,minLat,maxLon,maxLat"
    if bbox:
        try:
            minlon, minlat, maxlon, maxlat = map(float, bbox.split(","))
            q = q.filter(
                Alert.latitude >= minlat,
                Alert.latitude <= maxlat,
                Alert.longitude >= minlon,
                Alert.longitude <= maxlon,
            )
        except ValueError:
            pass  # Ignore invalid bbox
    alerts = q.order_by(Alert.fetched_at.desc()).limit(500).all()
    region_val = region or "all"
    # Convert Alert to AlertOut for Pydantic validation
    alert_outs = [AlertOut.model_validate(a) for a in alerts]
    return MapAlertListOut(
        alerts=alert_outs,
        region=region_val,
        generated_at=datetime.now(timezone.utc).isoformat(),
    )


@router.get("", response_model=list[AlertOut])
def list_alerts(
    alert_type: str | None = None,
    severity: str | None = None,
    source: str | None = None,
    limit: int = Query(default=50, le=200),
    offset: int = 0,
    db: Session = Depends(get_db),
):
    q = db.query(Alert)
    if alert_type:
        q = q.filter(Alert.alert_type == alert_type)
    if severity:
        q = q.filter(Alert.severity == severity)
    if source:
        q = q.filter(Alert.source == source)
    return q.order_by(Alert.fetched_at.desc()).offset(offset).limit(limit).all()


@router.get("/stats", response_model=AlertStats)
def alert_stats(db: Session = Depends(get_db)) -> AlertStats:
    total = db.query(Alert).count()
    by_type: dict[str, int] = {}
    for alert_type, in db.query(Alert.alert_type).distinct():
        count = db.query(Alert).filter(Alert.alert_type == alert_type).count()
        by_type[str(alert_type)] = int(count)
    by_severity: dict[str, int] = {}
    for severity, in db.query(Alert.severity).distinct():
        count = db.query(Alert).filter(Alert.severity == severity).count()
        by_severity[str(severity)] = int(count)
    return AlertStats(total=total or 0, by_type=by_type, by_severity=by_severity)


@router.get("/prioritized/{user_id}", response_model=PrioritizedAlertListOut)
def prioritized_alerts(
    user_id: int,
    radius_km: float = Query(default=150.0, ge=1.0, le=500.0),
    limit: int = Query(default=50, ge=1, le=200),
    db: Session = Depends(get_db),
) -> PrioritizedAlertListOut:
    """Return alerts ranked by personalized priority for the given user.

    Combines distance, severity, user health sensitivity, and alert recency
    into a composite priority score (0-100) with deterministic tie-breaking.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    result: dict[str, Any] = build_prioritized_alerts(user, db, radius_km=radius_km, limit=limit)
    alerts = result.get("alerts", [])
    # Convert dicts to PrioritizedAlertOut
    from ..schemas.alert import PrioritizedAlertOut, PriorityFactors
    alert_objs = []
    for a in alerts:
        if isinstance(a, dict):
            pf = a.get("priority_factors")
            if pf and not isinstance(pf, PriorityFactors):
                a["priority_factors"] = PriorityFactors(**pf)
            alert_objs.append(PrioritizedAlertOut(**a))
        else:
            alert_objs.append(a)
    return PrioritizedAlertListOut(
        user_id=int(result.get("user_id", user_id)),
        total_nearby=int(result.get("total_nearby", len(alert_objs))),
        alerts=alert_objs,
        computed_at=str(result.get("computed_at", datetime.now(timezone.utc).isoformat())),
    )


@router.get("/{alert_id}", response_model=AlertOut)
def get_alert(alert_id: int, db: Session = Depends(get_db)):
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    return alert
