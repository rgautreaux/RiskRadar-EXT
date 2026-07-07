from pydantic import BaseModel, Field
from typing import Optional


class SummaryOut(BaseModel):
    id: int
    title: str
    content: str
    summary_type: str
    region: Optional[str] = None
    generated_at: str
    model_used: Optional[str] = None
    summary_insight: Optional[str] = None
    why_it_matters: Optional[str] = None
    key_takeaways: list[str] = Field(default_factory=list)
    context_notes: Optional[str] = None
    confidence: Optional[float] = None

    model_config = {"from_attributes": True, "protected_namespaces": ()}


class SummaryAlertIdsOut(BaseModel):
    summary_id: int
    alert_ids: list[int]
    source: str
