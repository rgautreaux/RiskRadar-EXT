"""Tests for user API endpoints."""

from passlib.context import CryptContext

_pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


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
        assert user is not None
        assert _pwd_context.verify("mypassword", user.password_hash)

    def test_email_normalized_to_lowercase(self, test_client, db_session):
        from db.models import User

        resp = test_client.post("/api/v1/users/register", json={
            "display_name": "Dave",
            "email": "Dave@Test.COM",
            "password": "pass",
        })
        assert resp.status_code == 200
        assert resp.json()["email"] == "dave@test.com"
        user = db_session.query(User).filter(User.email == "dave@test.com").first()
        assert user is not None

    def test_duplicate_email_case_insensitive(self, test_client):
        test_client.post("/api/v1/users/register", json={
            "display_name": "Eve",
            "email": "eve@test.com",
            "password": "pass",
        })
        resp = test_client.post("/api/v1/users/register", json={
            "display_name": "Eve2",
            "email": "EVE@TEST.COM",
            "password": "pass",
        })
        assert resp.status_code == 400
        assert "Email already registered" in resp.json()["detail"]

    def test_duplicate_email_rejected(self, test_client, sample_user):
        resp = test_client.post("/api/v1/users/register", json={
            "display_name": "Duplicate",
            "email": "test@example.com",
            "password": "pass",
        })
        assert resp.status_code == 400
        assert "Email already registered" in resp.json()["detail"]


class TestUpdatePreferences:
    def test_update_zip_code(self, test_client, sample_user):
        resp = test_client.put(f"/api/v1/users/{sample_user.id}/preferences", json={
            "zip_code": "10001",
        })
        assert resp.status_code == 200
        assert resp.json()["zip_code"] == "10001"

    def test_update_alert_types(self, test_client, sample_user):
        resp = test_client.put(f"/api/v1/users/{sample_user.id}/preferences", json={
            "alert_types": ["weather", "earthquake"],
        })
        assert resp.status_code == 200

    def test_update_not_found(self, test_client):
        resp = test_client.put("/api/v1/users/9999/preferences", json={
            "zip_code": "00000",
        })
        assert resp.status_code == 404
