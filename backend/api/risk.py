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
