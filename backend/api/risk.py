
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import datetime
from db.database import get_db
from db.models import Alert, User
from schemas.risk_score import RiskScoreOut, MapRiskOverlayOut, MapRiskZone
from scoring import compute_risk_score

router = APIRouter(prefix="/risk", tags=["Risk Scoring"])

# Stage 3: Map Risk Overlay Endpoint
@router.get("/map", response_model=MapRiskOverlayOut)
def map_risk_overlay(
    region: str | None = None,
    bbox: str | None = None,
    risk_level: str | None = None,
    db: Session = Depends(get_db),
):
    # For MVP, use alerts as risk proxies; real impl would use grid/polygon risk
    alerts = db.query(Alert).filter(Alert.latitude != None, Alert.longitude != None).all()
    risk_zones = []
    for alert in alerts:
        centroid = {"lat": alert.latitude, "lon": alert.longitude}
        # Dummy risk_level: map severity to risk
        sev = (alert.severity or "").lower()
        if sev in ("high", "critical"): rl = "high"
        elif sev == "moderate": rl = "moderate"
        else: rl = "low"
        risk_zones.append(MapRiskZone(centroid=centroid, risk_level=rl, risk_score=None))
    region_val = region or "all"
    return MapRiskOverlayOut(
        risk_zones=risk_zones,
        region=region_val,
        generated_at=datetime.utcnow().isoformat() + "Z",
    )


# New: Personalized Map Risk Overlay Endpoint
@router.get("/map/personalized/{user_id}", response_model=MapRiskOverlayOut)
def personalized_map_risk_overlay(
    user_id: int,
    region: str | None = None,
    bbox: str | None = None,
    db: Session = Depends(get_db),
):
    """Return a map overlay with user-personalized risk scores for each alert location."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    alerts = db.query(Alert).filter(Alert.latitude != None, Alert.longitude != None).all()
    risk_zones = []
    for alert in alerts:
        centroid = {"lat": alert.latitude, "lon": alert.longitude}
        # Compute personalized risk score for this alert location
        # Temporarily override user location to alert location for scoring
        orig_lat, orig_lon = user.latitude, user.longitude
        user.latitude, user.longitude = alert.latitude, alert.longitude
        risk_score_result = compute_risk_score(user, db)
        user.latitude, user.longitude = orig_lat, orig_lon
        risk_score = risk_score_result["overall_score"]
        risk_level = risk_score_result["risk_level"]
        risk_zones.append(MapRiskZone(centroid=centroid, risk_level=risk_level, risk_score=risk_score))
    region_val = region or "all"
    return MapRiskOverlayOut(
        risk_zones=risk_zones,
        region=region_val,
        generated_at=datetime.utcnow().isoformat() + "Z",
    )


@router.get("/score/{user_id}", response_model=RiskScoreOut)
def get_risk_score(
    user_id: int,
    radius_km: float = Query(default=150.0, ge=1.0, le=500.0),
    db: Session = Depends(get_db),
):
    """Compute a personalized environmental risk score for the user."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return compute_risk_score(user, db, radius_km=radius_km)
