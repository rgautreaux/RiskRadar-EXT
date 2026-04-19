"""Shared forecast and risk overlay response models."""

from typing import Any

from pydantic import BaseModel, Field

class MapRiskZone(BaseModel):
    # For simplicity, use centroid and risk info; can extend to full polygon later
    centroid: dict[str, float]  # {"lat": float, "lon": float}
    risk_level: str
    risk_score: float | None = None
    polygon: list[dict[str, float]] | None = None  # Optional: list of {"lat": float, "lon": float}


class ForecastPoint(BaseModel):
    hour_offset: int
    risk_score: float
    risk_level: str
    confidence: float
    alert_count: int
    dominant_type: str | None = None

class MapRiskOverlayOut(BaseModel):
    risk_zones: list[MapRiskZone] = Field(default_factory=list)
    region: str | dict[str, Any]
    generated_at: str
    forecast_hours: int | None = None
    forecast_points: list[ForecastPoint] = Field(default_factory=list)
    # Optional: per-risk-type forecast breakdown, e.g. {"weather": [...], "pollen": [...], ...}
    per_risk_forecasts: dict[str, list[ForecastPoint]] | None = None
    confidence: float | None = None
    trend: str | None = None
    summary: str | None = None
    baseline_risk_score: float | None = None
    personalized: bool = False


class RiskFactor(BaseModel):
    name: str
    value: float
    weight: float
    description: str



class RiskScoreBreakdownOut(BaseModel):
    alert_id: int
    risk_score: float
    risk_level: str
    distance_km: float
    factor_scores: dict[str, float]
    formula: str
    weights: dict[str, float]

class RiskScoreOut(BaseModel):
    user_id: int
    overall_score: float
    risk_level: str
    factors: list[RiskFactor]
    nearby_alert_count: int
    computed_at: str
