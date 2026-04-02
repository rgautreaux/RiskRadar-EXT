"""Tests for map API endpoints (alerts and risk overlays)."""

class TestMapEndpoints:
    def test_risk_map_polygons(self, test_client):
        resp = test_client.get("/api/v1/risk/map")
        assert resp.status_code == 200
        data = resp.json()
        assert "risk_zones" in data
        for zone in data["risk_zones"]:
            if zone.get("polygon"):
                poly = zone["polygon"]
                assert isinstance(poly, list)
                assert len(poly) >= 4  # Should be a closed polygon
                for pt in poly:
                    assert "lat" in pt and "lon" in pt
                    assert isinstance(pt["lat"], float)
                    assert isinstance(pt["lon"], float)

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
