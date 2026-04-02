"""Tests for Stage 2 Step 1: Personal Risk Scoring Engine."""

import json
import math
import pytest
from datetime import datetime, timezone

from db.models import Alert, User
from scoring import (
    compute_risk_score,
    haversine_km,
    _proximity_score,
    _severity_score,
    _sensitivity_score,
    _density_score,
    _level_from_score,
)


NOW = datetime.now(timezone.utc).isoformat()


# ---------------------------------------------------------------------------
# Geo helper tests
# ---------------------------------------------------------------------------

class TestHaversine:
    def test_same_point_is_zero(self):
        assert haversine_km(34.05, -118.24, 34.05, -118.24) == 0.0

    def test_known_distance(self):
        # LA to San Francisco ≈ 559 km
        dist = haversine_km(34.05, -118.24, 37.77, -122.42)
        assert 550 < dist < 570

    def test_short_distance(self):
        # ~1 km offset in latitude ≈ 0.009 degrees
        dist = haversine_km(34.05, -118.24, 34.059, -118.24)
        assert 0.5 < dist < 1.5


# ---------------------------------------------------------------------------
# Factor calculator tests
# ---------------------------------------------------------------------------

class TestProximityScore:
    def test_empty_returns_zero(self):
        assert _proximity_score([]) == 0.0

    def test_very_close_alert_scores_high(self):
        score = _proximity_score([1.0])
        assert score > 90

    def test_far_alert_scores_low(self):
        score = _proximity_score([140.0])
        assert score < 15

    def test_at_max_radius_is_zero(self):
        score = _proximity_score([150.0])
        assert score == 0.0

    def test_multiple_close_alerts(self):
        score = _proximity_score([5.0, 10.0, 15.0])
        assert score > 80


class TestSeverityScore:
    def test_empty_returns_zero(self):
        assert _severity_score([]) == 0.0

    def test_single_critical(self, db_session):
        alert = Alert(
            source="test", alert_type="weather", severity="critical",
            title="t", fetched_at=NOW, created_at=NOW, updated_at=NOW,
        )
        score = _severity_score([alert])
        assert score == 100.0

    def test_single_low(self, db_session):
        alert = Alert(
            source="test", alert_type="weather", severity="low",
            title="t", fetched_at=NOW, created_at=NOW, updated_at=NOW,
        )
        score = _severity_score([alert])
        assert score == 25.0

    def test_mixed_severity_weighted(self, db_session):
        alerts = [
            Alert(source="test", alert_type="weather", severity="critical",
                  title="t", fetched_at=NOW, created_at=NOW, updated_at=NOW),
            Alert(source="test", alert_type="weather", severity="low",
                  title="t", fetched_at=NOW, created_at=NOW, updated_at=NOW),
        ]
        score = _severity_score(alerts)
        # Best is 100, avg of top is 62.5, so 0.6*100 + 0.4*62.5 = 85
        assert score == 85.0


class TestSensitivityScore:
    def test_no_conditions_returns_zero(self):
        assert _sensitivity_score([], ["air_quality"]) == 0.0

    def test_respiratory_with_air_quality(self):
        score = _sensitivity_score(["respiratory"], ["air_quality"])
        # respiratory maps to [air_quality, wildfire], 1/2 matched = 50
        assert score == 50.0

    def test_respiratory_with_both_matches(self):
        score = _sensitivity_score(["respiratory"], ["air_quality", "wildfire"])
        assert score == 100.0

    def test_unknown_condition(self):
        score = _sensitivity_score(["unknown_condition"], ["air_quality"])
        assert score == 0.0

    def test_multiple_conditions(self):
        score = _sensitivity_score(
            ["respiratory", "cardiovascular"],
            ["air_quality", "weather"],
        )
        # respiratory: air_quality(yes)+wildfire(no) = 1/2
        # cardiovascular: air_quality(yes)+weather(yes) = 2/2
        # total: 3/4 = 75
        assert score == 75.0


class TestDensityScore:
    def test_zero_alerts(self):
        assert _density_score(0) == 0.0

    def test_two_alerts(self):
        assert _density_score(2) == 25.0

    def test_five_alerts(self):
        assert _density_score(5) == 50.0

    def test_twenty_plus_alerts(self):
        assert _density_score(25) == 100.0


class TestLevelFromScore:
    def test_low(self):
        assert _level_from_score(0) == "low"
        assert _level_from_score(25) == "low"

    def test_moderate(self):
        assert _level_from_score(26) == "moderate"
        assert _level_from_score(50) == "moderate"

    def test_high(self):
        assert _level_from_score(51) == "high"
        assert _level_from_score(75) == "high"

    def test_critical(self):
        assert _level_from_score(76) == "critical"
        assert _level_from_score(100) == "critical"


# ---------------------------------------------------------------------------
# Integration: compute_risk_score
# ---------------------------------------------------------------------------

class TestComputeRiskScore:
    def _make_user(self, db_session, lat=34.05, lon=-118.24, conditions=None):
        from passlib.context import CryptContext
        pwd = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")
        user = User(
            display_name="Scorer",
            email="scorer@test.com",
            password_hash=pwd.hash("pass"),
            latitude=lat,
            longitude=lon,
            health_conditions=json.dumps(conditions or []),
            created_at=NOW,
            updated_at=NOW,
        )
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)
        return user

    def _add_alert(self, db_session, lat, lon, severity="moderate", alert_type="weather"):
        alert = Alert(
            source="test",
            source_id=f"test_{lat}_{lon}",
            alert_type=alert_type,
            severity=severity,
            title="Test Alert",
            latitude=lat,
            longitude=lon,
            fetched_at=NOW,
            created_at=NOW,
            updated_at=NOW,
        )
        db_session.add(alert)
        db_session.commit()
        return alert

    def test_no_location_returns_zero(self, db_session):
        user = User(
            display_name="No Loc",
            email="noloc@test.com",
            password_hash="x",
            created_at=NOW,
            updated_at=NOW,
        )
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)

        result = compute_risk_score(user, db_session)
        assert result["overall_score"] == 0.0
        assert result["risk_level"] == "low"

    def test_no_nearby_alerts(self, db_session):
        user = self._make_user(db_session)
        # Add alert far away (New York)
        self._add_alert(db_session, 40.71, -74.01)

        result = compute_risk_score(user, db_session)
        assert result["overall_score"] == 0.0
        assert result["nearby_alert_count"] == 0

    def test_nearby_alert_produces_score(self, db_session):
        user = self._make_user(db_session)
        # Alert ~11 km away
        self._add_alert(db_session, 34.15, -118.24, severity="high")

        result = compute_risk_score(user, db_session)
        assert result["overall_score"] > 0
        assert result["nearby_alert_count"] == 1
        assert result["user_id"] == user.id

    def test_health_conditions_amplify_score(self, db_session):
        user_no_cond = self._make_user(db_session, conditions=[])

        # Need a different email for second user
        db_session.query(User).delete()
        db_session.commit()

        user_with_cond = self._make_user(db_session, conditions=["respiratory"])
        self._add_alert(db_session, 34.15, -118.24, severity="high", alert_type="air_quality")

        result_with = compute_risk_score(user_with_cond, db_session)
        assert result_with["overall_score"] > 0
        # Sensitivity factor should be non-zero
        sens_factor = next(f for f in result_with["factors"] if f["name"] == "health_sensitivity")
        assert sens_factor["value"] > 0

    def test_deterministic_same_input(self, db_session):
        user = self._make_user(db_session)
        self._add_alert(db_session, 34.15, -118.24, severity="high")

        r1 = compute_risk_score(user, db_session)
        r2 = compute_risk_score(user, db_session)
        assert r1["overall_score"] == r2["overall_score"]
        assert r1["risk_level"] == r2["risk_level"]

    def test_response_has_all_factors(self, db_session):
        user = self._make_user(db_session)
        self._add_alert(db_session, 34.15, -118.24)

        result = compute_risk_score(user, db_session)
        factor_names = {f["name"] for f in result["factors"]}
        assert factor_names == {"proximity", "severity", "health_sensitivity", "alert_density"}


# ---------------------------------------------------------------------------
# API endpoint tests
# ---------------------------------------------------------------------------

class TestRiskScoreAPI:
    def test_get_risk_score(self, test_client, db_session):
        from passlib.context import CryptContext
        pwd = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")
        user = User(
            display_name="API User",
            email="apiuser@test.com",
            password_hash=pwd.hash("pass"),
            latitude=34.05,
            longitude=-118.24,
            created_at=NOW,
            updated_at=NOW,
        )
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)

        resp = test_client.get(f"/api/v1/risk/score/{user.id}")
        assert resp.status_code == 200
        data = resp.json()
        assert "overall_score" in data
        assert "risk_level" in data
        assert "factors" in data
        assert len(data["factors"]) == 4

    def test_risk_score_user_not_found(self, test_client):
        resp = test_client.get("/api/v1/risk/score/9999")
        assert resp.status_code == 404

    def test_risk_score_with_alerts(self, test_client, db_session, sample_alerts):
        from passlib.context import CryptContext
        pwd = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")
        user = User(
            display_name="Near LA",
            email="nearla@test.com",
            password_hash=pwd.hash("pass"),
            latitude=34.05,
            longitude=-118.24,
            health_conditions=json.dumps(["respiratory"]),
            created_at=NOW,
            updated_at=NOW,
        )
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)

        resp = test_client.get(f"/api/v1/risk/score/{user.id}")
        assert resp.status_code == 200
        data = resp.json()
        assert data["overall_score"] > 0
        assert data["nearby_alert_count"] > 0

    def test_risk_score_custom_radius(self, test_client, db_session, sample_alerts):
        from passlib.context import CryptContext
        pwd = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")
        user = User(
            display_name="Radius Test",
            email="radius@test.com",
            password_hash=pwd.hash("RadiusPass123!"),
            latitude=34.05,
            longitude=-118.24,
            created_at=NOW,
            updated_at=NOW,
        )
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)

        # Very small radius should exclude most alerts
        resp = test_client.get(f"/api/v1/risk/score/{user.id}?radius_km=1")
        assert resp.status_code == 200
        data = resp.json()
        assert data["nearby_alert_count"] <= 1

    def test_update_health_conditions(self, test_client, db_session):
        # Register user
        resp = test_client.post("/api/v1/users/register", json={
            "display_name": "Health User",
            "email": "health@test.com",
            "password": "HealthPass123!",
        })
        user_id = resp.json()["id"]

        # Update with health conditions
        resp = test_client.put(f"/api/v1/users/{user_id}/preferences", json={
            "health_conditions": ["respiratory", "cardiovascular"],
            "latitude": 34.05,
            "longitude": -118.24,
        })
        assert resp.status_code == 200
        data = resp.json()
        assert data["health_conditions"] is not None
        conditions = json.loads(data["health_conditions"])
        assert "respiratory" in conditions
        assert "cardiovascular" in conditions
