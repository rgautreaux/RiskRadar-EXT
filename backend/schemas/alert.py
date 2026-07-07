
from pydantic import BaseModel, ConfigDict
from typing import Any, Optional

# Stage 3: Map Alert List Output
class MapAlertListOut(BaseModel):
    alerts: list["AlertOut"]
    region: str | dict[str, Any]
    generated_at: str


class AlertOut(BaseModel):
    id: int
    source: str
    source_id: Optional[str] = None
    alert_type: str
    severity: str
    title: str
    description: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    location_name: Optional[str] = None
    event_start: Optional[str] = None
    event_end: Optional[str] = None
    fetched_at: str
    created_at: str

    model_config = ConfigDict(from_attributes=True)


class AlertStats(BaseModel):
    total: int
    by_type: dict[str, int]
    by_severity: dict[str, int]


class PriorityFactors(BaseModel):
    distance: float
    severity: float
    sensitivity: float
    recency: float


class PrioritizedAlertOut(BaseModel):
    alert_id: int
    source: str
    source_id: Optional[str] = None
    alert_type: str
    severity: str
    title: str
    description: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    location_name: Optional[str] = None
    event_start: Optional[str] = None
    event_end: Optional[str] = None
    fetched_at: Optional[str] = None
    created_at: Optional[str] = None
    priority_score: float
    priority_level: str
    distance_km: float
    priority_factors: PriorityFactors


class PrioritizedAlertListOut(BaseModel):
    user_id: int
    total_nearby: int
    alerts: list[PrioritizedAlertOut]
    computed_at: str
