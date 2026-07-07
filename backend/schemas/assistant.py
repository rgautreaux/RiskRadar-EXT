from typing import Literal

from pydantic import BaseModel, Field


class AssistantRequest(BaseModel):
    message: str = Field(min_length=1, max_length=500)
    page_context: str | None = None
    user_id: int | None = None
    location: str | None = None


class AssistantResponse(BaseModel):
    reply: str
    category: Literal["guardrail", "live", "fallback"]
    used_live_data: bool = False
    sources: list[str] = Field(default_factory=list)
