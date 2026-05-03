from __future__ import annotations

import logging
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from sqlalchemy.orm import Session

from auth.dependencies import get_current_user
from auth.security import SESSION_COOKIE_NAME, create_session_token, hash_email, normalize_email, verify_password
from db.database import get_db
from db.models import User
from backend.schemas.auth import AuthLoginRequest, AuthSessionOut
from backend.schemas.user import UserOut
from backend.api.users import _serialize_user

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["Auth"])

# Rate limiting: track failed login attempts per IP
_login_failures: dict[str, dict] = {}  # {ip: {count: int, last_attempt: datetime}}
LOGIN_RATE_LIMIT_FAILURES = 10  # Allow 10 failed attempts
LOGIN_RATE_LIMIT_WINDOW = 900  # 15 minute lockout window (seconds)


def _check_login_rate_limit(request: Request) -> None:
    """Check if IP has exceeded login failure threshold."""
    client_ip = request.client.host if request.client else "unknown"
    now = datetime.utcnow()
    
    if client_ip in _login_failures:
        failure_record = _login_failures[client_ip]
        time_since_last = (now - failure_record['last_attempt']).total_seconds()
        
        # Check if still in lockout window
        if time_since_last < LOGIN_RATE_LIMIT_WINDOW and failure_record['count'] >= LOGIN_RATE_LIMIT_FAILURES:
            logger.warning(f"Login rate limit exceeded for IP {client_ip}")
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Account temporarily locked due to too many login failures. Try again in 15 minutes."
            )
        
        # Reset count if outside window
        if time_since_last >= LOGIN_RATE_LIMIT_WINDOW:
            _login_failures[client_ip] = {'count': 0, 'last_attempt': now}


def _record_login_failure(request: Request) -> None:
    """Record a failed login attempt."""
    client_ip = request.client.host if request.client else "unknown"
    now = datetime.utcnow()
    
    if client_ip not in _login_failures:
        _login_failures[client_ip] = {'count': 0, 'last_attempt': now}
    
    _login_failures[client_ip]['count'] += 1
    _login_failures[client_ip]['last_attempt'] = now
    logger.warning(f"Login failure for IP {client_ip}. Attempt {_login_failures[client_ip]['count']} of {LOGIN_RATE_LIMIT_FAILURES}")


def _reset_login_failures(request: Request) -> None:
    """Reset login failures after successful login."""
    client_ip = request.client.host if request.client else "unknown"
    if client_ip in _login_failures:
        del _login_failures[client_ip]
        logger.info(f"Login successful for IP {client_ip}. Rate limit counter reset.")


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
