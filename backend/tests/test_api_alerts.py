"""Tests for alert API endpoints."""


def _login(test_client, email: str, password: str = "password123"):
    resp = test_client.post(
        "/api/v1/auth/login",
        json={"email": email, "password": password},
    )
    assert resp.status_code == 200


class TestListAlerts:
    def test_list_all(self, test_client, sample_alerts):
        _ = sample_alerts
        resp = test_client.get("/api/v1/alerts")
        assert resp.status_code == 200
        data = resp.json()
        assert len(data) == 3

    def test_filter_by_alert_type(self, test_client, sample_alerts):
        _ = sample_alerts
        resp = test_client.get("/api/v1/alerts?alert_type=weather")
        assert resp.status_code == 200
        data = resp.json()
        assert len(data) == 1
        assert data[0]["alert_type"] == "weather"

    def test_filter_by_severity(self, test_client, sample_alerts):
        _ = sample_alerts
        resp = test_client.get("/api/v1/alerts?severity=moderate")
        data = resp.json()
        assert len(data) == 1
        assert data[0]["severity"] == "moderate"

    def test_filter_by_source(self, test_client, sample_alerts):
        resp = test_client.get("/api/v1/alerts?source=epa")
        data = resp.json()
        assert len(data) == 1
        assert data[0]["source"] == "epa"

    def test_pagination_limit(self, test_client, sample_alerts):
        resp = test_client.get("/api/v1/alerts?limit=2")
        data = resp.json()
        assert len(data) == 2

    def test_pagination_offset(self, test_client, sample_alerts):
        resp = test_client.get("/api/v1/alerts?limit=2&offset=2")
        data = resp.json()
        assert len(data) == 1

    def test_empty_database(self, test_client):
        resp = test_client.get("/api/v1/alerts")
        assert resp.status_code == 200
        assert resp.json() == []


class TestAlertStats:
    def test_stats(self, test_client, sample_alerts):
        resp = test_client.get("/api/v1/alerts/stats")
        assert resp.status_code == 200
        data = resp.json()
        assert data["total"] == 3
        assert data["by_type"]["weather"] == 1
        assert data["by_type"]["pollution"] == 1
        assert data["by_type"]["earthquake"] == 1
        assert data["by_severity"]["high"] == 1
        assert data["by_severity"]["moderate"] == 1
        assert data["by_severity"]["low"] == 1

    def test_stats_empty(self, test_client):
        resp = test_client.get("/api/v1/alerts/stats")
        data = resp.json()
        assert data["total"] == 0


class TestGetAlert:
    def test_get_by_id(self, test_client, sample_alerts):
        alert_id = sample_alerts[0].id
        resp = test_client.get(f"/api/v1/alerts/{alert_id}")
        assert resp.status_code == 200
        assert resp.json()["title"] == "Severe Thunderstorm Warning"

    def test_not_found(self, test_client):
        resp = test_client.get("/api/v1/alerts/9999")
        assert resp.status_code == 404


class TestPrioritizedAlertsAuth:
    def test_prioritized_requires_authentication(self, test_client, sample_user):
        _ = sample_user
        resp = test_client.get(f"/api/v1/alerts/prioritized/{sample_user.id}")
        assert resp.status_code == 401

    def test_prioritized_allows_owner(self, test_client, sample_user):
        _login(test_client, "test@example.com")
        resp = test_client.get(f"/api/v1/alerts/prioritized/{sample_user.id}")
        assert resp.status_code == 200

    def test_prioritized_forbids_non_owner(self, test_client, sample_user):
        create_resp = test_client.post(
            "/api/v1/users/register",
            json={
                "display_name": "Other User",
                "email": "other-user@test.com",
                "password": "OtherUser123!",
            },
        )
        assert create_resp.status_code == 200

        _login(test_client, "other-user@test.com", "OtherUser123!")
        resp = test_client.get(f"/api/v1/alerts/prioritized/{sample_user.id}")
        assert resp.status_code == 403

    def test_prioritized_allows_admin_for_other_user(self, test_client, sample_user, admin_user):
        _ = sample_user
        _ = admin_user
        _login(test_client, "admin@example.com")
        resp = test_client.get(f"/api/v1/alerts/prioritized/{sample_user.id}")
        assert resp.status_code == 200
