"""Tests for risk API authentication and authorization."""


def _login(test_client, email: str, password: str = "password123"):
    resp = test_client.post(
        "/api/v1/auth/login",
        json={"email": email, "password": password},
    )
    assert resp.status_code == 200


class TestRiskEndpointAuth:
    def test_risk_score_requires_authentication(self, test_client, sample_user):
        resp = test_client.get(f"/api/v1/risk/score/{sample_user.id}")
        assert resp.status_code == 401

    def test_risk_score_allows_owner(self, test_client, sample_user):
        _login(test_client, "test@example.com")
        resp = test_client.get(f"/api/v1/risk/score/{sample_user.id}")
        assert resp.status_code == 200
        assert resp.json()["user_id"] == sample_user.id

    def test_risk_score_forbids_non_owner(self, test_client, sample_user):
        create_resp = test_client.post(
            "/api/v1/users/register",
            json={
                "display_name": "Other User",
                "email": "other-risk@test.com",
                "password": "OtherUser123!",
            },
        )
        assert create_resp.status_code == 200

        _login(test_client, "other-risk@test.com", "OtherUser123!")
        resp = test_client.get(f"/api/v1/risk/score/{sample_user.id}")
        assert resp.status_code == 403

    def test_risk_score_allows_admin_for_other_user(self, test_client, sample_user, admin_user):
        _ = admin_user
        _login(test_client, "admin@example.com")
        resp = test_client.get(f"/api/v1/risk/score/{sample_user.id}")
        assert resp.status_code == 200

    def test_personalized_map_requires_authentication(self, test_client, sample_user):
        resp = test_client.get(f"/api/v1/risk/map/personalized/{sample_user.id}")
        assert resp.status_code == 401

    def test_personalized_map_allows_owner(self, test_client, sample_user):
        _login(test_client, "test@example.com")
        resp = test_client.get(f"/api/v1/risk/map/personalized/{sample_user.id}")
        assert resp.status_code == 200
        assert "risk_zones" in resp.json()

    def test_personalized_map_forbids_non_owner(self, test_client, sample_user):
        create_resp = test_client.post(
            "/api/v1/users/register",
            json={
                "display_name": "Other User",
                "email": "other-risk-map@test.com",
                "password": "OtherUser123!",
            },
        )
        assert create_resp.status_code == 200

        _login(test_client, "other-risk-map@test.com", "OtherUser123!")
        resp = test_client.get(f"/api/v1/risk/map/personalized/{sample_user.id}")
        assert resp.status_code == 403

    def test_personalized_map_allows_admin_for_other_user(self, test_client, sample_user, admin_user):
        _ = admin_user
        _login(test_client, "admin@example.com")
        resp = test_client.get(f"/api/v1/risk/map/personalized/{sample_user.id}")
        assert resp.status_code == 200
