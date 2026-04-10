"""Tests for assistant API endpoint."""

import json


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
