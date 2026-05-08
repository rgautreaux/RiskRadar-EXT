from __future__ import annotations

import logging
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from sqlalchemy.orm import Session

from ..auth.dependencies import get_current_user
from ..auth.security import SESSION_COOKIE_NAME, create_session_token, hash_email, normalize_email, verify_password
from ..db.database import get_db
from ..db.models import User
from ..schemas.auth import AuthLoginRequest, AuthSessionOut
from ..schemas.user import UserOut
from .users import _serialize_user  # type: ignore

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["Auth"])

# Rate limiting: track failed login attempts per IP
_login_failures: dict[str, dict[str, int | datetime]] = {}  # {ip: {count: int, last_attempt: datetime}}
LOGIN_RATE_LIMIT_FAILURES = 10  # Allow 10 failed attempts
LOGIN_RATE_LIMIT_WINDOW = 900  # 15 minute lockout window (seconds)


def _check_login_rate_limit(request: Request) -> None:
    """Check if IP has exceeded login failure threshold."""
    client_ip = request.client.host if request.client else "unknown"
    now = datetime.now(timezone.utc)
    
    if client_ip in _login_failures:
        failure_record = _login_failures[client_ip]
        last_attempt = failure_record.get('last_attempt')  # type: ignore
        if isinstance(last_attempt, datetime):
            time_since_last = (now - last_attempt).total_seconds()
        else:
            time_since_last = 0
        
        # Check if still in lockout window
        count: int = failure_record.get('count', 0)  # type: ignore
        if time_since_last < LOGIN_RATE_LIMIT_WINDOW and count >= LOGIN_RATE_LIMIT_FAILURES:
            logger.warning("Login rate limit exceeded for IP %s", client_ip)
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
    now = datetime.now(timezone.utc)
    
    if client_ip not in _login_failures:
        _login_failures[client_ip] = {'count': 0, 'last_attempt': now}
    
    _login_failures[client_ip]['count'] = _login_failures[client_ip].get('count', 0) + 1  # type: ignore
    _login_failures[client_ip]['last_attempt'] = now
    count = _login_failures[client_ip].get('count', 0)  # type: ignore
    logger.warning("Login failure for IP %s. Attempt %d of %d", client_ip, count, LOGIN_RATE_LIMIT_FAILURES)


def _reset_login_failures(request: Request) -> None:
    """Reset login failures after successful login."""
    client_ip = request.client.host if request.client else "unknown"
    if client_ip in _login_failures:
        del _login_failures[client_ip]
        logger.info("Login successful for IP %s. Rate limit counter reset.", client_ip)


@router.post("/login", response_model=AuthSessionOut)
def login(body: AuthLoginRequest, request: Request, response: Response, db: Session = Depends(get_db)):
    # Rate limit check
    _check_login_rate_limit(request)
    
    normalized_email = normalize_email(str(body.email))
    user = db.query(User).filter(User.email_lookup_hash == hash_email(normalized_email)).first()
    if user is None or not user.password_hash or not verify_password(body.password, user.password_hash):
        _record_login_failure(request)
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
    _reset_login_failures(request)
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
