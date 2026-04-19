from pydantic import BaseModel, ConfigDict, EmailStr
from typing import Optional



class UserOut(BaseModel):
    """
    User profile output schema, including preferences for personalization and risk scoring.
    - alert_types: JSON string of alert types user is interested in
    - notify_severity: Minimum severity for notifications
    - health_conditions: JSON string of user health conditions
    - assistant_style_profile: JSON string for assistant UI personalization
    """
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
