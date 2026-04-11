"""Tests for user API endpoints."""

from auth.security import create_access_token, verify_password
from db.models import User


def _auth_headers(user_id: int) -> dict[str, str]:
    token = create_access_token(data={"sub": str(user_id)})
    return {"Authorization": f"Bearer {token}"}


class TestRegisterUser:
    def test_register_success(self, test_client):
        resp = test_client.post("/api/v1/users/register", json={
            "display_name": "Alice",
            "email": "alice@test.com",
            "password": "secret123",
        })
        assert resp.status_code == 200
        data = resp.json()
        assert data["display_name"] == "Alice"
        assert data["email"] == "alice@test.com"
        assert "password" not in data
        assert "password_hash" not in data

    def test_register_with_zip(self, test_client):
        resp = test_client.post("/api/v1/users/register", json={
            "display_name": "Bob",
            "email": "bob@test.com",
            "password": "pass",
            "zip_code": "90210",
        })
        assert resp.status_code == 200
        assert resp.json()["zip_code"] == "90210"

    def test_password_is_hashed(self, test_client, db_session):
        from db.models import User

        test_client.post("/api/v1/users/register", json={
            "display_name": "Carol",
            "email": "carol@test.com",
            "password": "mypassword",
        })
        user = db_session.query(User).filter(User.email == "carol@test.com").first()
        assert user.password_hash != "mypassword"
        assert verify_password("mypassword", user.password_hash)

    def test_duplicate_email_rejected(self, test_client, sample_user):
        resp = test_client.post("/api/v1/users/register", json={
            "display_name": "Duplicate",
            "email": "test@example.com",
            "password": "pass",
        })
        assert resp.status_code == 400
        assert "Email already registered" in resp.json()["detail"]

    def test_register_invalid_email_rejected(self, test_client):
        resp = test_client.post("/api/v1/users/register", json={
            "display_name": "Bad Email",
            "email": "not-an-email",
            "password": "secret123",
        })
        assert resp.status_code == 422

    def test_register_invalid_zip_rejected(self, test_client):
        resp = test_client.post("/api/v1/users/register", json={
            "display_name": "Bad Zip",
            "email": "zip@test.com",
            "password": "secret123",
            "zip_code": "12AB",
        })
        assert resp.status_code == 422


class TestLoginUser:
    def test_login_success(self, test_client, sample_user):
        resp = test_client.post("/api/v1/users/login", json={
            "email": "test@example.com",
            "password": "password123",
        })
        assert resp.status_code == 200
        data = resp.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    def test_login_invalid_password_rejected(self, test_client, sample_user):
        resp = test_client.post("/api/v1/users/login", json={
            "email": "test@example.com",
            "password": "wrong-password",
        })
        assert resp.status_code == 401
        assert "Invalid email or password" in resp.json()["detail"]

    def test_login_unknown_email_rejected(self, test_client):
        resp = test_client.post("/api/v1/users/login", json={
            "email": "missing@example.com",
            "password": "password123",
        })
        assert resp.status_code == 401


class TestCurrentUserAndNotifications:
    def test_me_requires_auth(self, test_client):
        resp = test_client.get("/api/v1/users/me")
        assert resp.status_code == 401

    def test_me_returns_current_user(self, test_client, sample_user):
        resp = test_client.get("/api/v1/users/me", headers=_auth_headers(sample_user.id))
        assert resp.status_code == 200
        data = resp.json()
        assert data["email"] == "test@example.com"
        assert data["display_name"] == "Test User"

    def test_get_preferences_requires_own_user(self, test_client, sample_user):
        resp = test_client.get(f"/api/v1/users/{sample_user.id}/preferences", headers=_auth_headers(sample_user.id))
        assert resp.status_code == 200
        assert resp.json()["email"] == "test@example.com"

    def test_get_preferences_for_other_user_forbidden(self, test_client, sample_user):
        resp = test_client.get("/api/v1/users/9999/preferences", headers=_auth_headers(sample_user.id))
        assert resp.status_code == 403

    def test_get_notifications_returns_settings(self, test_client, sample_user):
        resp = test_client.get("/api/v1/users/notifications", headers=_auth_headers(sample_user.id))
        assert resp.status_code == 200
        data = resp.json()
        assert data["notify_severity"] == "high"
        assert data["device_token"] is None

    def test_update_notifications(self, test_client, sample_user, db_session):
        resp = test_client.put(
            "/api/v1/users/notifications",
            json={"notify_severity": "critical", "device_token": "device-123"},
            headers=_auth_headers(sample_user.id),
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["notify_severity"] == "critical"
        assert data["device_token"] == "device-123"

        user = db_session.query(User).filter(User.id == sample_user.id).first()
        assert user.notify_severity == "critical"
        assert user.device_token == "device-123"


class TestUpdatePreferences:
    def test_update_zip_code(self, test_client, sample_user):
        resp = test_client.put(f"/api/v1/users/{sample_user.id}/preferences", json={
            "zip_code": "10001",
        }, headers=_auth_headers(sample_user.id))
        assert resp.status_code == 200
        assert resp.json()["zip_code"] == "10001"

    def test_update_alert_types(self, test_client, sample_user):
        resp = test_client.put(f"/api/v1/users/{sample_user.id}/preferences", json={
            "alert_types": ["weather", "earthquake"],
        }, headers=_auth_headers(sample_user.id))
        assert resp.status_code == 200

    def test_update_forbidden_for_other_user(self, test_client, sample_user):
        resp = test_client.put("/api/v1/users/9999/preferences", json={
            "zip_code": "00000",
        }, headers=_auth_headers(sample_user.id))
        assert resp.status_code == 403

    def test_update_invalid_notify_severity_rejected(self, test_client, sample_user):
        resp = test_client.put(
            f"/api/v1/users/{sample_user.id}/preferences",
            json={"notify_severity": "urgent"},
            headers=_auth_headers(sample_user.id),
        )
        assert resp.status_code == 422

    def test_update_invalid_alert_types_rejected(self, test_client, sample_user):
        resp = test_client.put(
            f"/api/v1/users/{sample_user.id}/preferences",
            json={"alert_types": ["weather", "bad_type"]},
            headers=_auth_headers(sample_user.id),
        )
        assert resp.status_code == 422


class TestDeviceTokenManagement:
    def test_register_device_token(self, test_client, sample_user, db_session):
        resp = test_client.post(
            f"/api/v1/users/{sample_user.id}/device-token",
            json={"device_token": "ExponentPushToken[abc123]"},
            headers=_auth_headers(sample_user.id),
        )
        assert resp.status_code == 200
        assert resp.json()["device_token"] == "ExponentPushToken[abc123]"

        user = db_session.query(User).filter(User.id == sample_user.id).first()
        assert user.device_token == "ExponentPushToken[abc123]"

    def test_register_blank_device_token_rejected(self, test_client, sample_user):
        resp = test_client.post(
            f"/api/v1/users/{sample_user.id}/device-token",
            json={"device_token": "   "},
            headers=_auth_headers(sample_user.id),
        )
        assert resp.status_code == 422

    def test_revoke_device_token(self, test_client, sample_user, db_session):
        sample_user.device_token = "ExponentPushToken[seed]"
        db_session.commit()

        resp = test_client.post(
            f"/api/v1/users/{sample_user.id}/device-token/revoke",
            headers=_auth_headers(sample_user.id),
        )
        assert resp.status_code == 200
        assert resp.json()["device_token"] is None

        user = db_session.query(User).filter(User.id == sample_user.id).first()
        assert user.device_token is None

    def test_register_device_token_other_user_forbidden(self, test_client, sample_user):
        resp = test_client.post(
            "/api/v1/users/9999/device-token",
            json={"device_token": "ExponentPushToken[abc123]"},
            headers=_auth_headers(sample_user.id),
        )
        assert resp.status_code == 403
