import json

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from auth.security import decrypt_email, hash_email, normalize_email, password_hash, validate_password_strength
from db.database import get_db
from db.models import User
from schemas.user import UserCreate, UserPrefsUpdate, UserOut

router = APIRouter(prefix="/users", tags=["Users"])


def _serialize_user(user: User) -> UserOut:
    return UserOut(
        id=user.id,
        display_name=user.display_name,
        email=decrypt_email(user.email) if user.email else None,
        zip_code=user.zip_code,
        latitude=user.latitude,
        longitude=user.longitude,
        alert_types=user.alert_types,
        notify_severity=user.notify_severity,
        health_conditions=user.health_conditions,
        created_at=user.created_at,
    )


@router.post("/register", response_model=UserOut)
def register_user(body: UserCreate, db: Session = Depends(get_db)):
    normalized_email = normalize_email(str(body.email))
    password_ok, password_error = validate_password_strength(body.password)
    if not password_ok:
        raise HTTPException(status_code=400, detail=password_error)

    existing = db.query(User).filter(User.email_lookup_hash == hash_email(normalized_email)).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    user = User(
        display_name=body.display_name,
        email=normalized_email,
        email_lookup_hash=hash_email(normalized_email),
        password_hash=password_hash(body.password),
        zip_code=body.zip_code,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return _serialize_user(user)


@router.put("/{user_id}/preferences", response_model=UserOut)
def update_preferences(user_id: int, body: UserPrefsUpdate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if body.zip_code is not None:
        user.zip_code = body.zip_code
    if body.latitude is not None:
        user.latitude = body.latitude
    if body.longitude is not None:
        user.longitude = body.longitude
    if body.alert_types is not None:
        user.alert_types = json.dumps(body.alert_types)
    if body.notify_severity is not None:
        user.notify_severity = body.notify_severity
    if body.device_token is not None:
        user.device_token = body.device_token
    if body.health_conditions is not None:
        user.health_conditions = json.dumps(body.health_conditions)

    db.commit()
    db.refresh(user)
    return _serialize_user(user)
