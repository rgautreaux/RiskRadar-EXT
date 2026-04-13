from typing import Optional, Literal

from pydantic import BaseModel, ConfigDict, Field


FeedbackReaction = Literal["thumbs_up", "thumbs_down", "smile"]


class FeedbackCreate(BaseModel):
    session_id: str
    message_id: str
    reaction: FeedbackReaction
    rating: int = Field(ge=1, le=5)
    page_context: Optional[str] = None
    response_category: Optional[str] = None
    response_text: Optional[str] = None
    comment: Optional[str] = None


class FeedbackOut(BaseModel):
    id: int
    session_id: str
    message_id: str
    user_id: Optional[int] = None
    reaction: str
    rating: int
    page_context: Optional[str] = None
    response_category: Optional[str] = None
    response_text: Optional[str] = None
    comment: Optional[str] = None
    created_at: str
    updated_at: str

    model_config = ConfigDict(from_attributes=True)