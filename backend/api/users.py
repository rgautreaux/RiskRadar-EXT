import json

from fastapi import APIRouter, Depends, HTTPException
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from db.database import get_db
from db.models import User
from schemas.user import UserCreate, UserPrefsUpdate, UserOut

router = APIRouter(prefix="/users", tags=["Users"])

_pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")


@router.post("/register", response_model=UserOut)
def register_user(body: UserCreate, db: Session = Depends(get_db)):
    normalized_email = body.email.lower()
    existing = db.query(User).filter(User.email == normalized_email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    user = User(
        display_name=body.display_name,
        email=normalized_email,
        password_hash=_pwd_context.hash(body.password),
        zip_code=body.zip_code,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


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
    return user
