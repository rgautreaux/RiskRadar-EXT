"""Tests for database models."""

import json
import pytest
from sqlalchemy import inspect
from sqlalchemy.exc import IntegrityError

from auth.security import decrypt_email, hash_email, password_hash, verify_password
from db.models import Alert, Summary, SummaryAlertLink, User, UserAlertPreference, ScrapeLog
from scripts.backfill_summary_alert_links import backfill_summary_alert_links
from scripts.backfill_user_alert_preferences import backfill_user_alert_preferences
from tests.conftest import NOW


class TestAlertModel:
    def test_create_alert(self, db_session):
        alert = Alert(
            source="test", source_id="t_001", alert_type="weather",
            severity="high", title="Test Alert",
            fetched_at=NOW, created_at=NOW, updated_at=NOW,
        )
        db_session.add(alert)
        db_session.commit()
        assert alert.id is not None
        assert alert.source == "test"

    def test_unique_constraint_source_source_id(self, db_session):
        a1 = Alert(
            source="test", source_id="dup_001", alert_type="weather",
            severity="high", title="Alert 1",
            fetched_at=NOW, created_at=NOW, updated_at=NOW,
        )
        a2 = Alert(
            source="test", source_id="dup_001", alert_type="weather",
            severity="low", title="Alert 2",
            fetched_at=NOW, created_at=NOW, updated_at=NOW,
        )
        db_session.add(a1)
        db_session.commit()
        db_session.add(a2)
        with pytest.raises(IntegrityError):
            db_session.commit()

    def test_optional_fields_nullable(self, db_session):
        alert = Alert(
            source="test", source_id="t_002", alert_type="weather",
            severity="low", title="Minimal Alert",
            fetched_at=NOW, created_at=NOW, updated_at=NOW,
        )
        db_session.add(alert)
        db_session.commit()
        assert alert.description is None
        assert alert.latitude is None
        assert alert.longitude is None


class TestSummaryModel:
    def test_create_summary(self, db_session):
        summary = Summary(
            title="Daily Digest", content="Summary text.",
            summary_type="daily", alert_ids="[1,2]",
            generated_at=NOW, created_at=NOW,
        )
        db_session.add(summary)
        db_session.commit()
        assert summary.id is not None
        assert summary.summary_type == "daily"

    def test_alert_ids_stored_as_json(self, db_session):
        ids = [1, 2, 3]
        summary = Summary(
            title="Test", content="Content",
            summary_type="daily", alert_ids=json.dumps(ids),
            generated_at=NOW, created_at=NOW,
        )
        db_session.add(summary)
        db_session.commit()
        assert json.loads(summary.alert_ids) == ids

    def test_generate_summary_creates_junction_rows(self, db_session, sample_alerts):
        from unittest.mock import patch
        from llm.summarizer import Summarizer

        with patch.object(Summarizer, "_call_llm", return_value=("## Digest\nBody", 42)):
            summary = Summarizer().generate_daily_digest(db_session)

        assert summary is not None
        links = (
            db_session.query(SummaryAlertLink)
            .filter(SummaryAlertLink.summary_id == summary.id)
            .all()
        )
        assert len(links) == len(sample_alerts)
        assert {link.alert_id for link in links} == {alert.id for alert in sample_alerts}

    def test_backfill_creates_missing_junction_rows(self, db_session, sample_alerts):
        summary = Summary(
            title="Backfill Me",
            content="Body",
            summary_type="daily",
            alert_ids=json.dumps([sample_alerts[0].id, sample_alerts[1].id]),
            generated_at=NOW,
            created_at=NOW,
        )
        db_session.add(summary)
        db_session.commit()

        stats = backfill_summary_alert_links(session=db_session)
        assert stats["inserted"] == 2

        links = (
            db_session.query(SummaryAlertLink)
            .filter(SummaryAlertLink.summary_id == summary.id)
            .all()
        )
        assert {link.alert_id for link in links} == {sample_alerts[0].id, sample_alerts[1].id}

    def test_backfill_skips_missing_alert_ids(self, db_session, sample_alerts):
        summary = Summary(
            title="Backfill Missing",
            content="Body",
            summary_type="daily",
            alert_ids=json.dumps([sample_alerts[0].id, 999999]),
            generated_at=NOW,
            created_at=NOW,
        )
        db_session.add(summary)
        db_session.commit()

        stats = backfill_summary_alert_links(session=db_session)
        assert stats["inserted"] == 1
        assert stats["skipped_missing_alert"] == 1


class TestFeedbackModel:
    def test_feedback_user_fk_exists(self, db_session):
        foreign_keys = inspect(db_session.bind).get_foreign_keys("feedback")
        assert any(
            fk["referred_table"] == "users" and fk["referred_columns"] == ["id"]
            for fk in foreign_keys
        )


class TestUserModel:
    def test_create_user(self, db_session):
        user = User(
            display_name="Alice", email="alice@test.com",
            password_hash=password_hash("AlicePass123!"),
            created_at=NOW, updated_at=NOW,
        )
        db_session.add(user)
        db_session.commit()
        assert user.id is not None
        assert user.password_hash != "AlicePass123!"
        assert verify_password("AlicePass123!", user.password_hash)
        assert decrypt_email(user.email) == "alice@test.com"

    def test_unique_email_constraint(self, db_session):
        u1 = User(
            display_name="A", email="same@test.com",
            password_hash=password_hash("SamePass123!"), created_at=NOW, updated_at=NOW,
        )
        u2 = User(
            display_name="B", email="same@test.com",
            password_hash=password_hash("SamePass456!"), created_at=NOW, updated_at=NOW,
        )
        db_session.add(u1)
        db_session.commit()
        db_session.add(u2)
        with pytest.raises(IntegrityError):
            db_session.commit()

    def test_email_lookup_hash_populated(self, db_session):
        user = User(
            display_name="Hash Test", email="hash@test.com",
            password_hash=password_hash("HashPass123!"), created_at=NOW, updated_at=NOW,
        )
        db_session.add(user)
        db_session.commit()
        assert user.email_lookup_hash == hash_email("hash@test.com")

    def test_backfill_user_alert_preferences_from_json(self, db_session):
        user = User(
            display_name="Prefs",
            email="prefs@test.com",
            password_hash=password_hash("PrefsPass123!"),
            alert_types=json.dumps(["weather", "wildfire", "weather"]),
            created_at=NOW,
            updated_at=NOW,
        )
        db_session.add(user)
        db_session.commit()

        stats = backfill_user_alert_preferences(session=db_session)
        assert stats["inserted"] == 2

        rows = (
            db_session.query(UserAlertPreference)
            .filter(UserAlertPreference.user_id == user.id)
            .order_by(UserAlertPreference.alert_type.asc())
            .all()
        )
        assert [row.alert_type for row in rows] == ["weather", "wildfire"]


class TestScrapeLogModel:
    def test_create_scrape_log(self, db_session):
        log = ScrapeLog(
            source="nws", status="success",
            alerts_fetched=10, alerts_new=3,
            duration_ms=450,
            started_at=NOW, completed_at=NOW,
        )
        db_session.add(log)
        db_session.commit()
        assert log.id is not None
        assert log.alerts_fetched == 10
        assert log.alerts_new == 3
