from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, EmailStr


class UserCreate(BaseModel):
    display_name: str
    email: EmailStr
    password: str
    zip_code: str | None = None


class UserPrefsUpdate(BaseModel):
    zip_code: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    alert_types: list[str] | None = None
    notify_severity: str | None = None
    device_token: str | None = None
    health_conditions: list[str] | None = None
    assistant_style_profile: dict[str, Any] | None = None


class UserAdminUpdate(BaseModel):
    is_admin: bool


class UserOut(BaseModel):
    id: int
    display_name: str | None = None
    email: str | None = None
    is_admin: bool = False
    zip_code: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    alert_types: str | None = None
    notify_severity: str | None = None
    health_conditions: str | None = None
    assistant_style_profile: str | None = None
    created_at: datetime | str
    has_completed_onboarding: bool = False

    model_config = ConfigDict(from_attributes=True)
