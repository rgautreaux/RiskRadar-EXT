from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import or_
from sqlalchemy.orm import Session

from db.database import get_db
from db.models import Alert, User
from schemas.assistant import AssistantRequest, AssistantResponse

router = APIRouter(prefix="/assistant", tags=["Assistant"])

GUARDRAIL_KEYWORDS = {
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


def _query_active_alerts(db: Session, location: str | None = None) -> list[Alert]:
    now = datetime.now(timezone.utc)
    window_end = now + timedelta(hours=48)

    query = db.query(Alert).filter(
        or_(Alert.event_start.is_(None), Alert.event_start <= window_end.isoformat()),
        or_(Alert.event_end.is_(None), Alert.event_end >= now.isoformat()),
    )

    if location:
        query = query.filter(Alert.location_name.ilike(f"%{location}%"))

    return query.order_by(Alert.fetched_at.desc()).limit(100).all()


def _risk_level(score: float) -> str:
    if score >= 70:
        return "high"
    if score >= 40:
        return "moderate"
    return "low"


def _severity_weight(severity: str | None) -> float:
    mapping = {
        "critical": 1.0,
        "high": 0.85,
        "moderate": 0.55,
        "low": 0.25,
    }
    return mapping.get((severity or "").lower(), 0.35)


@router.post("/respond", response_model=AssistantResponse)
def respond(body: AssistantRequest, db: Session = Depends(get_db)):
    guardrail_category = _detect_guardrail(body.message)
    if guardrail_category:
        return AssistantResponse(
            reply=_guardrail_reply(guardrail_category),
            category="guardrail",
            used_live_data=False,
            sources=["guardrail-policy"],
        )

    user = None
    if body.user_id is not None:
        user = db.query(User).filter(User.id == body.user_id).first()
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")

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

        weighted = sum(_severity_weight(alert.severity) for alert in alerts)
        score = min(100.0, round((weighted / max(len(alerts), 1)) * 100, 1))
        high = sum(1 for alert in alerts if (alert.severity or "").lower() in {"high", "critical"})
        moderate = sum(1 for alert in alerts if (alert.severity or "").lower() == "moderate")
        low = max(len(alerts) - high - moderate, 0)
        location_label = body.location or "your area"
        return AssistantResponse(
            reply=(
                f"Forecast summary for {location_label}: risk is {_risk_level(score)} ({score}/100). "
                f"Active alerts -> High/Critical: {high}, Moderate: {moderate}, Low: {low}."
            ),
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
        return AssistantResponse(
            reply="Latest alerts:\n" + "\n".join(lines),
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

        weighted = sum(_severity_weight(alert.severity) for alert in alerts)
        score = min(100.0, round((weighted / max(len(alerts), 1)) * 100, 1))
        return AssistantResponse(
            reply=(
                f"Current regional risk is {_risk_level(score)} ({score}/100) based on {len(alerts)} active alerts. "
                "Use the map and forecast pages for location-specific detail."
            ),
            category="live",
            used_live_data=True,
            sources=["alerts"],
        )

    if "help" in message:
        return AssistantResponse(
            reply=(
                "I can help with RiskRadar alerts, forecast summaries, map risk interpretation, and dashboard guidance. "
                "Try asking: 'forecast for Baton Rouge' or 'show latest alerts'."
            ),
            category="fallback",
            used_live_data=False,
            sources=["assistant-help"],
        )

    role_hint = " and your profile preferences" if user else ""
    return AssistantResponse(
        reply=(
            "I can explain RiskRadar data and features. Ask me about alerts, forecast, or map risk, "
            f"and I will use current platform data{role_hint} where available."
        ),
        category="fallback",
        used_live_data=False,
        sources=["assistant-help"],
    )
