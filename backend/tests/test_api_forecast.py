"""Tests for forecast API endpoints."""

import json


class TestForecastEndpoint:
    def test_forecast_returns_points_and_summary(self, test_client, _sample_alerts):
        resp = test_client.get("/api/v1/forecast?location=Los Angeles")
        assert resp.status_code == 200

        data = resp.json()
        assert data["region"] == "Los Angeles"
        assert data["summary"]
        assert data["confidence"] is not None
        assert data["trend"] in {"increasing", "decreasing", "steady"}

        points = data["forecast_points"]
        assert isinstance(points, list)
        assert len(points) >= 2
        for point in points:
            assert "hour_offset" in point
            assert "risk_score" in point
            assert "risk_level" in point
            assert "confidence" in point

        assert data["baseline_risk_score"] is not None
        assert data["personalized"] is False

    def test_personalized_forecast_marks_response(self, test_client, sample_user, _sample_alerts, db_session):
        sample_user.health_conditions = json.dumps(["asthma", "respiratory"])
        db_session.add(sample_user)
        db_session.commit()
        db_session.refresh(sample_user)

        resp = test_client.get(f"/api/v1/forecast/personalized/{sample_user.id}?location=Los Angeles")
        assert resp.status_code == 200

        data = resp.json()
        assert data["personalized"] is True
        assert data["forecast_points"]
        assert data["risk_zones"]
