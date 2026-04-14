from __future__ import annotations
from fastapi import Depends, HTTPException, Request, status
from sqlalchemy.orm import Session
from backend.auth.security import SESSION_COOKIE_NAME, verify_session_token
from backend.db.database import get_db
from backend.db.models import User


def require_account_owner_or_admin(user_id: int, request: Request, db: Session = Depends(get_db)) -> User:
    # First, check if the target user exists
    target_user = db.query(User).filter(User.id == user_id).first()
    if not target_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    user = require_account_user(request, db)
    # SQLAlchemy boolean columns require .is_(True) for correct evaluation
    if user.id != user_id and not (getattr(user, "is_admin", False) is True or getattr(user, "is_admin", False) == True or (hasattr(user, "is_admin") and getattr(user, "is_admin").__class__.__name__ == 'InstrumentedAttribute' and getattr(user, "is_admin").is_(True))):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    return user



def _extract_session_token(request: Request) -> str | None:
    authorization = request.headers.get("Authorization", "")
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


# New: Require account (non-guest) user for restricted features
def require_account_user(request: Request, db: Session = Depends(get_db)) -> User:
    user = get_optional_current_user(request, db)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication required")
    # Guest users are marked by a special flag or property; adjust as needed
    if getattr(user, "is_guest", False):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Account required for this feature")
    return user


def require_admin_user(current_user: User = Depends(get_current_user)) -> User:
    if not (getattr(current_user, "is_admin", False) is True or getattr(current_user, "is_admin", False) == True or (hasattr(current_user, "is_admin") and getattr(current_user, "is_admin").__class__.__name__ == 'InstrumentedAttribute' and getattr(current_user, "is_admin").is_(True))):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required")

    return current_user


def require_self_or_admin(user_id: int, current_user: User = Depends(get_current_user)) -> User:
    """Allow access only to the account owner or an admin user."""
    if current_user.id != user_id and not (getattr(current_user, "is_admin", False) is True or getattr(current_user, "is_admin", False) == True or (hasattr(current_user, "is_admin") and getattr(current_user, "is_admin").__class__.__name__ == 'InstrumentedAttribute' and getattr(current_user, "is_admin").is_(True))):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")

    return current_user
