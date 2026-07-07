"""Tests for authentication session endpoints."""


class TestAuthSession:
    def test_login_returns_session_and_me(self, test_client, admin_user):
        _ = admin_user
        login_resp = test_client.post(
            "/api/v1/auth/login",
            json={"email": "admin@example.com", "password": "password123"},
        )
        assert login_resp.status_code == 200
        data = login_resp.json()
        assert data["session_token"]
        assert data["user"]["is_admin"] is True

        me_resp = test_client.get("/api/v1/auth/me")
        assert me_resp.status_code == 200
        me_data = me_resp.json()
        assert me_data["id"] == admin_user.id
        assert me_data["is_admin"] is True

    def test_login_rejects_bad_password(self, test_client, admin_user):
        _ = admin_user
        resp = test_client.post(
            "/api/v1/auth/login",
            json={"email": "admin@example.com", "password": "wrong-password"},
        )
        assert resp.status_code == 401

    def test_logout_clears_session(self, test_client, admin_user):
        _ = admin_user
        login_resp = test_client.post(
            "/api/v1/auth/login",
            json={"email": "admin@example.com", "password": "password123"},
        )
        assert login_resp.status_code == 200

        logout_resp = test_client.post("/api/v1/auth/logout")
        assert logout_resp.status_code == 200

        me_resp = test_client.get("/api/v1/auth/me")
        assert me_resp.status_code == 401
