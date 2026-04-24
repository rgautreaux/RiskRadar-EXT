import json
import logging
from collections import defaultdict

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db.database import get_db
from db.models import Summary, SummaryAlertLink
from backend.schemas.summary import SummaryAlertIdsOut, SummaryOut

router = APIRouter(prefix="/summaries", tags=["Summaries"])
LOGGER = logging.getLogger(__name__)
_FALLBACK_COUNTERS: dict[str, int] = defaultdict(int)


def _record_fallback(event_name: str, summary_id: int):
    _FALLBACK_COUNTERS[event_name] += 1
    LOGGER.info(
        "normalization_fallback event=%s summary_id=%s count=%s",
        event_name,
        summary_id,
        _FALLBACK_COUNTERS[event_name],
    )


def _parse_alert_ids_json(raw_alert_ids: str | None) -> list[int]:
    if not raw_alert_ids:
        return []

    try:
        parsed = json.loads(raw_alert_ids)
    except (json.JSONDecodeError, TypeError):
        return []

    if not isinstance(parsed, list):
        return []

    normalized: list[int] = []
    for item in parsed:
        if isinstance(item, bool):
            continue
        try:
            value = int(item)
        except (TypeError, ValueError):
            continue
        if value > 0:
            normalized.append(value)
    return list(dict.fromkeys(normalized))


def resolve_summary_alert_ids(summary: Summary, db: Session) -> tuple[list[int], str]:
    linked_ids = [
        int(row[0])
        for row in db.query(SummaryAlertLink.alert_id)
        .filter(SummaryAlertLink.summary_id == summary.id)
        .order_by(SummaryAlertLink.alert_id.asc())
        .all()
    ]
    if linked_ids:
        return linked_ids, "summary_alerts"

    fallback_ids = _parse_alert_ids_json(summary.alert_ids)
    if fallback_ids:
        _record_fallback("summary.alert_ids.json_fallback", int(summary.id))
    return fallback_ids, "summaries.alert_ids"


@router.get("", response_model=list[SummaryOut])
def list_summaries(
    summary_type: str | None = None,
    limit: int = 20,
    db: Session = Depends(get_db),
):
    q = db.query(Summary)
    if summary_type:
        q = q.filter(Summary.summary_type == summary_type)
    return q.order_by(Summary.generated_at.desc()).limit(limit).all()


@router.get("/latest", response_model=SummaryOut | None)
def latest_summary(db: Session = Depends(get_db)):
    return db.query(Summary).order_by(Summary.generated_at.desc()).first()


@router.get("/{summary_id}", response_model=SummaryOut)
def get_summary(summary_id: int, db: Session = Depends(get_db)):
    summary = db.query(Summary).filter(Summary.id == summary_id).first()
    if not summary:
        raise HTTPException(status_code=404, detail="Summary not found")
    return summary


@router.get("/{summary_id}/alert-ids", response_model=SummaryAlertIdsOut)
def get_summary_alert_ids(summary_id: int, db: Session = Depends(get_db)):
    summary = db.query(Summary).filter(Summary.id == summary_id).first()
    if not summary:
        raise HTTPException(status_code=404, detail="Summary not found")

    alert_ids, source = resolve_summary_alert_ids(summary, db)
    return SummaryAlertIdsOut(summary_id=summary.id, alert_ids=alert_ids, source=source)


@router.post("/generate", response_model=SummaryOut)
def generate_summary(db: Session = Depends(get_db)):
    from llm.summarizer import Summarizer

    summarizer = Summarizer()
    summary = summarizer.generate_daily_digest(db)
    if not summary:
        raise HTTPException(status_code=404, detail="No alerts to summarize")
    return summary
