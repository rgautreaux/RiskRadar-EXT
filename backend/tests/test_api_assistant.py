"""Tests for assistant API endpoint."""

# pylint: disable=protected-access
import json
from datetime import datetime, timedelta, timezone

import pytest

from backend.api import assistant as assistant_api
from config.settings import settings


@pytest.fixture(autouse=True)
def reset_guest_limit_cache():
    assistant_api._guest_limit_cache.clear()
    yield
    assistant_api._guest_limit_cache.clear()


class TestAssistantRespond:
    def test_guardrail_response(self, test_client):
        resp = test_client.post(
            "/api/v1/assistant/respond",
            json={"message": "Can you give me medical advice for asthma?"},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["category"] == "guardrail"
        assert data["used_live_data"] is False
        assert "cannot provide medical advice" in data["reply"].lower()

    def test_guest_daily_limit_and_lockout(self, test_client):
        """Guests should be locked out after exceeding the daily chat limit."""
        limit = settings.GUEST_DAILY_LIMIT

        for index in range(limit):
            resp = test_client.post(
                "/api/v1/assistant/respond",
                json={"message": f"test message {index + 1}"},
            )
            assert resp.status_code == 200
            data = resp.json()
            assert "daily limit" not in data["reply"].lower()

        resp = test_client.post(
            "/api/v1/assistant/respond",
            json={"message": "should trigger lockout"},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert "daily limit" in data["reply"].lower()
        assert data["category"] == "fallback"
        assert "guest-limit" in data["sources"]

    def test_guest_personalized_lockout(self, test_client):
        resp = test_client.post(
            "/api/v1/assistant/respond",
            json={"message": "What is my risk score?"},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["category"] == "fallback"
        assert "registered users" in data["reply"].lower()
        assert "guest-lockout" in data["sources"]

    def test_registered_user_not_limited(self, test_client, sample_user):
        """Registered users should not be affected by guest daily limit."""
        login_resp = test_client.post(
            "/api/v1/auth/login",
            json={"email": "test@example.com", "password": "password123"},
        )
        assert login_resp.status_code == 200

        for index in range(settings.GUEST_DAILY_LIMIT + 5):
            resp = test_client.post(
                "/api/v1/assistant/respond",
                json={"message": f"user message {index + 1}", "user_id": sample_user.id},
            )
            assert resp.status_code == 200
            data = resp.json()
            assert "daily limit" not in data["reply"].lower()

    def test_live_forecast_summary_response(self, test_client, sample_alerts):
        assert sample_alerts
        resp = test_client.post(
            "/api/v1/assistant/respond",
            json={"message": "forecast for Los Angeles", "location": "Los Angeles"},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["category"] == "live"
        assert data["used_live_data"] is True
        assert "forecast summary" in data["reply"].lower()

    def test_user_not_found(self, test_client):
        resp = test_client.post(
            "/api/v1/assistant/respond",
            json={"message": "show latest alerts", "user_id": 99999},
        )
        assert resp.status_code == 404
        assert "User not found" in resp.json()["detail"]

    def test_profile_shaped_help_response(self, test_client, sample_user, db_session):
        from db.models import User

        user = db_session.query(User).filter(User.id == sample_user.id).first()
        profile = json.loads(user.assistant_style_profile)
        profile["tone"]["warmth"] = 0.9
        user.assistant_style_profile = json.dumps(profile)
        db_session.commit()

        resp = test_client.post(
            "/api/v1/assistant/respond",
            json={"message": "help", "user_id": sample_user.id},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["category"] == "fallback"
        assert data["reply"].startswith("Absolutely.")

    def test_style_directive_persists_for_known_user(self, test_client, sample_user, db_session):
        from db.models import User

        before = db_session.query(User).filter(User.id == sample_user.id).first()
        before_profile = json.loads(before.assistant_style_profile)

        resp = test_client.post(
            "/api/v1/assistant/respond",
            json={"message": "be shorter", "user_id": sample_user.id},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["category"] == "fallback"
        assert "more concise" in data["reply"].lower()

        after = db_session.query(User).filter(User.id == sample_user.id).first()
        after_profile = json.loads(after.assistant_style_profile)
        assert after_profile["delivery"]["conciseness"] > before_profile["delivery"]["conciseness"]

    def test_style_directive_works_anonymous_without_persistence(self, test_client):
        resp = test_client.post(
            "/api/v1/assistant/respond",
            json={"message": "be goofy"},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["category"] == "fallback"
        assert "for this reply" in data["reply"].lower()

    def test_alert_filter_handles_mixed_timestamp_formats(self, test_client, db_session):
        from db.models import Alert

        now = datetime.now(timezone.utc)

        active_z = Alert(
            source="nws",
            source_id="mix-z",
            alert_type="weather",
            severity="high",
            title="Active Z Alert",
            description="Active alert with Z format",
            location_name="Los Angeles, CA",
            event_start=(now - timedelta(hours=1)).strftime("%Y-%m-%dT%H:%M:%SZ"),
            event_end=(now + timedelta(hours=1)).strftime("%Y-%m-%dT%H:%M:%SZ"),
            fetched_at=now.isoformat(),
            created_at=now.isoformat(),
            updated_at=now.isoformat(),
        )
        active_naive = Alert(
            source="epa",
            source_id="mix-naive",
            alert_type="pollution",
            severity="moderate",
            title="Active Naive Alert",
            description="Active alert with naive format",
            location_name="Los Angeles, CA",
            event_start=(now - timedelta(hours=2)).replace(tzinfo=None).isoformat(),
            event_end=(now + timedelta(hours=2)).replace(tzinfo=None).isoformat(),
            fetched_at=now.isoformat(),
            created_at=now.isoformat(),
            updated_at=now.isoformat(),
        )
        expired = Alert(
            source="firms",
            source_id="mix-expired",
            alert_type="wildfire",
            severity="high",
            title="Expired Alert",
            description="Should be filtered out",
            location_name="Los Angeles, CA",
            event_start=(now - timedelta(days=2)).isoformat(),
            event_end=(now - timedelta(hours=2)).isoformat(),
            fetched_at=now.isoformat(),
            created_at=now.isoformat(),
            updated_at=now.isoformat(),
        )
        future = Alert(
            source="nws",
            source_id="mix-future",
            alert_type="weather",
            severity="low",
            title="Future Alert",
            description="Should be filtered out",
            location_name="Los Angeles, CA",
            event_start=(now + timedelta(days=3)).isoformat(),
            event_end=(now + timedelta(days=3, hours=1)).isoformat(),
            fetched_at=now.isoformat(),
            created_at=now.isoformat(),
            updated_at=now.isoformat(),
        )

        db_session.add_all([active_z, active_naive, expired, future])
        db_session.commit()

        resp = test_client.post(
            "/api/v1/assistant/respond",
            json={"message": "show latest alerts", "location": "Los Angeles"},
        )
        assert resp.status_code == 200
        data = resp.json()
        reply = data["reply"]
        assert "Active Z Alert" in reply
        assert "Active Naive Alert" in reply
        assert "Expired Alert" not in reply
        assert "Future Alert" not in reply
