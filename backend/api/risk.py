from schemas.risk_score import MapRiskOverlayOut, MapRiskZone
from db.models import Alert
from datetime import datetime

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
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from db.database import get_db
from db.models import User
from schemas.risk_score import RiskScoreOut
from scoring import compute_risk_score

router = APIRouter(prefix="/risk", tags=["Risk Scoring"])


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
