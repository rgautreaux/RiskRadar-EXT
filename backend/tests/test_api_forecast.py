"""Tests for forecast API endpoints."""

import json
from datetime import datetime, timedelta, timezone


def _login(test_client, email: str, password: str = "password123"):
    resp = test_client.post(
        "/api/v1/auth/login",
        json={"email": email, "password": password},
    )
    assert resp.status_code == 200


class TestForecastEndpoint:
    def test_forecast_returns_points_and_summary(self, test_client, sample_user, sample_alerts):
        assert sample_alerts
        _ = sample_user
        _login(test_client, "test@example.com")
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

    def test_personalized_forecast_marks_response(self, test_client, sample_user, sample_alerts, db_session):
        assert sample_alerts
        sample_user.health_conditions = json.dumps(["asthma", "respiratory"])
        db_session.add(sample_user)
        db_session.commit()
        db_session.refresh(sample_user)

        _login(test_client, "test@example.com")
        resp = test_client.get(f"/api/v1/forecast/personalized/{sample_user.id}?location=Los Angeles")
        assert resp.status_code == 200

        data = resp.json()
        assert data["personalized"] is True
        assert data["forecast_points"]
        assert data["risk_zones"]

    def test_forecast_filters_mixed_timestamp_formats(self, test_client, sample_user, db_session):
        from db.models import Alert
        _ = sample_user

        now = datetime.now(timezone.utc)
        rows = [
            Alert(
                source="nws",
                source_id="f-mix-z",
                alert_type="weather",
                severity="high",
                title="Forecast Z",
                description="Active Z",
                location_name="Los Angeles, CA",
                event_start=(now - timedelta(hours=1)).strftime("%Y-%m-%dT%H:%M:%SZ"),
                event_end=(now + timedelta(hours=4)).strftime("%Y-%m-%dT%H:%M:%SZ"),
                fetched_at=now.isoformat(),
                created_at=now.isoformat(),
                updated_at=now.isoformat(),
            ),
            Alert(
                source="epa",
                source_id="f-mix-naive",
                alert_type="air_quality",
                severity="moderate",
                title="Forecast Naive",
                description="Active naive",
                location_name="Los Angeles, CA",
                event_start=(now - timedelta(hours=1)).replace(tzinfo=None).isoformat(),
                event_end=(now + timedelta(hours=3)).replace(tzinfo=None).isoformat(),
                fetched_at=now.isoformat(),
                created_at=now.isoformat(),
                updated_at=now.isoformat(),
            ),
            Alert(
                source="firms",
                source_id="f-mix-expired",
                alert_type="wildfire",
                severity="high",
                title="Forecast Expired",
                description="Expired",
                location_name="Los Angeles, CA",
                event_start=(now - timedelta(days=3)).isoformat(),
                event_end=(now - timedelta(hours=1)).isoformat(),
                fetched_at=now.isoformat(),
                created_at=now.isoformat(),
                updated_at=now.isoformat(),
            ),
            Alert(
                source="nws",
                source_id="f-mix-future",
                alert_type="weather",
                severity="low",
                title="Forecast Future",
                description="Future",
                location_name="Los Angeles, CA",
                event_start=(now + timedelta(days=4)).isoformat(),
                event_end=(now + timedelta(days=4, hours=1)).isoformat(),
                fetched_at=now.isoformat(),
                created_at=now.isoformat(),
                updated_at=now.isoformat(),
            ),
        ]

        db_session.add_all(rows)
        db_session.commit()

        _login(test_client, "test@example.com")
        resp = test_client.get("/api/v1/forecast?location=Los Angeles")
        assert resp.status_code == 200
        data = resp.json()

        assert len(data["risk_zones"]) == 2
        assert data["forecast_points"]

    def test_forecast_requires_authentication(self, test_client):
        resp = test_client.get("/api/v1/forecast?location=Los Angeles")
        assert resp.status_code == 401

    def test_personalized_forecast_requires_authentication(self, test_client, sample_user):
        resp = test_client.get(f"/api/v1/forecast/personalized/{sample_user.id}?location=Los Angeles")
        assert resp.status_code == 401

    def test_personalized_forecast_forbids_non_owner(self, test_client, sample_user):
        create_resp = test_client.post(
            "/api/v1/users/register",
            json={
                "display_name": "Other User",
                "email": "other-forecast@test.com",
                "password": "OtherUser123!",
            },
        )
        assert create_resp.status_code == 200

        _login(test_client, "other-forecast@test.com", "OtherUser123!")
        resp = test_client.get(f"/api/v1/forecast/personalized/{sample_user.id}?location=Los Angeles")
        assert resp.status_code == 403
