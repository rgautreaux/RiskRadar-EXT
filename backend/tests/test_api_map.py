"""Tests for map API endpoints (alerts and risk overlays)."""

class TestMapEndpoints:
    def test_alerts_map_empty(self, test_client):
        resp = test_client.get("/api/v1/alerts/map")
        assert resp.status_code == 200
        data = resp.json()
        assert isinstance(data, dict)
        assert "alerts" in data
        assert isinstance(data["alerts"], list)

    def test_risk_map_empty(self, test_client):
        resp = test_client.get("/api/v1/risk/map")
        assert resp.status_code == 200
        data = resp.json()
        assert isinstance(data, dict)
        assert "risk_zones" in data
        assert isinstance(data["risk_zones"], list)

    # Optionally, add more tests with sample data if fixtures are available
