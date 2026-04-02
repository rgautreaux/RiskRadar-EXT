"""Tests for user API endpoints."""

from auth.security import decrypt_email, hash_email, verify_password



class TestRegisterUser:
    def test_register_success(self, test_client):
        resp = test_client.post("/api/v1/users/register", json={
            "display_name": "Alice",
            "email": "alice@test.com",
            "password": "Secret123!Aa",
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
            "password": "BobSecure123!",
            "zip_code": "90210",
        })
        assert resp.status_code == 200
        assert resp.json()["zip_code"] == "90210"

    def test_register_rejects_weak_password(self, test_client):
        resp = test_client.post("/api/v1/users/register", json={
            "display_name": "Weak",
            "email": "weak@test.com",
            "password": "pass",
        })
        assert resp.status_code == 400
        assert "Password must be at least" in resp.json()["detail"]

    def test_password_is_hashed(self, test_client, db_session):
        from db.models import User

        test_client.post("/api/v1/users/register", json={
            "display_name": "Carol",
            "email": "carol@test.com",
            "password": "CarolPass123!",
        })
        user = db_session.query(User).filter(User.email_lookup_hash == hash_email("carol@test.com")).first()
        assert user is not None
        assert verify_password("CarolPass123!", user.password_hash)
        assert decrypt_email(user.email) == "carol@test.com"

    def test_email_normalized_to_lowercase(self, test_client, db_session):
        from db.models import User

        resp = test_client.post("/api/v1/users/register", json={
            "display_name": "Dave",
            "email": "Dave@Test.COM",
            "password": "DavePass123!",
        })
        assert resp.status_code == 200
        assert resp.json()["email"] == "dave@test.com"
        user = db_session.query(User).filter(User.email_lookup_hash == hash_email("dave@test.com")).first()
        assert user is not None
        assert decrypt_email(user.email) == "dave@test.com"

    def test_duplicate_email_case_insensitive(self, test_client):
        test_client.post("/api/v1/users/register", json={
            "display_name": "Eve",
            "email": "eve@test.com",
            "password": "EvePass123!Aa",
        })
        resp = test_client.post("/api/v1/users/register", json={
            "display_name": "Eve2",
            "email": "EVE@TEST.COM",
            "password": "EvePass456!Bb",
        })
        assert resp.status_code == 400
        assert "Email already registered" in resp.json()["detail"]

    def test_duplicate_email_rejected(self, test_client, sample_user):
        resp = test_client.post("/api/v1/users/register", json={
            "display_name": "Duplicate",
            "email": "test@example.com",
            "password": "Duplicate123!Aa",
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
