

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime
from auth.dependencies import require_account_user
from db.database import get_db
from db.models import Alert, User
from schemas.alert import AlertOut, AlertStats, PrioritizedAlertListOut, MapAlertListOut
from scoring.prioritization import prioritize_alerts as build_prioritized_alerts

router = APIRouter(prefix="/alerts", tags=["Alerts"])

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
    return MapAlertListOut(
        alerts=alerts,
        region=region_val,
        generated_at=datetime.utcnow().isoformat() + "Z",
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
def alert_stats(db: Session = Depends(get_db)):
    total = db.query(func.count(Alert.id)).scalar()
    by_type = dict(db.query(Alert.alert_type, func.count(Alert.id)).group_by(Alert.alert_type).all())
    by_severity = dict(db.query(Alert.severity, func.count(Alert.id)).group_by(Alert.severity).all())
    return AlertStats(total=total or 0, by_type=by_type, by_severity=by_severity)


from auth.dependencies import require_account_user

@router.get("/prioritized/{user_id}", response_model=PrioritizedAlertListOut)
def prioritized_alerts(
    user_id: int,
    radius_km: float = Query(default=150.0, ge=1.0, le=500.0),
    limit: int = Query(default=50, ge=1, le=200),
    _current_user: User = Depends(lambda request=Depends(), db=Depends(get_db), user_id=user_id: require_self_or_admin(user_id, require_account_user(request, db))),
    db: Session = Depends(get_db),
):
    """Return alerts ranked by personalized priority for the given user.

    Combines distance, severity, user health sensitivity, and alert recency
    into a composite priority score (0-100) with deterministic tie-breaking.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return build_prioritized_alerts(user, db, radius_km=radius_km, limit=limit)


@router.get("/{alert_id}", response_model=AlertOut)
def get_alert(alert_id: int, db: Session = Depends(get_db)):
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    return alert
