"""Tests for feedback API endpoints."""


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


class TestFeedbackAnalytics:
    def test_feedback_analytics_summary(self, test_client):
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

    def test_feedback_analytics_filters_by_session(self, test_client):
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

    def test_feedback_weekly_report(self, test_client):
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

    def test_feedback_weekly_report_filters_by_category(self, test_client):
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

        resp = test_client.get(
            "/api/v1/feedback/analytics/weekly",
            params={"days": 7, "response_category": "docs"},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["total_feedback"] == 1
        assert data["average_rating"] == 5.0