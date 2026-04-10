"""Tests for assistant API endpoint."""


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
