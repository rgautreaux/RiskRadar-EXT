from datetime import datetime, timezone

from sqlalchemy import Column, Integer, Text, Float, Boolean, ForeignKey, UniqueConstraint, event
from sqlalchemy.orm import relationship
from db.database import Base
from auth.security import decrypt_email, encrypt_email, hash_email, is_encrypted_email, normalize_email


def _now():
    return datetime.now(timezone.utc).isoformat()


class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    source = Column(Text, nullable=False)            # 'airnow', 'epa', 'nws', 'firms'
    source_id = Column(Text)                          # dedup key from the API
    alert_type = Column(Text, nullable=False)         # 'air_quality', 'weather', 'wildfire', 'pollution'
    severity = Column(Text, nullable=False, default="moderate")
    title = Column(Text, nullable=False)
    description = Column(Text)
    raw_data = Column(Text)                           # JSON string
    latitude = Column(Float)
    longitude = Column(Float)
    location_name = Column(Text)
    event_start = Column(Text)
    event_end = Column(Text)
    fetched_at = Column(Text, nullable=False, default=_now)
    created_at = Column(Text, nullable=False, default=_now)
    updated_at = Column(Text, nullable=False, default=_now, onupdate=_now)

    __table_args__ = (
        UniqueConstraint("source", "source_id", name="uq_source_alert"),
    )


class Summary(Base):
    __tablename__ = "summaries"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(Text, nullable=False)
    content = Column(Text, nullable=False)            # LLM-generated markdown
    summary_type = Column(Text, nullable=False, default="daily")
    alert_ids = Column(Text)                          # JSON array of alert IDs
    region = Column(Text)
    generated_at = Column(Text, nullable=False, default=_now)
    model_used = Column(Text)
    token_count = Column(Integer)
    created_at = Column(Text, nullable=False, default=_now)

    summary_alert_links = relationship(
        "SummaryAlertLink",
        cascade="all, delete-orphan",
        back_populates="summary",
    )


class SummaryAlertLink(Base):
    __tablename__ = "summary_alerts"

    summary_id = Column(Integer, ForeignKey("summaries.id", ondelete="CASCADE"), primary_key=True)
    alert_id = Column(Integer, ForeignKey("alerts.id", ondelete="CASCADE"), primary_key=True)
    created_at = Column(Text, nullable=False, default=_now)

    summary = relationship("Summary", back_populates="summary_alert_links")
    alert = relationship("Alert")


class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(Text, nullable=False)
    message_id = Column(Text, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    reaction = Column(Text, nullable=False)
    rating = Column(Integer, nullable=False)
    page_context = Column(Text)
    response_category = Column(Text)
    response_text = Column(Text)
    comment = Column(Text)
    created_at = Column(Text, nullable=False, default=_now)
    updated_at = Column(Text, nullable=False, default=_now, onupdate=_now)

    __table_args__ = (
        UniqueConstraint("session_id", "message_id", name="uq_feedback_session_message"),
    )


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    device_token = Column(Text)
    display_name = Column(Text)
    email = Column(Text, nullable=False)
    email_lookup_hash = Column(Text, unique=True, nullable=False)
    password_hash = Column(Text)
    is_admin = Column(Boolean, nullable=False, default=False)
    zip_code = Column(Text)
    latitude = Column(Float)
    longitude = Column(Float)
    alert_types = Column(Text, default='["all"]')     # JSON array
    notify_severity = Column(Text, default="high")
    health_conditions = Column(Text, default='[]')    # JSON array of condition keys
    assistant_style_profile = Column(
        Text,
        default=(
            '{"tone":{"warmth":0.55,"calmness":0.75,"humor":0.4},'
            '"delivery":{"conciseness":0.7,"detail":0.45,"expandability":0.55},'
            '"voice":{"formality":0.35},'
            '"learning":{"feedback_count":0,"last_feedback_at":null}}'
        ),
    )
    created_at = Column(Text, nullable=False, default=_now)
    updated_at = Column(Text, nullable=False, default=_now, onupdate=_now)

    alert_preferences = relationship(
        "UserAlertPreference",
        cascade="all, delete-orphan",
        back_populates="user",
    )
    health_condition_rows = relationship(
        "UserHealthCondition",
        cascade="all, delete-orphan",
        back_populates="user",
    )


class UserAlertPreference(Base):
    __tablename__ = "user_alert_preferences"

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    alert_type = Column(Text, primary_key=True)
    created_at = Column(Text, nullable=False, default=_now)

    user = relationship("User", back_populates="alert_preferences")


class UserHealthCondition(Base):
    __tablename__ = "user_health_conditions"

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    condition_key = Column(Text, primary_key=True)
    created_at = Column(Text, nullable=False, default=_now)

    user = relationship("User", back_populates="health_condition_rows")


def _secure_user_email(target: User):
    if not target.email:
        return

    if is_encrypted_email(target.email):
        plaintext_email = decrypt_email(target.email)
        target.email = encrypt_email(plaintext_email)
        target.email_lookup_hash = target.email_lookup_hash or hash_email(plaintext_email)
        return

    normalized_email = normalize_email(target.email)
    target.email = encrypt_email(normalized_email)
    target.email_lookup_hash = hash_email(normalized_email)


@event.listens_for(User, "before_insert")
def _user_before_insert(_mapper, _connection, target):
    _secure_user_email(target)


@event.listens_for(User, "before_update")
def _user_before_update(_mapper, _connection, target):
    _secure_user_email(target)


class ScrapeLog(Base):
    __tablename__ = "scrape_log"

    id = Column(Integer, primary_key=True, autoincrement=True)
    source = Column(Text, nullable=False)
    status = Column(Text, nullable=False)             # 'success', 'failure', 'partial'
    alerts_fetched = Column(Integer, default=0)
    alerts_new = Column(Integer, default=0)
    error_message = Column(Text)
    duration_ms = Column(Integer)
    started_at = Column(Text, nullable=False)
    completed_at = Column(Text, nullable=False, default=_now)
