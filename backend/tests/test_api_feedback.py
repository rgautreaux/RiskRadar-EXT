"""Tests for feedback API endpoints."""

import json


def _login(test_client, email: str, password: str):
    resp = test_client.post("/api/v1/auth/login", json={"email": email, "password": password})
    assert resp.status_code == 200
    return resp


class TestRecordFeedback:
    def test_create_feedback(self, test_client):
        resp = test_client.post("/api/v1/feedback", json={
            "session_id": "session-1",
            "message_id": "msg-1",
            "reaction": "thumbs_up",
            "rating": 5,
            "page_context": "dashboard",
            "response_category": "live",
            "response_text": "Forecast for your area: ...",
        })
        assert resp.status_code == 200
        data = resp.json()
        assert data["session_id"] == "session-1"
        assert data["message_id"] == "msg-1"
        assert data["reaction"] == "thumbs_up"
        assert data["rating"] == 5
        assert data["response_category"] == "live"

    def test_upsert_feedback_for_same_message(self, test_client):
        first = test_client.post("/api/v1/feedback", json={
            "session_id": "session-2",
            "message_id": "msg-2",
            "reaction": "thumbs_down",
            "rating": 1,
        })
        assert first.status_code == 200

        second = test_client.post("/api/v1/feedback", json={
            "session_id": "session-2",
            "message_id": "msg-2",
            "reaction": "smile",
            "rating": 4,
            "comment": "Much better",
        })
        assert second.status_code == 200
        data = second.json()
        assert data["reaction"] == "smile"
        assert data["rating"] == 4
        assert data["comment"] == "Much better"

    def test_feedback_rejects_invalid_rating(self, test_client):
        resp = test_client.post("/api/v1/feedback", json={
            "session_id": "session-3",
            "message_id": "msg-3",
            "reaction": "thumbs_up",
            "rating": 9,
        })
        assert resp.status_code == 422

    def test_feedback_updates_user_assistant_profile(self, test_client, sample_user, db_session):
        from db.models import User

        _ = sample_user
        _login(test_client, "test@example.com", "password123")

        before = db_session.query(User).filter(User.id == sample_user.id).first()
        before_profile = json.loads(before.assistant_style_profile)
        before_count = before_profile["learning"]["feedback_count"]

        resp = test_client.post("/api/v1/feedback", json={
            "session_id": "session-personality",
            "message_id": "msg-personality",
            "reaction": "smile",
            "rating": 5,
            "comment": "Great tone, not robotic",
        })

        assert resp.status_code == 200

        after = db_session.query(User).filter(User.id == sample_user.id).first()
        after_profile = json.loads(after.assistant_style_profile)

        assert after_profile["learning"]["feedback_count"] == before_count + 1
        assert after_profile["tone"]["warmth"] > before_profile["tone"]["warmth"]


class TestFeedbackAnalytics:
    def test_feedback_analytics_requires_admin(self, test_client):
        resp = test_client.get("/api/v1/feedback/analytics")
        assert resp.status_code == 401

    def test_feedback_analytics_summary(self, test_client, admin_user):
        _ = admin_user
        _login(test_client, "admin@example.com", "password123")
        test_client.post("/api/v1/feedback", json={
            "session_id": "session-analytics",
            "message_id": "msg-1",
            "reaction": "thumbs_up",
            "rating": 5,
            "response_category": "docs",
        })
        test_client.post("/api/v1/feedback", json={
            "session_id": "session-analytics",
            "message_id": "msg-2",
            "reaction": "thumbs_down",
            "rating": 1,
            "response_category": "live",
        })

        resp = test_client.get("/api/v1/feedback/analytics")
        assert resp.status_code == 200
        data = resp.json()
        assert data["total_feedback"] >= 2
        assert data["average_rating"] is not None
        assert any(entry["reaction"] == "thumbs_up" for entry in data["by_reaction"])
        assert any(entry["response_category"] == "docs" for entry in data["by_category"])

    def test_feedback_analytics_filters_by_session(self, test_client, admin_user):
        _ = admin_user
        _login(test_client, "admin@example.com", "password123")
        test_client.post("/api/v1/feedback", json={
            "session_id": "session-filter-a",
            "message_id": "msg-a",
            "reaction": "smile",
            "rating": 4,
            "response_category": "static",
        })
        test_client.post("/api/v1/feedback", json={
            "session_id": "session-filter-b",
            "message_id": "msg-b",
            "reaction": "thumbs_down",
            "rating": 1,
            "response_category": "static",
        })

        resp = test_client.get("/api/v1/feedback/analytics", params={"session_id": "session-filter-a"})
        assert resp.status_code == 200
        data = resp.json()
        assert data["total_feedback"] == 1
        assert data["average_rating"] == 4.0

    def test_feedback_weekly_report(self, test_client, admin_user):
        _ = admin_user
        _login(test_client, "admin@example.com", "password123")
        test_client.post("/api/v1/feedback", json={
            "session_id": "session-weekly",
            "message_id": "msg-w1",
            "reaction": "thumbs_up",
            "rating": 5,
            "response_category": "docs",
        })
        test_client.post("/api/v1/feedback", json={
            "session_id": "session-weekly",
            "message_id": "msg-w2",
            "reaction": "smile",
            "rating": 4,
            "response_category": "live",
        })

        resp = test_client.get("/api/v1/feedback/analytics/weekly", params={"days": 7})
        assert resp.status_code == 200
        data = resp.json()
        assert data["window_days"] == 7
        assert data["total_feedback"] >= 2
        assert len(data["by_day"]) == 7

    def test_feedback_weekly_report_filters_by_category(self, test_client, admin_user):
        _ = admin_user
        _login(test_client, "admin@example.com", "password123")
        test_client.post("/api/v1/feedback", json={
            "session_id": "session-weekly-category",
            "message_id": "msg-c1",
            "reaction": "thumbs_up",
            "rating": 5,
            "response_category": "docs",
        })
        test_client.post("/api/v1/feedback", json={
            "session_id": "session-weekly-category",
            "message_id": "msg-c2",
            "reaction": "thumbs_down",
            "rating": 1,
            "response_category": "live",
        })

        resp = test_client.get("/api/v1/feedback/analytics/weekly", params={"days": 7, "response_category": "docs"})
        assert resp.status_code == 200
        data = resp.json()
        assert data["total_feedback"] == 1
        assert data["average_rating"] == 5.0

    def test_feedback_analytics_rejects_standard_user(self, test_client, sample_user):
        _ = sample_user
        _login(test_client, "test@example.com", "password123")
        resp = test_client.get("/api/v1/feedback/analytics")
        assert resp.status_code == 403


class TestSessionFeedback:
    def test_session_feedback_requires_auth(self, test_client):
        resp = test_client.get("/api/v1/feedback/session/some-session-id")
        assert resp.status_code == 401

    def test_admin_can_see_all_session_feedback(self, test_client, admin_user):
        _ = admin_user
        _login(test_client, "admin@example.com", "password123")
        test_client.post("/api/v1/feedback", json={
            "session_id": "session-admin-view",
            "message_id": "msg-av1",
            "reaction": "thumbs_up",
            "rating": 5,
        })
        resp = test_client.get("/api/v1/feedback/session/session-admin-view")
        assert resp.status_code == 200
        assert len(resp.json()) >= 1

    def test_regular_user_sees_only_own_session_feedback(self, test_client, sample_user, db_session):
        _ = sample_user
        _login(test_client, "test@example.com", "password123")
        resp = test_client.post("/api/v1/feedback", json={
            "session_id": "session-user-own",
            "message_id": "msg-uo1",
            "reaction": "smile",
            "rating": 4,
        })
        assert resp.status_code == 200

        resp = test_client.get("/api/v1/feedback/session/session-user-own")
        assert resp.status_code == 200
        data = resp.json()
        # Only returns feedback owned by this user
        for item in data:
            assert item["user_id"] == sample_user.id