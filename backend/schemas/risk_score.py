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
