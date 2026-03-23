
# Stage 3: Map risk overlay endpoint
from schemas.risk_score import MapRiskOverlayOut, MapRiskZoneOut
from datetime import datetime

@router.get("/map", response_model=MapRiskOverlayOut)
def map_risk_overlay(
    region: str | None = None,
    bbox: str | None = None,
    risk_level: str | None = None,
    db: Session = Depends(get_db),
):
    # Dummy implementation: return a few hardcoded risk zones (replace with real logic)
    risk_zones = [
        MapRiskZoneOut(
            centroid={"lat": 34.05, "lon": -118.25},
            risk_level="high",
            risk_score=85.0,
            metadata={"label": "Downtown LA"},
        ),
        MapRiskZoneOut(
            centroid={"lat": 34.15, "lon": -118.15},
            risk_level="moderate",
            risk_score=60.0,
            metadata={"label": "Pasadena"},
        ),
        MapRiskZoneOut(
            centroid={"lat": 33.94, "lon": -118.40},
            risk_level="low",
            risk_score=30.0,
            metadata={"label": "LAX"},
        ),
    ]
    return MapRiskOverlayOut(
        risk_zones=risk_zones,
        region=region,
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
