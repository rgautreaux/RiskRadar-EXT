import json
import logging
from collections import defaultdict
from datetime import datetime, timezone
from typing import Any, List, Dict

from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session

from auth.security import decrypt_email, hash_email, normalize_email, password_hash, validate_password_strength
from db.database import get_db
from db.models import User, UserAlertPreference, UserHealthCondition
from backend.schemas.user import UserCreate, UserPrefsUpdate, UserOut
from services.assistant_personality import default_profile_json

router = APIRouter(prefix="/users", tags=["Users"])
LOGGER = logging.getLogger(__name__)
_FALLBACK_COUNTERS: dict[str, int] = defaultdict(int)

# --- Onboarding Tutorial Completion Endpoint ---
@router.post("/{user_id}/onboarding", response_model=UserOut)
def complete_onboarding(user_id: int, completed: bool = Body(..., embed=True), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    setattr(user, 'has_completed_onboarding', completed)
    db.commit()
    db.refresh(user)
    return _serialize_user(user, db)


def _record_fallback(event_name: str, user_id: int):
    _FALLBACK_COUNTERS[event_name] += 1
    LOGGER.info(
        "normalization_fallback event=%s user_id=%s count=%s",
        event_name,
        user_id,
        _FALLBACK_COUNTERS[event_name],
    )


def _normalize_alert_types(values: list[str] | None) -> list[str]:
    if values is None:
        return []

    cleaned: list[str] = []
    for value in values:
        normalized = (value or "").strip().lower()
        if normalized:
            cleaned.append(normalized)

    return list(dict.fromkeys(cleaned))


def _normalize_health_conditions(values: list[str] | None) -> list[str]:
    if values is None:
        return []

    cleaned: list[str] = []
    for value in values:
        normalized = (value or "").strip().lower()
        if normalized:
            cleaned.append(normalized)

    return list(dict.fromkeys(cleaned))



def _parse_alert_types_json(raw_alert_types: str | None) -> List[str]:
    if not raw_alert_types:
        return []

    try:
        parsed = json.loads(raw_alert_types)
    except (json.JSONDecodeError, TypeError):
        return []

    if not isinstance(parsed, list):
        return []

    # type: ignore for mypy/pyright: item type is dynamic from JSON
    return _normalize_alert_types([str(item) for item in parsed])  # type: ignore


def _parse_health_conditions_json(raw_health_conditions: str | None) -> List[str]:
    if not raw_health_conditions:
        return []

    try:
        parsed = json.loads(raw_health_conditions)
    except (json.JSONDecodeError, TypeError):
        return []

    if not isinstance(parsed, list):
        return []

    # type: ignore for mypy/pyright: item type is dynamic from JSON
    return _normalize_health_conditions([str(item) for item in parsed])  # type: ignore


def _sync_user_alert_preferences(db: Session, user: User, alert_types: list[str]):
    db.query(UserAlertPreference).filter(UserAlertPreference.user_id == user.id).delete()
    if not alert_types:
        return

    db.add_all(
        [
            UserAlertPreference(user_id=user.id, alert_type=alert_type)
            for alert_type in alert_types
        ]
    )


def _sync_user_health_conditions(db: Session, user: User, condition_keys: list[str]):
    db.query(UserHealthCondition).filter(UserHealthCondition.user_id == user.id).delete()
    if not condition_keys:
        return

    db.add_all(
        [
            UserHealthCondition(user_id=user.id, condition_key=condition_key)
            for condition_key in condition_keys
        ]
    )


def _serialize_user(user: User, db: Session | None = None) -> UserOut:
    # Use .__dict__ to access actual values, not SQLAlchemy columns
    user_data: Dict[str, Any] = user.__dict__
    alert_types = _parse_alert_types_json(user_data.get('alert_types'))
    if db is not None and not alert_types:
        pref_rows = (
            db.query(UserAlertPreference)
            .filter(UserAlertPreference.user_id == user_data['id'])
            .order_by(UserAlertPreference.alert_type.asc())
            .all()
        )
        alert_types = [row.alert_type for row in pref_rows]
        if alert_types:
            _record_fallback("user.alert_types.relational_fallback", int(user_data['id']))

    health_conditions = _parse_health_conditions_json(user_data.get('health_conditions'))
    if db is not None and not health_conditions:
        condition_rows = (
            db.query(UserHealthCondition)
            .filter(UserHealthCondition.user_id == user_data['id'])
            .order_by(UserHealthCondition.condition_key.asc())
            .all()
        )
        health_conditions = [row.condition_key for row in condition_rows]
        if health_conditions:
            _record_fallback("user.health_conditions.relational_fallback", int(user_data['id']))

    serialized_alert_types = json.dumps(alert_types) if alert_types else user_data.get('alert_types')
    serialized_health_conditions = (
        json.dumps(health_conditions) if health_conditions else user_data.get('health_conditions')
    )

    created_at = user_data.get('created_at') or datetime.now(timezone.utc)
    return UserOut(
        id=user_data['id'],
        display_name=user_data.get('display_name'),
        email=decrypt_email(user_data['email']) if user_data.get('email') else None,
        is_admin=bool(user_data.get('is_admin', False)),
        zip_code=user_data.get('zip_code'),
        latitude=user_data.get('latitude'),
        longitude=user_data.get('longitude'),
        alert_types=serialized_alert_types,
        notify_severity=user_data.get('notify_severity'),
        health_conditions=serialized_health_conditions,
        assistant_style_profile=user_data.get('assistant_style_profile'),
        created_at=created_at,
        has_completed_onboarding=user_data.get('has_completed_onboarding', False),
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

    user = User()
    setattr(user, 'display_name', body.display_name)
    setattr(user, 'email', normalized_email)
    setattr(user, 'email_lookup_hash', hash_email(normalized_email))
    setattr(user, 'password_hash', password_hash(body.password))
    setattr(user, 'is_admin', False)
    setattr(user, 'zip_code', body.zip_code)
    setattr(user, 'alert_types', json.dumps(["all"]))
    setattr(user, 'assistant_style_profile', default_profile_json())
    db.add(user)
    db.flush()
    _sync_user_alert_preferences(db, user, ["all"])
    db.commit()
    db.refresh(user)
    return _serialize_user(user, db)


@router.put("/{user_id}/preferences", response_model=UserOut)
def update_preferences(user_id: int, body: UserPrefsUpdate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    changed_fields: List[str] = []
    if body.zip_code is not None:
        setattr(user, 'zip_code', body.zip_code)
        changed_fields.append('zip_code')
    if body.latitude is not None:
        setattr(user, 'latitude', body.latitude)
        changed_fields.append('latitude')
    if body.longitude is not None:
        setattr(user, 'longitude', body.longitude)
        changed_fields.append('longitude')
    if body.alert_types is not None:
        normalized_alert_types = _normalize_alert_types(body.alert_types)
        setattr(user, 'alert_types', json.dumps(normalized_alert_types))
        setattr(user, 'alert_types', json.dumps(normalized_alert_types))
        _sync_user_alert_preferences(db, user, normalized_alert_types)
        changed_fields.append('alert_types')
    if body.notify_severity is not None:
        setattr(user, 'notify_severity', body.notify_severity)
        changed_fields.append('notify_severity')
    if body.device_token is not None:
        setattr(user, 'device_token', body.device_token)
        changed_fields.append('device_token')
    if body.health_conditions is not None:
        normalized_health_conditions = _normalize_health_conditions(body.health_conditions)
        setattr(user, 'health_conditions', json.dumps(normalized_health_conditions))
        setattr(user, 'health_conditions', json.dumps(normalized_health_conditions))
        _sync_user_health_conditions(db, user, normalized_health_conditions)
        changed_fields.append('health_conditions')
    if body.assistant_style_profile is not None:
        asp = body.assistant_style_profile  # type: ignore
        # type: ignore for type checker on dynamic dict
        logging.getLogger(__name__).info("User %s assistant_style_profile updated: %s", user.id, asp)  # type: ignore
        setattr(user, 'assistant_style_profile', json.dumps(asp))
        changed_fields.append('assistant_style_profile')

    db.commit()
    db.refresh(user)
    return _serialize_user(user, db)
