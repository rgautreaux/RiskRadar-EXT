from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from sqlalchemy.orm import Session

from auth.dependencies import get_current_user
from auth.security import SESSION_COOKIE_NAME, create_session_token, hash_email, normalize_email, verify_password
from db.database import get_db
from db.models import User
from schemas.auth import AuthLoginRequest, AuthSessionOut
from schemas.user import UserOut
from api.users import _serialize_user

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login", response_model=AuthSessionOut)
def login(body: AuthLoginRequest, request: Request, response: Response, db: Session = Depends(get_db)):
    normalized_email = normalize_email(str(body.email))
    user = db.query(User).filter(User.email_lookup_hash == hash_email(normalized_email)).first()
    if user is None or not user.password_hash or not verify_password(body.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")

    session_token, expires_at = create_session_token(user.id)
    response.set_cookie(
        key=SESSION_COOKIE_NAME,
        value=session_token,
        httponly=True,
        secure=request.url.scheme == "https",
        samesite="lax",
        path="/",
        expires=int(expires_at.timestamp()),
    )
    return AuthSessionOut(
        session_token=session_token,
        expires_at=expires_at.isoformat(),
        user=_serialize_user(user),
    )


@router.post("/logout")
def logout(response: Response):
    response.delete_cookie(key=SESSION_COOKIE_NAME, path="/")
    return {"ok": True}


@router.get("/me", response_model=UserOut)
def read_current_user(current_user: User = Depends(get_current_user)):
    return _serialize_user(current_user)
