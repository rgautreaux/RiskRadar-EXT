"""Trip packing guide endpoint — generates LLM-powered packing recommendations."""

import logging
from datetime import date, datetime, timedelta, timezone
from typing import Optional

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from auth.dependencies import get_optional_current_user
from db.database import get_db
from db.models import Alert, User

router = APIRouter(prefix="/packing", tags=["Packing"])
logger = logging.getLogger(__name__)


class PackingGuideRequest(BaseModel):
    city: str
    state: str
    zip_code: str
    trip_date: Optional[str] = None  # ISO date string; defaults to today


class PackingGuideResponse(BaseModel):
    guide: str
    city: str
    state: str
    zip_code: str
    trip_date: str
    alert_count: int
    model_used: str
    is_personalized: bool


def _parse_datetime(value: str | None) -> datetime | None:
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


def _query_location_alerts(db: Session, city: str, state: str) -> list[Alert]:
    """Return active alerts matching the destination city or state."""
    now = datetime.now(timezone.utc)
    window_end = now + timedelta(hours=72)

    candidates = (
        db.query(Alert)
        .filter(
            Alert.location_name.ilike(f"%{city}%")
            | Alert.location_name.ilike(f"%{state}%")
        )
        .order_by(Alert.fetched_at.desc())
        .limit(200)
        .all()
    )

    active: list[Alert] = []
    for alert in candidates:
        event_start = _parse_datetime(alert.event_start)
        event_end = _parse_datetime(alert.event_end)
        if event_start is not None and event_start > window_end:
            continue
        if event_end is not None and event_end < now:
            continue
        active.append(alert)

    return active[:50]


@router.post("/guide", response_model=PackingGuideResponse)
def get_packing_guide(
    body: PackingGuideRequest,
    db: Session = Depends(get_db),
    current_user: User | None = Depends(get_optional_current_user),
):
    """
    Generate a trip packing guide for a destination.

    Authenticated users receive a more capable model response (premium tier);
    guests are served by the standard guest model.
    """
    from llm.summarizer import Summarizer

    trip_date = body.trip_date or date.today().isoformat()
    is_premium = current_user is not None

    alerts = _query_location_alerts(db, body.city, body.state)

    summarizer = Summarizer()
    guide, model_used = summarizer.generate_trip_packing_guide(
        city=body.city,
        state=body.state,
        zip_code=body.zip_code,
        alerts=alerts,
        trip_date=trip_date,
        is_premium=is_premium,
    )

    return PackingGuideResponse(
        guide=guide,
        city=body.city,
        state=body.state,
        zip_code=body.zip_code,
        trip_date=trip_date,
        alert_count=len(alerts),
        model_used=model_used,
        is_personalized=is_premium,
    )
