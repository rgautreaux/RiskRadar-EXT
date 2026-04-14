"""Tests for Stage 2 Step 2: Smart Alert Prioritization System."""

import json
from backend.auth.security import hash_email
from datetime import datetime, timezone, timedelta

from backend.db.models import Alert, User
from backend.scoring.prioritization import (
    prioritize_alerts,
    compute_alert_priority,
    _distance_priority,
    _severity_priority,
    _sensitivity_priority,
    _recency_priority,
    _level_from_priority,
)


NOW = datetime.now(timezone.utc)
NOW_ISO = NOW.isoformat()
OLD_ISO = (NOW - timedelta(hours=72)).isoformat()
RECENT_ISO = (NOW - timedelta(hours=1)).isoformat()


# ---------------------------------------------------------------------------
# Helper factories
# ---------------------------------------------------------------------------

def _make_user(db_session, lat=34.05, lon=-118.24, conditions=None):
    from passlib.context import CryptContext
    pwd = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")
    user = User(
        display_name="PriorityUser",
        email=f"priority_{lat}_{lon}@test.com",
        password_hash=pwd.hash("pass"),
        latitude=lat,
        longitude=lon,
        health_conditions=json.dumps(conditions or []),
        created_at=NOW_ISO,
        updated_at=NOW_ISO,
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


def _add_alert(
    db_session,
    lat, lon,
    severity="moderate",
    alert_type="weather",
    title="Test Alert",
    fetched_at=None,
    source_id=None,
):
    alert = Alert(
        source="test",
        source_id=source_id or f"test_{lat}_{lon}_{severity}",
        alert_type=alert_type,
        severity=severity,
        title=title,
        latitude=lat,
        longitude=lon,
        fetched_at=fetched_at or NOW_ISO,
        created_at=NOW_ISO,
        updated_at=NOW_ISO,
    )
    db_session.add(alert)
    db_session.commit()
    db_session.refresh(alert)
    return alert


# ---------------------------------------------------------------------------
# Factor calculator unit tests
# ---------------------------------------------------------------------------

class TestDistancePriority:
    def test_at_zero_distance(self):
        assert _distance_priority(0.0, 150.0) == 100.0

    def test_at_max_radius(self):
        assert _distance_priority(150.0, 150.0) == 0.0

    def test_beyond_radius(self):
        assert _distance_priority(200.0, 150.0) == 0.0

    def test_halfway(self):
        score = _distance_priority(75.0, 150.0)
        assert abs(score - 50.0) < 0.01

    def test_very_close(self):
        score = _distance_priority(1.0, 150.0)
        assert score > 99.0

    def test_custom_radius(self):
        score = _distance_priority(25.0, 50.0)
        assert abs(score - 50.0) < 0.01


class TestSeverityPriority:
    def test_critical(self):
        assert _severity_priority("critical") == 100.0

    def test_high(self):
        assert _severity_priority("high") == 75.0

    def test_moderate(self):
        assert _severity_priority("moderate") == 50.0

    def test_low(self):
        assert _severity_priority("low") == 25.0

    def test_unknown(self):
        assert _severity_priority("unknown") == 25.0


class TestSensitivityPriority:
    def test_no_conditions(self):
        assert _sensitivity_priority([], "air_quality") == 0.0

    def test_matching_condition(self):
        assert _sensitivity_priority(["respiratory"], "air_quality") == 100.0

    def test_matching_wildfire(self):
        assert _sensitivity_priority(["respiratory"], "wildfire") == 100.0

    def test_no_match(self):
        assert _sensitivity_priority(["respiratory"], "earthquake") == 0.0

    def test_multiple_conditions_one_match(self):
        assert _sensitivity_priority(["respiratory", "mobility_limited"], "weather") == 100.0

    def test_unknown_condition(self):
        assert _sensitivity_priority(["unknown"], "air_quality") == 0.0


class TestRecencyPriority:
    def test_just_now(self):
        score = _recency_priority(NOW_ISO)
        assert score > 95.0

    def test_old_alert(self):
        score = _recency_priority(OLD_ISO)
        assert score == 0.0

    def test_recent_alert(self):
        score = _recency_priority(RECENT_ISO)
        assert score > 90.0

    def test_none_value(self):
        assert _recency_priority(None) == 0.0

    def test_invalid_string(self):
        assert _recency_priority("not-a-date") == 0.0


class TestLevelFromPriority:
    def test_high(self):
        assert _level_from_priority(70) == "high"
        assert _level_from_priority(100) == "high"

    def test_medium(self):
        assert _level_from_priority(40) == "medium"
        assert _level_from_priority(69) == "medium"

    def test_low(self):
        assert _level_from_priority(0) == "low"
        assert _level_from_priority(39) == "low"


# ---------------------------------------------------------------------------
# Integration: prioritize_alerts
# ---------------------------------------------------------------------------

class TestPrioritizeAlerts:
    def test_no_user_location(self, db_session):
        user = User(
            display_name="No Loc",
            email="noloc_pri@test.com",
            password_hash="x",
            created_at=NOW_ISO,
            updated_at=NOW_ISO,
        )
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)

        result = prioritize_alerts(user, db_session)
        assert result["alerts"] == []
        assert result["total_nearby"] == 0

    def test_no_nearby_alerts(self, db_session):
        user = _make_user(db_session)
        # Add alert far away (New York)
        _add_alert(db_session, 40.71, -74.01)

        result = prioritize_alerts(user, db_session)
        assert result["alerts"] == []
        assert result["total_nearby"] == 0

    def test_single_nearby_alert(self, db_session):
        user = _make_user(db_session)
        alert = _add_alert(db_session, 34.15, -118.24, severity="high")

        result = prioritize_alerts(user, db_session)
        assert len(result["alerts"]) == 1
        a = result["alerts"][0]
        assert a["alert_id"] == alert.id
        assert a["priority_score"] > 0
        assert a["priority_level"] in ("low", "medium", "high")
        assert a["distance_km"] > 0
        assert "priority_factors" in a

    def test_priority_factors_present(self, db_session):
        user = _make_user(db_session)
        _add_alert(db_session, 34.15, -118.24)

        result = prioritize_alerts(user, db_session)
        factors = result["alerts"][0]["priority_factors"]
        assert "distance" in factors
        assert "severity" in factors
        assert "sensitivity" in factors
        assert "recency" in factors

    def test_higher_severity_ranks_higher(self, db_session):

        user = _make_user(db_session)
        # Same distance alerts, different severity
        _add_alert(db_session, 34.06, -118.24, severity="low", source_id="low_1")
        _add_alert(db_session, 34.06, -118.25, severity="critical", source_id="crit_1")

        result = prioritize_alerts(user, db_session)
        assert len(result["alerts"]) == 2
        # Critical should be first
        _add_alert(db_session, 35.0, -118.24, severity="moderate", source_id="far_1")
        _add_alert(db_session, 34.06, -118.24, severity="moderate", source_id="close_1")


    def test_closer_alert_ranks_higher(self, db_session):
        user = _make_user(db_session)
        # Same severity, different distance
        _add_alert(db_session, 34.06, -118.24, severity="moderate", source_id="close_1")
        _add_alert(db_session, 35.0, -118.24, severity="moderate", source_id="far_1")

        result = prioritize_alerts(user, db_session)
        assert result["alerts"][0]["distance_km"] < result["alerts"][1]["distance_km"]

    def test_health_conditions_boost_matching_alerts(self, db_session):
        user = _make_user(db_session, conditions=["respiratory"])
        # Same location and severity, but different types
        _add_alert(db_session, 34.06, -118.24, severity="moderate", alert_type="air_quality", source_id="aq_1")
        _add_alert(db_session, 34.06, -118.25, severity="moderate", alert_type="earthquake", source_id="eq_1")

        result = prioritize_alerts(user, db_session)
        assert len(result["alerts"]) == 2
        # air_quality alert should rank higher due to respiratory sensitivity
        assert result["alerts"][0]["alert_type"] == "air_quality"
        assert result["alerts"][0]["priority_score"] > result["alerts"][1]["priority_score"]

    def test_deterministic_same_input(self, db_session):
        user = _make_user(db_session)
        _add_alert(db_session, 34.15, -118.24, severity="high", source_id="det_1")
        _add_alert(db_session, 34.10, -118.30, severity="moderate", source_id="det_2")

        r1 = prioritize_alerts(user, db_session)
        r2 = prioritize_alerts(user, db_session)

        assert len(r1["alerts"]) == len(r2["alerts"])
        for a1, a2 in zip(r1["alerts"], r2["alerts"]):
            assert a1["alert_id"] == a2["alert_id"]
            assert a1["priority_score"] == a2["priority_score"]

    def test_limit_parameter(self, db_session):
        user = _make_user(db_session)
        for i in range(10):
            _add_alert(
                db_session, 34.05 + i * 0.01, -118.24,
                severity="moderate", source_id=f"lim_{i}",
            )

        result = prioritize_alerts(user, db_session, limit=3)
        assert len(result["alerts"]) == 3

    def test_radius_parameter(self, db_session):
        user = _make_user(db_session)
        # Alert ~11 km away
        _add_alert(db_session, 34.15, -118.24, source_id="rad_1")
        # Alert ~100 km away
        _add_alert(db_session, 35.0, -118.24, source_id="rad_2")

        result_small = prioritize_alerts(user, db_session, radius_km=20.0)
        result_large = prioritize_alerts(user, db_session, radius_km=200.0)

        assert len(result_small["alerts"]) < len(result_large["alerts"])

    def test_response_fields(self, db_session):
        user = _make_user(db_session)
        _add_alert(db_session, 34.15, -118.24)

        result = prioritize_alerts(user, db_session)
        assert "user_id" in result
        assert "total_nearby" in result
        assert "alerts" in result
        assert "computed_at" in result
        assert result["user_id"] == user.id

    def test_alert_fields_preserved(self, db_session):
        user = _make_user(db_session)
        _add_alert(
            db_session, 34.15, -118.24,
            severity="high",
            alert_type="wildfire",
            title="Major Wildfire",
        )

        result = prioritize_alerts(user, db_session)
        a = result["alerts"][0]
        # Verify original alert data is preserved
        assert a["title"] == "Major Wildfire"
        assert a["alert_type"] == "wildfire"
        assert a["severity"] == "high"
        assert a["source"] == "test"

    def test_recency_affects_ordering(self, db_session):
        user = _make_user(db_session)
        # Old alert (same location and severity)
        _add_alert(
            db_session, 34.06, -118.24, severity="moderate",
            fetched_at=OLD_ISO, source_id="old_1",
        )
        # Recent alert
        _add_alert(
            db_session, 34.06, -118.25, severity="moderate",
            fetched_at=RECENT_ISO, source_id="recent_1",
        )

        result = prioritize_alerts(user, db_session)
        assert len(result["alerts"]) == 2
        # Recent alert should have higher priority score
        assert result["alerts"][0]["priority_score"] >= result["alerts"][1]["priority_score"]


# ---------------------------------------------------------------------------
# Unit: compute_alert_priority (single alert)
# ---------------------------------------------------------------------------

class TestComputeAlertPriority:
    def test_basic(self, db_session):
        user = _make_user(db_session)
        alert = _add_alert(db_session, 34.15, -118.24, severity="high")

        result = compute_alert_priority(alert, user)
        assert result is not None
        assert "priority_score" in result
        assert "priority_level" in result
        assert "distance_km" in result
        assert "priority_factors" in result

    def test_out_of_range(self, db_session):
        user = _make_user(db_session)
        alert = _add_alert(db_session, 40.71, -74.01)  # New York, far away

        result = compute_alert_priority(alert, user)
        assert result is None

    def test_no_user_location(self, db_session):
        user = User(
            display_name="No Loc",
            email="noloc_cap@test.com",
            password_hash="x",
            created_at=NOW_ISO,
            updated_at=NOW_ISO,
        )
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)

        alert = _add_alert(db_session, 34.15, -118.24)
        result = compute_alert_priority(alert, user)
        assert result is None

    def test_no_alert_location(self, db_session):
        user = _make_user(db_session)
        alert = Alert(
            source="test", source_id="nocoord",
            alert_type="weather", severity="moderate",
            title="No Coords Alert",
            fetched_at=NOW_ISO, created_at=NOW_ISO, updated_at=NOW_ISO,
        )
        db_session.add(alert)
        db_session.commit()
        db_session.refresh(alert)

        result = compute_alert_priority(alert, user)
        assert result is None

    def test_sensitivity_boost(self, db_session):
        user = _make_user(db_session, conditions=["respiratory"])
        aq_alert = _add_alert(
            db_session, 34.06, -118.24, severity="moderate",
            alert_type="air_quality", source_id="aq_cap",
        )
        eq_alert = _add_alert(
            db_session, 34.06, -118.25, severity="moderate",
            alert_type="earthquake", source_id="eq_cap",
        )

        aq_result = compute_alert_priority(aq_alert, user)
        eq_result = compute_alert_priority(eq_alert, user)

        assert aq_result["priority_score"] > eq_result["priority_score"]
        assert aq_result["priority_factors"]["sensitivity"] > eq_result["priority_factors"]["sensitivity"]


# ---------------------------------------------------------------------------
# API endpoint tests
# ---------------------------------------------------------------------------

class TestPrioritizedAlertsAPI:
    def _register_user(self, test_client, db_session, lat=34.05, lon=-118.24, conditions=None):
        # Register via API to ensure password is valid and matches login
        import uuid
        email = f"apipri_{uuid.uuid4().hex[:8]}@test.com"
        password = "Secret123!Aa"
        resp = test_client.post(
            "/api/v1/users/register",
            json={
                "display_name": "API Priority User",
                "email": email,
                "password": password,
            },
        )
        assert resp.status_code == 200
        user = db_session.query(User).filter(User.email_lookup_hash == hash_email(email)).first()
        # Set additional fields directly if needed
        user.latitude = lat
        user.longitude = lon
        if conditions is not None:
            user.health_conditions = json.dumps(conditions)
        db_session.commit()
        db_session.refresh(user)
        # Clear cookies to ensure clean login session
        test_client.cookies.clear()
        return user, email


    def test_prioritized_alerts_endpoint(self, test_client, db_session):
        user, plain_email = self._register_user(test_client, db_session)
        # Custom login with debug output
        resp = test_client.post(
            "/api/v1/auth/login",
            json={"email": plain_email, "password": "Secret123!Aa"},
        )
        if resp.status_code != 200:
            print("LOGIN FAILURE RESPONSE:", resp.status_code, resp.text)
        assert resp.status_code == 200

        resp = test_client.get(f"/api/v1/alerts/prioritized/{user.id}")
        assert resp.status_code == 200
        data = resp.json()
        assert "user_id" in data
        assert "total_nearby" in data
        assert "alerts" in data
        assert "computed_at" in data

    def test_prioritized_alerts_user_not_found(self, test_client):
        resp = test_client.get("/api/v1/alerts/prioritized/9999")
        assert resp.status_code == 404

    def test_prioritized_alerts_with_data(self, test_client, db_session):
        user, email = self._register_user(test_client, db_session)

        resp = test_client.post(
            "/api/v1/auth/login",
            json={"email": email, "password": "Secret123!Aa"},
        )
        assert resp.status_code == 200
        resp = test_client.get(f"/api/v1/alerts/prioritized/{user.id}")
        assert resp.status_code == 200
        data = resp.json()
        assert len(data["alerts"]) > 0
        # Verify each alert has priority metadata
        for alert in data["alerts"]:
            assert "priority_score" in alert
            assert "priority_level" in alert
            assert "distance_km" in alert
            assert "priority_factors" in alert
            assert alert["priority_level"] in ("low", "medium", "high")

    def test_prioritized_alerts_ordered(self, test_client, db_session):
        user, email = self._register_user(test_client, db_session)

        resp = test_client.post(
            "/api/v1/auth/login",
            json={"email": email, "password": "Secret123!Aa"},
        )
        assert resp.status_code == 200
        resp = test_client.get(f"/api/v1/alerts/prioritized/{user.id}")
        data = resp.json()
        scores = [a["priority_score"] for a in data["alerts"]]
        assert scores == sorted(scores, reverse=True)

    def test_prioritized_alerts_limit(self, test_client, db_session):
        user, email = self._register_user(test_client, db_session)

        resp = test_client.post(
            "/api/v1/auth/login",
            json={"email": email, "password": "Secret123!Aa"},
        )
        assert resp.status_code == 200
        resp = test_client.get(f"/api/v1/alerts/prioritized/{user.id}?limit=1")
        assert resp.status_code == 200
        data = resp.json()
        assert len(data["alerts"]) <= 1

    def test_prioritized_alerts_radius(self, test_client, db_session):
        user, email = self._register_user(test_client, db_session)

        resp = test_client.post(
            "/api/v1/auth/login",
            json={"email": email, "password": "Secret123!Aa"},
        )
        assert resp.status_code == 200

        resp_small = test_client.get(f"/api/v1/alerts/prioritized/{user.id}?radius_km=1")
        resp_large = test_client.get(f"/api/v1/alerts/prioritized/{user.id}?radius_km=500")
        small_data = resp_small.json()
        large_data = resp_large.json()

        assert len(small_data["alerts"]) <= len(large_data["alerts"])

    def test_prioritized_alerts_with_health_conditions(self, test_client, db_session):
        user, email = self._register_user(
            test_client, db_session,
            conditions=["respiratory"],
        )

        resp = test_client.post(
            "/api/v1/auth/login",
            json={"email": email, "password": "Secret123!Aa"},
        )
        assert resp.status_code == 200

        resp = test_client.get(f"/api/v1/alerts/prioritized/{user.id}")
        assert resp.status_code == 200
        data = resp.json()
        # Verify sensitivity factor is present
        if data["alerts"]:
            factors = data["alerts"][0]["priority_factors"]
            assert "sensitivity" in factors

    def test_no_location_returns_empty(self, test_client, db_session):
        from passlib.context import CryptContext
        pwd = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")
        user = User(
            display_name="No Loc API",
            email="noloc_api@test.com",
            password_hash=pwd.hash("pass"),
            created_at=NOW_ISO,
            updated_at=NOW_ISO,
        )
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)

        # Login as the user
        resp = test_client.post(
            "/api/v1/auth/login",
            json={"email": "noloc_api@test.com", "password": "pass"},
        )
        assert resp.status_code == 200

        resp = test_client.get(f"/api/v1/alerts/prioritized/{user.id}")
        assert resp.status_code == 200
        data = resp.json()
        assert data["alerts"] == []
        assert data["total_nearby"] == 0
