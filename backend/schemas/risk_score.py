# Stage 3: Map Risk Overlay Output
from typing import Any
from pydantic import BaseModel

class MapRiskZone(BaseModel):
    # For simplicity, use centroid and risk info; can extend to full polygon later
    centroid: dict[str, float]  # {"lat": float, "lon": float}
    risk_level: str
    risk_score: float | None = None
    # Optionally: polygon: list[dict[str, float]]

class MapRiskOverlayOut(BaseModel):
    risk_zones: list[MapRiskZone]
    region: str | dict[str, Any]
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
