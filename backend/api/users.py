import json
import logging
from collections import defaultdict

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.auth.dependencies import require_self_or_admin
from backend.auth.security import decrypt_email, hash_email, normalize_email, password_hash, validate_password_strength
from backend.db.database import get_db
from backend.db.models import User, UserAlertPreference, UserHealthCondition
from backend.schemas.user import UserCreate, UserPrefsUpdate, UserOut
from backend.services.assistant_personality import default_profile_json

router = APIRouter(prefix="/users", tags=["Users"])
LOGGER = logging.getLogger(__name__)
_FALLBACK_COUNTERS: dict[str, int] = defaultdict(int)


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


def _parse_alert_types_json(raw_alert_types: str | None) -> list[str]:
    if not raw_alert_types:
        return []

    try:
        parsed = json.loads(raw_alert_types)
    except (json.JSONDecodeError, TypeError):
        return []

    if not isinstance(parsed, list):
        return []

    return _normalize_alert_types([str(item) for item in parsed])


def _parse_health_conditions_json(raw_health_conditions: str | None) -> list[str]:
    if not raw_health_conditions:
        return []

    try:
        parsed = json.loads(raw_health_conditions)
    except (json.JSONDecodeError, TypeError):
        return []

    if not isinstance(parsed, list):
        return []

    return _normalize_health_conditions([str(item) for item in parsed])


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
    alert_types = _parse_alert_types_json(user.alert_types)
    if db is not None and not alert_types:
        pref_rows = (
            db.query(UserAlertPreference)
            .filter(UserAlertPreference.user_id == user.id)
            .order_by(UserAlertPreference.alert_type.asc())
            .all()
        )
        alert_types = [row.alert_type for row in pref_rows]
        if alert_types:
            _record_fallback("user.alert_types.relational_fallback", int(user.id))

    health_conditions = _parse_health_conditions_json(user.health_conditions)
    if db is not None and not health_conditions:
        condition_rows = (
            db.query(UserHealthCondition)
            .filter(UserHealthCondition.user_id == user.id)
            .order_by(UserHealthCondition.condition_key.asc())
            .all()
        )
        health_conditions = [row.condition_key for row in condition_rows]
        if health_conditions:
            _record_fallback("user.health_conditions.relational_fallback", int(user.id))

    serialized_alert_types = json.dumps(alert_types) if alert_types else user.alert_types
    serialized_health_conditions = (
        json.dumps(health_conditions) if health_conditions else user.health_conditions
    )

    return UserOut(
        id=user.id,
        display_name=user.display_name,
        email=decrypt_email(user.email) if user.email else None,
        is_admin=bool(user.is_admin),
        zip_code=user.zip_code,
        latitude=user.latitude,
        longitude=user.longitude,
        alert_types=serialized_alert_types,
        notify_severity=user.notify_severity,
        health_conditions=serialized_health_conditions,
        assistant_style_profile=user.assistant_style_profile,
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
        is_admin=False,
        zip_code=body.zip_code,
        alert_types=json.dumps(["all"]),
        assistant_style_profile=default_profile_json(),
    )
    db.add(user)
    db.flush()
    _sync_user_alert_preferences(db, user, ["all"])
    db.commit()
    db.refresh(user)
    return _serialize_user(user, db)


@router.put("/{user_id}/preferences", response_model=UserOut)
def update_preferences(
    user_id: int,
    body: UserPrefsUpdate,
    _current_user: User = Depends(require_self_or_admin),
    db: Session = Depends(get_db),
):
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
        normalized_alert_types = _normalize_alert_types(body.alert_types)
        user.alert_types = json.dumps(normalized_alert_types)
        _sync_user_alert_preferences(db, user, normalized_alert_types)
    if body.notify_severity is not None:
        user.notify_severity = body.notify_severity
    if body.device_token is not None:
        user.device_token = body.device_token
    if body.health_conditions is not None:
        normalized_health_conditions = _normalize_health_conditions(body.health_conditions)
        user.health_conditions = json.dumps(normalized_health_conditions)
        _sync_user_health_conditions(db, user, normalized_health_conditions)
    if body.assistant_style_profile is not None:
        user.assistant_style_profile = json.dumps(body.assistant_style_profile)

    db.commit()
    db.refresh(user)
    return _serialize_user(user, db)
