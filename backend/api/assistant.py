import time
from datetime import datetime, timedelta, timezone
from typing import Any, Optional

from auth.dependencies import get_optional_current_user
from db.database import get_db
from db.models import Alert, User
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from services.assistant_personality import (
    Profile,
    apply_style_directive,
    parse_profile,
    parse_style_directive,
    serialize_profile,
    shape_reply,
    style_directive_ack,
)
from backend.schemas.assistant import AssistantRequest, AssistantResponse

router = APIRouter(prefix="/assistant", tags=["Assistant"])

GUARDRAIL_KEYWORDS: dict[str, list[str]] = {
    "medical": ["diagnose", "diagnosis", "prescription", "dosage", "medication", "treatment", "medical advice"],
    "legal": ["legal advice", "lawsuit", "sue", "liability", "lawyer", "attorney", "court"],
    "emergency": ["call 911", "emergency", "evacuate now", "life threatening", "immediate danger"],
    "unsafe": ["hack", "bypass", "exploit", "steal", "weapon", "harm", "violence", "password", "secret key", "token"],
}


def _detect_guardrail(message: str) -> Optional[str]:
    lower = message.lower()
    for category, keywords in GUARDRAIL_KEYWORDS.items():
        if any(keyword in lower for keyword in keywords):
            return category
    return None


def _guardrail_reply(category: str) -> str:
    if category == "emergency":
        return (
            "I cannot provide emergency-response instructions. "
            "If there is immediate danger, contact local emergency services and follow official local alerts."
        )
    if category == "medical":
        return (
            "I can explain RiskRadar environmental data, but I cannot provide medical advice, "
            "diagnosis, or treatment guidance. Please consult a qualified healthcare professional."
        )
    if category == "legal":
        return "I cannot provide legal advice. Please consult a licensed attorney or official legal resources."
    return (
        "I cannot help with harmful, illegal, or credential-related requests. "
        "I can still help interpret RiskRadar alerts, map risk, and forecast data."
    )


def _parse_datetime(value: Optional[str]) -> Optional[datetime]:
    if not value:
        return None
    cleaned = value.strip().replace("Z", "+00:00")
    try:
        parsed = datetime.fromisoformat(cleaned)
    except ValueError:
        return None
    if parsed.tzinfo is None:
        return parsed.replace(tzinfo=timezone.utc)
    return parsed


def _query_active_alerts(db: Session, location: Optional[str] = None) -> list[Alert]:
    now = datetime.now(timezone.utc)
    window_end = now + timedelta(hours=48)

    query = db.query(Alert)
    if location:
        query = query.filter(Alert.location_name.ilike(f"%{location}%"))

    alerts = query.order_by(Alert.fetched_at.desc()).limit(500).all()
    active_alerts: list[Alert] = []

    for alert in alerts:
        raw_start: Any = alert.event_start
        raw_end: Any = alert.event_end
        event_start = _parse_datetime(str(raw_start) if raw_start is not None else None)
        event_end = _parse_datetime(str(raw_end) if raw_end is not None else None)

        if event_start is not None and event_start > window_end:
            continue
        if event_end is not None and event_end < now:
            continue

        active_alerts.append(alert)

    return active_alerts[:100]


def _risk_level(score: float) -> str:
    if score >= 70:
        return "high"
    if score >= 40:
        return "moderate"
    return "low"


def _severity_weight(severity: Optional[str]) -> float:
    mapping: dict[str, float] = {
        "critical": 1.0,
        "high": 0.85,
        "moderate": 0.55,
        "low": 0.25,
    }
    return mapping.get((severity or "").lower(), 0.35)


GUEST_DAILY_LIMIT = 10  # Should match frontend, or make configurable

# Simple in-memory guest rate limit (per IP, per day)
_guest_limit_cache: dict[str, int] = {}


def _guest_limit_key(request: Request) -> str:
    ip = request.client.host if request.client else "unknown"
    today = time.strftime("%Y-%m-%d", time.gmtime())
    return f"{ip}:{today}"


def _increment_guest_limit(request: Request) -> int:
    key = _guest_limit_key(request)
    count = _guest_limit_cache.get(key, 0) + 1
    _guest_limit_cache[key] = count
    return count


def _get_guest_limit(request: Request) -> int:
    key = _guest_limit_key(request)
    return _guest_limit_cache.get(key, 0)


@router.post("/respond", response_model=AssistantResponse, response_model_exclude_unset=True)

from fastapi import Request as FastAPIRequest

def respond(
    body: AssistantRequest,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user),
    request: Optional[FastAPIRequest] = None,
) -> Any:

    # Guest daily limit enforcement
    is_guest = current_user is None
    if is_guest and request is not None:
        if _get_guest_limit(request) >= GUEST_DAILY_LIMIT:
            return AssistantResponse(
                reply=(
                    f"You have reached the daily limit for guest users ({GUEST_DAILY_LIMIT} messages per day). "
                    "Create a free account to unlock unlimited chat and personalized features!"
                ),
                category="fallback",
                used_live_data=False,
                sources=["guest-limit"],
            )
        _increment_guest_limit(request)

    # User-only feature lockout for guests (simple keyword-based)
    personalized_keywords = [
        "my risk", "my score", "my alerts", "my profile", "my preferences", "my account",
        "personalized", "custom alert", "my health", "my recommendations",
    ]
    lower_msg = body.message.lower()
    if is_guest and any(k in lower_msg for k in personalized_keywords):
        return AssistantResponse(
            reply=(
                "This feature is only available to registered users.\n\nWhy register?\n"
                "- Unlock personalized risk scores and recommendations\n"
                "- Set up custom alerts for your area\n"
                "- Save your preferences and health info\n"
                "- Access your profile and account features\n\n"
                "Sign in or create an account for full access!"
            ),
            category="fallback",
            used_live_data=False,
            sources=["guest-lockout"],
        )

    guardrail_category = _detect_guardrail(body.message)
    if guardrail_category:
        return AssistantResponse(
            reply=_guardrail_reply(guardrail_category),
            category="guardrail",
            used_live_data=False,
            sources=["guardrail-policy"],
        )

    user = current_user
    profile: Profile = parse_profile(None)
    if body.user_id is not None:
        if user is None:
            user = db.query(User).filter(User.id == body.user_id).first()
            if user is None:
                raise HTTPException(status_code=404, detail="User not found")
    if user is not None:
        raw_profile: Any = user.assistant_style_profile
        profile = parse_profile(str(raw_profile) if raw_profile is not None else None)

    directive = parse_style_directive(body.message)
    if directive:
        profile = apply_style_directive(profile, directive)
        persisted = user is not None
        if user is not None:
            user.assistant_style_profile = serialize_profile(profile)  # type: ignore[assignment]
            db.commit()
        return AssistantResponse(
            reply=style_directive_ack(directive, persisted=persisted),
            category="fallback",
            used_live_data=False,
            sources=["assistant-preferences"],
        )

    message = body.message.lower()
    alerts = _query_active_alerts(db, body.location)

    if "forecast" in message or "weather" in message:
        if not alerts:
            return AssistantResponse(
                reply=f"No forecast data is currently available{f' for {body.location}' if body.location else ''}.",
                category="live",
                used_live_data=True,
                sources=["alerts"],
            )
        weighted = sum(_severity_weight(getattr(alert, "severity", None)) for alert in alerts)
        score = min(100.0, round((weighted / max(len(alerts), 1)) * 100, 1))
        high = sum(1 for alert in alerts if (alert.severity or "").lower() in {"high", "critical"})
        moderate = sum(1 for alert in alerts if (alert.severity or "").lower() == "moderate")
        low = max(len(alerts) - high - moderate, 0)
        location_label = body.location or "your area"
        reply = (
            f"Forecast summary for {location_label}: risk is {_risk_level(score)} ({score}/100). "
            f"Active alerts -> High/Critical: {high}, Moderate: {moderate}, Low: {low}."
        )
        return AssistantResponse(
            reply=shape_reply(reply, category="live", profile=profile, message=body.message),
            category="live",
            used_live_data=True,
            sources=["alerts", "forecast-baseline"],
        )

    if "alert" in message:
        if not alerts:
            return AssistantResponse(
                reply="There are no active alerts right now.",
                category="live",
                used_live_data=True,
                sources=["alerts"],
            )
        top = alerts[:3]
        lines = [f"- {item.title} ({item.severity})" for item in top]
        reply = "Latest alerts:\n" + "\n".join(lines)
        return AssistantResponse(
            reply=shape_reply(reply, category="live", profile=profile, message=body.message),
            category="live",
            used_live_data=True,
            sources=["alerts"],
        )

    if "risk" in message or "map" in message:
        if not alerts:
            return AssistantResponse(
                reply="No active risk signals are available right now.",
                category="live",
                used_live_data=True,
                sources=["alerts"],
            )
        weighted = sum(_severity_weight(getattr(alert, "severity", None)) for alert in alerts)
        score = min(100.0, round((weighted / max(len(alerts), 1)) * 100, 1))
        reply = (
            f"Current regional risk is {_risk_level(score)} ({score}/100) based on {len(alerts)} active alerts. "
            "Use the map and forecast pages for location-specific detail."
        )
        return AssistantResponse(
            reply=shape_reply(reply, category="live", profile=profile, message=body.message),
            category="live",
            used_live_data=True,
            sources=["alerts"],
        )

    if "help" in message:
        reply = (
            "I can help with RiskRadar alerts, forecast summaries, map risk interpretation, and dashboard guidance. "
            "Try asking: 'forecast for Baton Rouge' or 'show latest alerts'."
        )
        return AssistantResponse(
            reply=shape_reply(reply, category="fallback", profile=profile, message=body.message),
            category="fallback",
            used_live_data=False,
            sources=["assistant-help"],
        )

    role_hint = " and your profile preferences" if user else ""
    reply = (
        "I can explain RiskRadar data and features. Ask me about alerts, forecast, or map risk, "
        f"and I will use current platform data{role_hint} where available."
    )
    return AssistantResponse(
        reply=shape_reply(reply, category="fallback", profile=profile, message=body.message),
        category="fallback",
        used_live_data=False,
        sources=["assistant-help"],
    )