import json
import logging
import re
from collections import defaultdict
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from db.database import get_db
from db.models import Summary, SummaryAlertLink
from backend.schemas.summary import SummaryAlertIdsOut, SummaryOut

router = APIRouter(prefix="/summaries", tags=["Summaries"])
LOGGER = logging.getLogger(__name__)
_FALLBACK_COUNTERS: dict[str, int] = defaultdict(int)

_SECTION_ALIASES: dict[str, tuple[str, ...]] = {
    "summary_insight": ("daily safety briefing", "executive summary", "summary", "overview"),
    "why_it_matters": ("traveler recommendations", "recommendations", "action items"),
    "key_takeaways": ("top alerts", "traveler recommendations", "key takeaways"),
    "context_notes": ("regional highlights", "context", "regional context"),
}


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
    for item in parsed:  # type: ignore
        if isinstance(item, bool):
            continue
        try:
            value = int(item)
        except (TypeError, ValueError):
            continue
        if value > 0:
            normalized.append(value)
    return list(dict.fromkeys(normalized))


def _parse_markdown_sections(content: str) -> dict[str, list[str]]:
    sections: dict[str, list[str]] = defaultdict(list)
    current_section = ""

    for raw_line in content.splitlines():
        line = raw_line.strip()
        if not line:
            continue

        heading = re.match(r"^#{1,3}\s+(.+)$", line)
        if heading:
            current_section = heading.group(1).strip().lower()
            continue

        if current_section:
            sections[current_section].append(line)

    return sections


def _clean_section_text(lines: list[str]) -> str | None:
    if not lines:
        return None

    cleaned = [line.lstrip("-•*").strip() for line in lines]
    cleaned = [line for line in cleaned if line]
    if not cleaned:
        return None

    return " ".join(cleaned)


def _parse_section_bullets(lines: list[str]) -> list[str]:
    bullets: list[str] = []
    for line in lines:
        candidate = line.lstrip("-•*").strip()
        if candidate:
            bullets.append(candidate)
    return list(dict.fromkeys(bullets))


def enrich_summary(summary: Summary) -> dict[str, Any]:
    content = summary.content or ""
    sections = _parse_markdown_sections(content)

    summary_insight = None
    for section_name in _SECTION_ALIASES["summary_insight"]:
        summary_insight = _clean_section_text(sections.get(section_name, []))
        if summary_insight:
            break

    why_it_matters = None
    for section_name in _SECTION_ALIASES["why_it_matters"]:
        why_it_matters = _clean_section_text(sections.get(section_name, []))
        if why_it_matters:
            break

    key_takeaways: list[str] = []
    for section_name in _SECTION_ALIASES["key_takeaways"]:
        key_takeaways = _parse_section_bullets(sections.get(section_name, []))
        if key_takeaways:
            break

    context_notes = None
    for section_name in _SECTION_ALIASES["context_notes"]:
        context_notes = _clean_section_text(sections.get(section_name, []))
        if context_notes:
            break

    if not summary_insight:
        first_lines = [line for line in content.splitlines() if line.strip() and not line.strip().startswith("#")]
        summary_insight = first_lines[0].strip() if first_lines else None

    if not why_it_matters:
        why_it_matters = context_notes

    if not key_takeaways and sections:
        for candidate_section in ("regional highlights", "summary", "overview"):
            key_takeaways = _parse_section_bullets(sections.get(candidate_section, []))
            if key_takeaways:
                break

    return {
        "id": summary.id,
        "title": summary.title,
        "content": summary.content,
        "summary_type": summary.summary_type,
        "region": summary.region,
        "generated_at": summary.generated_at,
        "model_used": summary.model_used,
        "summary_insight": summary_insight,
        "why_it_matters": why_it_matters,
        "key_takeaways": key_takeaways,
        "context_notes": context_notes,
        "confidence": None,
    }


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


class ZipcodeSummaryRequest(BaseModel):
    zip_code: str
    lat: Optional[float] = None
    lon: Optional[float] = None
    location: Optional[str] = None


@router.get("", response_model=list[SummaryOut])
def list_summaries(
    summary_type: str | None = None,
    zip_code: str | None = None,
    limit: int = 20,
    db: Session = Depends(get_db),
) -> list[dict[str, Any]]:
    q = db.query(Summary)
    if summary_type:
        q = q.filter(Summary.summary_type == summary_type)
    return [enrich_summary(summary) for summary in q.order_by(Summary.generated_at.desc()).limit(limit).all()]


@router.get("/latest", response_model=SummaryOut | None)
def latest_summary(db: Session = Depends(get_db)) -> dict[str, Any] | None:
    summary = db.query(Summary).order_by(Summary.generated_at.desc()).first()
    return enrich_summary(summary) if summary else None


@router.get("/{summary_id}", response_model=SummaryOut)
def get_summary(summary_id: int, db: Session = Depends(get_db)) -> dict[str, Any]:
    summary = db.query(Summary).filter(Summary.id == summary_id).first()
    if not summary:
        raise HTTPException(status_code=404, detail="Summary not found")
    return enrich_summary(summary)


@router.get("/{summary_id}/alert-ids", response_model=SummaryAlertIdsOut)
def get_summary_alert_ids(summary_id: int, db: Session = Depends(get_db)):
    summary = db.query(Summary).filter(Summary.id == summary_id).first()
    if not summary:
        raise HTTPException(status_code=404, detail="Summary not found")

    alert_ids, source = resolve_summary_alert_ids(summary, db)
    return SummaryAlertIdsOut(summary_id=summary.id, alert_ids=alert_ids, source=source)


@router.post("/generate", response_model=SummaryOut)
def generate_summary(db: Session = Depends(get_db)) -> dict[str, Any]:
    from llm.summarizer import Summarizer

    summarizer = Summarizer()
    summary = summarizer.generate_daily_digest(db)
    if not summary:
        raise HTTPException(status_code=404, detail="No alerts to summarize")
    return enrich_summary(summary)
