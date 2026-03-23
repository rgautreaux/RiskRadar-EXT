
# For map overlays (Stage 3)
from typing import Optional

class MapRiskZoneOut(BaseModel):
    # geo-polygon or grid cell, here simplified as centroid and risk info
    centroid: dict  # {"lat": float, "lon": float}
    risk_level: str
    risk_score: float
    metadata: Optional[dict] = None

class MapRiskOverlayOut(BaseModel):
    risk_zones: list[MapRiskZoneOut]
    region: Optional[str] = None  # or geo-bounds string/structure
    generated_at: str
from pydantic import BaseModel


class RiskFactor(BaseModel):
    name: str
    value: float
    weight: float
    description: str


class RiskScoreOut(BaseModel):
    user_id: int
    overall_score: float
    risk_level: str
    factors: list[RiskFactor]
    nearby_alert_count: int
    computed_at: str
