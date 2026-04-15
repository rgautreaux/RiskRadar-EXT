"""LLM summarizer — generates daily digests and breaking alert summaries."""

import json
import logging
from datetime import date, datetime, timedelta, timezone

import openai
from sqlalchemy.orm import Session

from config.settings import settings
from db.models import Alert, Summary, SummaryAlertLink
from llm.prompts import (
    BREAKING_SYSTEM,
    BREAKING_USER,
    DAILY_DIGEST_SYSTEM,
    DAILY_DIGEST_USER,
    TRIP_PACKING_SYSTEM,
    TRIP_PACKING_USER,
)

logger = logging.getLogger(__name__)


class Summarizer:
    def _build_fallback_summary(self, alerts_count: int, scope: str) -> str:
        """Return a deterministic summary when the LLM provider is unavailable."""
        return (
            f"## {scope} Summary (Fallback)\n"
            "The language model is temporarily unavailable, so this summary was generated "
            "from structured alert metadata.\n\n"
            f"- Alerts analyzed: {alerts_count}\n"
            "- Next step: retry generation once LLM connectivity is restored."
        )

    def _resolve_model(self, is_premium: bool = False) -> str:
        """Return the LLM model name for the given user tier."""
        default_model = settings.LLM_MODEL.strip() or "gpt-4o-mini"
        guest_model = settings.LLM_MODEL_GUEST.strip() or default_model
        premium_model = settings.LLM_MODEL_PREMIUM.strip() or default_model

        if is_premium:
            return premium_model
        return guest_model

    def _call_llm(self, system: str, user: str, is_premium: bool = False) -> tuple[str, int, str]:
        """Call the configured LLM provider. Returns (text, token_count, model_used)."""
        api_key = settings.OPENROUTER_API_KEY.strip() or settings.LLM_API_KEY.strip()

        if api_key:
            model = self._resolve_model(is_premium)
            client = openai.OpenAI(
                    base_url="https://openrouter.ai/api/v1",
                    api_key=api_key,
                )

            completion = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": user},
                ],
            )

            text = completion.choices[0].message.content
            tokens = completion.usage.total_tokens if completion.usage else 0
            return text, tokens, model
        else:
            raise ValueError("No LLM API key configured")

    def generate_daily_digest(self, db: Session, since_hours: int = 24) -> Summary | None:
        cutoff = (datetime.now(timezone.utc) - timedelta(hours=since_hours)).isoformat()
        alerts = db.query(Alert).filter(Alert.fetched_at >= cutoff).all()

        if not alerts:
            return None

        alerts_data = [
            {
                "type": a.alert_type,
                "severity": a.severity,
                "title": a.title,
                "description": (a.description or "")[:500],
                "location": a.location_name,
                "time": a.event_start,
            }
            for a in alerts
        ]

        user_msg = DAILY_DIGEST_USER.format(
            count=len(alerts),
            date=date.today().strftime("%B %d, %Y"),
            alerts_json=json.dumps(alerts_data, indent=2),
        )

        text, tokens, model = self._call_llm(DAILY_DIGEST_SYSTEM, user_msg)

        summary = Summary(
            title=f"Environmental Digest — {date.today().strftime('%b %d, %Y')}",
            content=text,
            summary_type="daily",
            alert_ids=json.dumps([a.id for a in alerts]),
            region="US",
            model_used=model,
            token_count=tokens,
        )
        db.add(summary)
        db.flush()
        db.add_all(
            [
                SummaryAlertLink(summary_id=summary.id, alert_id=alert.id)
                for alert in alerts
            ]
        )
        db.commit()
        db.refresh(summary)
        logger.info("Daily digest generated: %s alerts, %s tokens", len(alerts), tokens)
        return summary

    def generate_breaking_summary(self, alert: Alert) -> str:
        """Short summary for push notifications."""
        alert_data = {
            "type": alert.alert_type,
            "title": alert.title,
            "description": (alert.description or "")[:300],
            "location": alert.location_name,
            "severity": alert.severity,
        }
        user_msg = BREAKING_USER.format(alert_json=json.dumps(alert_data))
        text, _, _ = self._call_llm(BREAKING_SYSTEM, user_msg)
        return text

    def generate_trip_packing_guide(
        self,
        city: str,
        state: str,
        zip_code: str,
        alerts: list[Alert],
        trip_date: str,
        is_premium: bool = False,
    ) -> tuple[str, str]:
        """Generate a trip packing guide for a destination. Returns (guide_markdown, model_used)."""
        alerts_data = [
            {
                "type": a.alert_type,
                "severity": a.severity,
                "title": a.title,
                "description": (a.description or "")[:500],
                "location": a.location_name,
                "time": a.event_start,
            }
            for a in alerts
        ]

        user_msg = TRIP_PACKING_USER.format(
            date=trip_date,
            city=city,
            state=state,
            zip_code=zip_code,
            count=len(alerts_data),
            alerts_json=json.dumps(alerts_data, indent=2),
        )

        try:
            text, _, model = self._call_llm(TRIP_PACKING_SYSTEM, user_msg, is_premium=is_premium)
            return text, model
        except Exception as exc:
            logger.warning("LLM unavailable for trip packing guide: %s", exc)
            return self._build_fallback_summary(len(alerts_data), f"{city}, {state}"), "fallback"
