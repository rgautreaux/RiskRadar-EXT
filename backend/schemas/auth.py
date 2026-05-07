from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, EmailStr

from schemas.user import UserOut


class AuthLoginRequest(BaseModel):
    email: EmailStr
    password: str


class AuthSessionOut(BaseModel):
    session_token: str
    token_type: Literal["bearer"] = "bearer"
    expires_at: str
    user: UserOut

    model_config = ConfigDict(from_attributes=True)
