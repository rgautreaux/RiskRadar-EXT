"""Tests for user API endpoints."""

import json

from backend.auth.security import decrypt_email, hash_email, verify_password


def _login(test_client, email: str, password: str = "password123"):
    resp = test_client.post(
        "/api/v1/auth/login",
        json={"email": email, "password": password},
    )
    assert resp.status_code == 200



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
        from backend.db.models import User

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
        from backend.db.models import User

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
        _ = sample_user
        resp = test_client.post("/api/v1/users/register", json={
            "display_name": "Duplicate",
            "email": "test@example.com",
            "password": "Duplicate123!Aa",
        })
        assert resp.status_code == 400
        assert "Email already registered" in resp.json()["detail"]

    def test_register_creates_default_alert_preference(self, test_client, db_session):
        from backend.db.models import User, UserAlertPreference

        resp = test_client.post("/api/v1/users/register", json={
            "display_name": "DefaultPref",
            "email": "defaultpref@test.com",
            "password": "DefaultPref123!",
        })
        assert resp.status_code == 200

        user = db_session.query(User).filter(User.email_lookup_hash == hash_email("defaultpref@test.com")).first()
        assert user is not None
        rows = db_session.query(UserAlertPreference).filter(UserAlertPreference.user_id == user.id).all()
        assert len(rows) == 1
        assert rows[0].alert_type == "all"


class TestUpdatePreferences:
    def test_update_zip_code(self, test_client, sample_user):
        _login(test_client, "test@example.com")
        resp = test_client.put(f"/api/v1/users/{sample_user.id}/preferences", json={
            "zip_code": "10001",
        })
        assert resp.status_code == 200
        assert resp.json()["zip_code"] == "10001"

    def test_update_alert_types(self, test_client, db_session, sample_user):
        from backend.db.models import UserAlertPreference

        _login(test_client, "test@example.com")
        resp = test_client.put(f"/api/v1/users/{sample_user.id}/preferences", json={
            "alert_types": ["weather", "earthquake"],
        })
        assert resp.status_code == 200
        rows = (
            db_session.query(UserAlertPreference)
            .filter(UserAlertPreference.user_id == sample_user.id)
            .order_by(UserAlertPreference.alert_type.asc())
            .all()
        )
        assert [row.alert_type for row in rows] == ["earthquake", "weather"]

    def test_alert_types_fallbacks_to_relational_rows_when_json_missing(self, test_client, db_session, sample_user):
        from backend.db.models import UserAlertPreference

        db_session.query(UserAlertPreference).filter(UserAlertPreference.user_id == sample_user.id).delete()
        db_session.add(UserAlertPreference(user_id=sample_user.id, alert_type="wildfire"))
        sample_user.alert_types = None
        db_session.commit()

        _login(test_client, "test@example.com")
        resp = test_client.put(f"/api/v1/users/{sample_user.id}/preferences", json={"zip_code": "90002"})
        assert resp.status_code == 200
        alert_types = json.loads(resp.json()["alert_types"])
        assert alert_types == ["wildfire"]

    def test_health_conditions_fallbacks_to_relational_rows_when_json_missing(self, test_client, db_session, sample_user):
        from backend.db.models import UserHealthCondition

        db_session.query(UserHealthCondition).filter(UserHealthCondition.user_id == sample_user.id).delete()
        db_session.add(UserHealthCondition(user_id=sample_user.id, condition_key="respiratory"))
        sample_user.health_conditions = None
        db_session.commit()

        _login(test_client, "test@example.com")
        resp = test_client.put(f"/api/v1/users/{sample_user.id}/preferences", json={"zip_code": "90003"})
        assert resp.status_code == 200
        conditions = json.loads(resp.json()["health_conditions"])
        assert conditions == ["respiratory"]

    def test_update_not_found(self, test_client, admin_user):
        _ = admin_user
        _login(test_client, "admin@example.com")
        resp = test_client.put("/api/v1/users/9999/preferences", json={
            "zip_code": "00000",
        })
        assert resp.status_code == 404

    def test_update_assistant_style_profile(self, test_client, sample_user):
        _login(test_client, "test@example.com")
        resp = test_client.put(f"/api/v1/users/{sample_user.id}/preferences", json={
            "assistant_style_profile": {
                "tone": {
                    "warmth": 0.82,
                    "calmness": 0.8,
                    "humor": 0.5
                },
                "delivery": {
                    "conciseness": 0.72,
                    "detail": 0.55,
                    "expandability": 0.6
                },
                "voice": {
                    "formality": 0.32
                },
                "learning": {
                    "feedback_count": 2,
                    "last_feedback_at": None
                }
            },
        })
        assert resp.status_code == 200
        assert '"warmth": 0.82' in resp.json()["assistant_style_profile"]

    def test_update_preferences_requires_authentication(self, test_client, sample_user):
        resp = test_client.put(
            f"/api/v1/users/{sample_user.id}/preferences",
            json={"zip_code": "94105"},
        )
        assert resp.status_code == 401

    def test_update_preferences_forbids_non_owner(self, test_client, sample_user):
        create_resp = test_client.post(
            "/api/v1/users/register",
            json={
                "display_name": "Other User",
                "email": "other-pref@test.com",
                "password": "OtherUser123!",
            },
        )
        assert create_resp.status_code == 200

        _login(test_client, "other-pref@test.com", "OtherUser123!")
        resp = test_client.put(
            f"/api/v1/users/{sample_user.id}/preferences",
            json={"zip_code": "10002"},
        )
        assert resp.status_code == 403

    def test_update_preferences_allows_admin_for_other_user(self, test_client, sample_user, admin_user):
        _ = sample_user
        _ = admin_user
        _login(test_client, "admin@example.com")
        resp = test_client.put(
            f"/api/v1/users/{sample_user.id}/preferences",
            json={"zip_code": "10003"},
        )
        assert resp.status_code == 200
