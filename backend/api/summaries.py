from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from config.settings import settings
from db.database import get_db
from db.models import Alert, Summary
from schemas.summary import SummaryOut

router = APIRouter(prefix="/summaries", tags=["Summaries"])


@router.get("", response_model=list[SummaryOut])
def list_summaries(
    summary_type: str | None = None,
    limit: int = Query(default=20, le=200, ge=1),
    db: Session = Depends(get_db),
):
    q = db.query(Summary)
    if summary_type:
        q = q.filter(Summary.summary_type == summary_type)
    return q.order_by(Summary.generated_at.desc()).limit(limit).all()


@router.get("/latest", response_model=SummaryOut | None)
def latest_summary(db: Session = Depends(get_db)):
    return db.query(Summary).order_by(Summary.generated_at.desc()).first()


@router.get("/latest/local", response_model=SummaryOut | None)
def latest_local_summary(
    zip_code: str = Query(..., min_length=5, max_length=5, pattern=r"^\d{5}$"),
    db: Session = Depends(get_db),
):
    return (
        db.query(Summary)
        .filter(
            Summary.summary_type == "local",
            Summary.region.isnot(None),
            Summary.region.endswith(zip_code),
        )
        .order_by(Summary.generated_at.desc())
        .first()
    )


@router.post("/generate", response_model=SummaryOut)
def generate_summary(db: Session = Depends(get_db)):
    from llm.summarizer import Summarizer

    summarizer = Summarizer()
    try:
        summary = summarizer.generate_daily_digest(db)
    except Exception:
        raise HTTPException(status_code=502, detail="Summary generation failed — LLM service may be unavailable")
    if not summary:
        raise HTTPException(status_code=404, detail="No alerts to summarize")
    return summary

@router.post("/generate/local", response_model=SummaryOut)
def generate_local_summary(
    zip_code: str = Query(..., min_length=5, max_length=5, pattern=r"^\d{5}$"),
    db: Session = Depends(get_db),
):
    # Return cached summary if one exists within the TTL
    ttl = settings.LOCATION_CACHE_TTL_MINUTES
    cutoff = datetime.now(timezone.utc) - timedelta(minutes=ttl)
    cached = (
        db.query(Summary)
        .filter(
            Summary.summary_type == "local",
            Summary.region.isnot(None),
            Summary.region.endswith(zip_code),
            Summary.generated_at >= cutoff,
        )
        .order_by(Summary.generated_at.desc())
        .first()
    )
    if cached:
        return cached

    from api.location import _zip_to_coords, _fetch_nws_alerts, _fetch_airnow

    location = _zip_to_coords(zip_code)
    if not location:
        raise HTTPException(status_code=404, detail=f"Could not find location for zip code {zip_code}")

    lat, lon, city, state = location

    # Fetch fresh alerts for this location (graceful on partial failure)
    raw_alerts: list[dict] = []
    try:
        raw_alerts.extend(_fetch_nws_alerts(lat, lon, state))
    except Exception:
        pass  # NWS down — continue with AirNow data
    try:
        raw_alerts.extend(_fetch_airnow(zip_code))
    except Exception:
        pass  # AirNow down — continue with NWS data

    # Store in DB (dedup by source + source_id) and collect alert objects
    local_alerts: list[Alert] = []
    for alert_data in raw_alerts:
        existing = (
            db.query(Alert)
            .filter_by(source=alert_data["source"], source_id=alert_data["source_id"])
            .first()
        )
        if existing:
            local_alerts.append(existing)
        else:
            alert = Alert(**alert_data)
            db.add(alert)
            local_alerts.append(alert)
    db.commit()
    for a in local_alerts:
        db.refresh(a)

    if not local_alerts:
        raise HTTPException(status_code=404, detail=f"No alerts found for {city}, {state} ({zip_code})")

    # Generate a location-specific summary via the LLM
    from llm.summarizer import Summarizer
    summarizer = Summarizer()
    try:
        summary = summarizer.generate_local_digest(db, local_alerts, city, state, zip_code)
    except Exception:
        raise HTTPException(status_code=502, detail="Summary generation failed — LLM service may be unavailable")
    return summary
