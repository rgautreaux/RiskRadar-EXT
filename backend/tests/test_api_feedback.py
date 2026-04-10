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