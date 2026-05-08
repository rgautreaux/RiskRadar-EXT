"""SQLAlchemy ORM models for the RiskRadar database."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from sqlalchemy import ForeignKey, Integer, Text, UniqueConstraint, event
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from ..auth.security import decrypt_email, encrypt_email, hash_email, is_encrypted_email, normalize_email


def _now() -> str:
    """Return the current UTC time as an ISO-8601 string."""
    return datetime.now(timezone.utc).isoformat()


class Base(DeclarativeBase):
    """Shared declarative base for all ORM models."""


class Alert(Base):
    """Represents a single environmental or weather alert from an external source."""

    __tablename__ = "alerts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    source: Mapped[str] = mapped_column(Text, nullable=False)            # 'airnow', 'epa', 'nws', 'firms'
    source_id: Mapped[str | None] = mapped_column(Text)                  # dedup key from the API
    alert_type: Mapped[str] = mapped_column(Text, nullable=False)        # 'air_quality', 'weather', 'wildfire', 'pollution'
    severity: Mapped[str] = mapped_column(Text, nullable=False, default="moderate")
    title: Mapped[str] = mapped_column(Text, nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    raw_data: Mapped[str | None] = mapped_column(Text)                   # JSON string
    latitude: Mapped[float | None] = mapped_column()
    longitude: Mapped[float | None] = mapped_column()
    location_name: Mapped[str | None] = mapped_column(Text)
    event_start: Mapped[str | None] = mapped_column(Text)
    event_end: Mapped[str | None] = mapped_column(Text)
    fetched_at: Mapped[str] = mapped_column(Text, nullable=False, default=_now)
    created_at: Mapped[str] = mapped_column(Text, nullable=False, default=_now)
    updated_at: Mapped[str] = mapped_column(Text, nullable=False, default=_now, onupdate=_now)

    __table_args__ = (
        UniqueConstraint("source", "source_id", name="uq_source_alert"),
    )


class Summary(Base):
    """Stores LLM-generated summaries aggregating multiple alerts."""

    __tablename__ = "summaries"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)           # LLM-generated markdown
    summary_type: Mapped[str] = mapped_column(Text, nullable=False, default="daily")
    alert_ids: Mapped[str | None] = mapped_column(Text)                  # JSON array of alert IDs
    region: Mapped[str | None] = mapped_column(Text)
    generated_at: Mapped[str] = mapped_column(Text, nullable=False, default=_now)
    model_used: Mapped[str | None] = mapped_column(Text)
    token_count: Mapped[int | None] = mapped_column(Integer)
    created_at: Mapped[str] = mapped_column(Text, nullable=False, default=_now)

    summary_alert_links: Mapped[list[SummaryAlertLink]] = relationship(
        "SummaryAlertLink",
        cascade="all, delete-orphan",
        back_populates="summary",
    )


class SummaryAlertLink(Base):
    """Join table linking summaries to the alerts they reference."""

    __tablename__ = "summary_alerts"

    summary_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("summaries.id", ondelete="CASCADE"), primary_key=True
    )
    alert_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("alerts.id", ondelete="CASCADE"), primary_key=True
    )
    created_at: Mapped[str] = mapped_column(Text, nullable=False, default=_now)

    summary: Mapped[Summary] = relationship("Summary", back_populates="summary_alert_links")
    alert: Mapped[Alert] = relationship("Alert")


class Feedback(Base):
    """Stores user feedback on assistant responses."""

    __tablename__ = "feedback"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    session_id: Mapped[str] = mapped_column(Text, nullable=False)
    message_id: Mapped[str] = mapped_column(Text, nullable=False)
    user_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    reaction: Mapped[str] = mapped_column(Text, nullable=False)
    rating: Mapped[int] = mapped_column(Integer, nullable=False)
    page_context: Mapped[str | None] = mapped_column(Text)
    response_category: Mapped[str | None] = mapped_column(Text)
    response_text: Mapped[str | None] = mapped_column(Text)
    comment: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[str] = mapped_column(Text, nullable=False, default=_now)
    updated_at: Mapped[str] = mapped_column(Text, nullable=False, default=_now, onupdate=_now)

    __table_args__ = (
        UniqueConstraint("session_id", "message_id", name="uq_feedback_session_message"),
    )


class User(Base):
    """Represents an application user with location, notification, and style preferences."""

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    device_token: Mapped[str | None] = mapped_column(Text)
    display_name: Mapped[str | None] = mapped_column(Text)
    email: Mapped[str] = mapped_column(Text, nullable=False)
    email_lookup_hash: Mapped[str] = mapped_column(Text, unique=True, nullable=False)
    password_hash: Mapped[str | None] = mapped_column(Text)
    is_admin: Mapped[bool] = mapped_column(nullable=False, default=False)
    zip_code: Mapped[str | None] = mapped_column(Text)
    latitude: Mapped[float | None] = mapped_column()
    longitude: Mapped[float | None] = mapped_column()
    alert_types: Mapped[str | None] = mapped_column(Text, nullable=True, default='["all"]')    # JSON array
    notify_severity: Mapped[str] = mapped_column(Text, default="high")
    health_conditions: Mapped[str | None] = mapped_column(Text, nullable=True, default='[]')   # JSON array of condition keys
    assistant_style_profile: Mapped[str] = mapped_column(
        Text,
        default=(
            '{"tone":{"warmth":0.55,"calmness":0.75,"humor":0.4},'
            '"delivery":{"conciseness":0.7,"detail":0.45,"expandability":0.55},'
            '"voice":{"formality":0.35},'
            '"learning":{"feedback_count":0,"last_feedback_at":null}}'
        ),
    )
    created_at: Mapped[str] = mapped_column(Text, nullable=False, default=_now)
    updated_at: Mapped[str] = mapped_column(Text, nullable=False, default=_now, onupdate=_now)

    # Onboarding tutorial completion flag
    has_completed_onboarding: Mapped[bool] = mapped_column(nullable=False, default=False)

    alert_preferences: Mapped[list[UserAlertPreference]] = relationship(
        "UserAlertPreference",
        cascade="all, delete-orphan",
        back_populates="user",
    )
    health_condition_rows: Mapped[list[UserHealthCondition]] = relationship(
        "UserHealthCondition",
        cascade="all, delete-orphan",
        back_populates="user",
    )


class UserAlertPreference(Base):
    """Stores the per-user alert-type subscription preferences."""

    __tablename__ = "user_alert_preferences"

    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )
    alert_type: Mapped[str] = mapped_column(Text, primary_key=True)
    created_at: Mapped[str] = mapped_column(Text, nullable=False, default=_now)

    user: Mapped[User] = relationship("User", back_populates="alert_preferences")


class UserHealthCondition(Base):
    """Stores the per-user health condition keys used for personalised alerts."""

    __tablename__ = "user_health_conditions"

    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )
    condition_key: Mapped[str] = mapped_column(Text, primary_key=True)
    created_at: Mapped[str] = mapped_column(Text, nullable=False, default=_now)

    user: Mapped[User] = relationship("User", back_populates="health_condition_rows")


def _secure_user_email(target: User) -> None:
    """Encrypt the user's email in-place and ensure the lookup hash is set."""
    if not target.email:
        return

    if is_encrypted_email(target.email):
        plaintext_email: str = decrypt_email(target.email)
        target.email = encrypt_email(plaintext_email)
        target.email_lookup_hash = target.email_lookup_hash or hash_email(plaintext_email)
        return

    normalized_email: str = normalize_email(target.email)
    target.email = encrypt_email(normalized_email)
    target.email_lookup_hash = hash_email(normalized_email)


# Explicitly exported so Pylance does not report the event-listener functions
# as unused (the @event.listens_for decorator registers them at import time).
__all__ = [
    "Base",
    "Alert",
    "Summary",
    "SummaryAlertLink",
    "Feedback",
    "User",
    "UserAlertPreference",
    "UserHealthCondition",
    "ScrapeLog",
    "_user_before_insert",
    "_user_before_update",
]


@event.listens_for(User, "before_insert")
def _user_before_insert(_mapper: Any, _connection: Any, target: User) -> None:
    """SQLAlchemy before_insert hook: encrypt email prior to INSERT."""
    _secure_user_email(target)


@event.listens_for(User, "before_update")
def _user_before_update(_mapper: Any, _connection: Any, target: User) -> None:
    """SQLAlchemy before_update hook: re-encrypt email prior to UPDATE."""
    _secure_user_email(target)


class ScrapeLog(Base):
    """Records the outcome of each external data-scraping run."""

    __tablename__ = "scrape_log"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    source: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(Text, nullable=False)            # 'success', 'failure', 'partial'
    alerts_fetched: Mapped[int] = mapped_column(Integer, default=0)
    alerts_new: Mapped[int] = mapped_column(Integer, default=0)
    error_message: Mapped[str | None] = mapped_column(Text)
    duration_ms: Mapped[int | None] = mapped_column(Integer)
    started_at: Mapped[str] = mapped_column(Text, nullable=False)
    completed_at: Mapped[str] = mapped_column(Text, nullable=False, default=_now)