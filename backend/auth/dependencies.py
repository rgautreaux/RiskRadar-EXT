from __future__ import annotations

from fastapi import Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from auth.security import SESSION_COOKIE_NAME, verify_session_token
from db.database import get_db
from db.models import User


def _extract_session_token(request: Request) -> str | None:
    authorization = request.headers.get("Authorization", "")
    token: str | None = None
    if authorization.lower().startswith("bearer "):
        token = authorization[7:].strip()
        if token:
            return token

    token = request.cookies.get(SESSION_COOKIE_NAME)
    if token:
        return token

    return None


def get_optional_current_user(request: Request, db: Session = Depends(get_db)) -> User | None:
    token = _extract_session_token(request)
    if not token:
        return None

    user_id = verify_session_token(token)
    if user_id is None:
        return None

    return db.query(User).filter(User.id == user_id).first()


def get_current_user(request: Request, db: Session = Depends(get_db)) -> User:
    user = get_optional_current_user(request, db)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication required")

    return user


def require_admin_user(current_user: User = Depends(get_current_user)) -> User:
    if not bool(current_user.is_admin):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required")

    return current_user
