from pydantic import BaseModel, ConfigDict
from typing import Optional



    # ...existing code...


class UserAdminUpdate(BaseModel):
    is_admin: bool


class UserOut(BaseModel):
    id: int
    display_name: Optional[str] = None
    email: Optional[str] = None
    is_admin: bool = False
    zip_code: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    alert_types: Optional[str] = None
    notify_severity: Optional[str] = None
    health_conditions: Optional[str] = None
    assistant_style_profile: Optional[str] = None
    created_at: str

    has_completed_onboarding: bool = False

    model_config = ConfigDict(from_attributes=True)
