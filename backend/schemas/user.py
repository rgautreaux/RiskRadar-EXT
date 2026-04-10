from pydantic import BaseModel, ConfigDict, EmailStr
from typing import Optional


class UserCreate(BaseModel):
    display_name: str
    email: EmailStr
    password: str
    zip_code: Optional[str] = None


class UserPrefsUpdate(BaseModel):
    zip_code: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    alert_types: Optional[list[str]] = None
    notify_severity: Optional[str] = None
    device_token: Optional[str] = None
    health_conditions: Optional[list[str]] = None


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
    created_at: str

    model_config = ConfigDict(from_attributes=True)
