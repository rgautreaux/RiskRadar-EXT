"""Tests for the trip packing guide API endpoint."""

from unittest.mock import patch


class TestPackingGuide:
    BASE_URL = "/api/v1/packing/guide"

    VALID_BODY = {
        "city": "Austin",
        "state": "TX",
        "zip_code": "78701",
        "trip_date": "2026-06-01",
    }

    # ------------------------------------------------------------------
    # is_personalized: unauthenticated vs authenticated
    # ------------------------------------------------------------------

    def test_unauthenticated_is_not_personalized(self, test_client):
        """Unauthenticated requests produce is_personalized=False."""
        mock_return = ("# Packing Guide\nBring sunscreen.", "guest-model")
        with patch(
            "llm.summarizer.Summarizer.generate_trip_packing_guide",
            return_value=mock_return,
        ):
            resp = test_client.post(self.BASE_URL, json=self.VALID_BODY)
        assert resp.status_code == 200
        data = resp.json()
        assert data["is_personalized"] is False

    def test_authenticated_is_personalized(self, test_client, sample_user):
        """Authenticated users receive is_personalized=True."""
        test_client.post(
            "/api/v1/auth/login",
            json={"email": "test@example.com", "password": "password123"},
        )
        mock_return = ("# Premium Packing Guide\nBring everything.", "premium-model")
        with patch(
            "llm.summarizer.Summarizer.generate_trip_packing_guide",
            return_value=mock_return,
        ):
            resp = test_client.post(self.BASE_URL, json=self.VALID_BODY)
        # Logout so subsequent tests start unauthenticated
        test_client.post("/api/v1/auth/logout")
        assert resp.status_code == 200
        data = resp.json()
        assert data["is_personalized"] is True

    # ------------------------------------------------------------------
    # model_used is always returned
    # ------------------------------------------------------------------

    def test_model_used_is_returned(self, test_client):
        """Response always contains the model_used field."""
        mock_return = ("Some guide content.", "test-model")
        with patch(
            "llm.summarizer.Summarizer.generate_trip_packing_guide",
            return_value=mock_return,
        ):
            resp = test_client.post(self.BASE_URL, json=self.VALID_BODY)
        assert resp.status_code == 200
        data = resp.json()
        assert "model_used" in data
        assert data["model_used"] == "test-model"

    def test_fallback_model_used_on_llm_error(self, test_client):
        """When the LLM is unavailable the fallback model label is returned."""
        mock_return = ("Fallback guide content.", "fallback")
        with patch(
            "llm.summarizer.Summarizer.generate_trip_packing_guide",
            return_value=mock_return,
        ):
            resp = test_client.post(self.BASE_URL, json=self.VALID_BODY)
        assert resp.status_code == 200
        assert resp.json()["model_used"] == "fallback"

    # ------------------------------------------------------------------
    # Request validation
    # ------------------------------------------------------------------

    def test_missing_city_returns_422(self, test_client):
        """A request without city is invalid."""
        resp = test_client.post(
            self.BASE_URL, json={"state": "TX", "zip_code": "78701"}
        )
        assert resp.status_code == 422

    def test_missing_state_returns_422(self, test_client):
        """A request without state is invalid."""
        resp = test_client.post(
            self.BASE_URL, json={"city": "Austin", "zip_code": "78701"}
        )
        assert resp.status_code == 422

    def test_missing_zip_code_returns_422(self, test_client):
        """A request without zip_code is invalid."""
        resp = test_client.post(
            self.BASE_URL, json={"city": "Austin", "state": "TX"}
        )
        assert resp.status_code == 422

    def test_empty_body_returns_422(self, test_client):
        """An empty body returns a validation error."""
        resp = test_client.post(self.BASE_URL, json={})
        assert resp.status_code == 422

    # ------------------------------------------------------------------
    # Optional trip_date defaults to today
    # ------------------------------------------------------------------

    def test_trip_date_optional_defaults_to_today(self, test_client):
        """trip_date is optional; when omitted it defaults to today's date."""
        from datetime import date

        body = {"city": "Austin", "state": "TX", "zip_code": "78701"}
        mock_return = ("Guide content.", "test-model")
        with patch(
            "llm.summarizer.Summarizer.generate_trip_packing_guide",
            return_value=mock_return,
        ):
            resp = test_client.post(self.BASE_URL, json=body)
        assert resp.status_code == 200
        data = resp.json()
        assert data["trip_date"] == date.today().isoformat()

    # ------------------------------------------------------------------
    # Full response shape
    # ------------------------------------------------------------------

    def test_response_contains_all_expected_fields(self, test_client):
        """Response contains every field declared in PackingGuideResponse."""
        mock_return = ("Packing guide text.", "some-model")
        with patch(
            "llm.summarizer.Summarizer.generate_trip_packing_guide",
            return_value=mock_return,
        ):
            resp = test_client.post(self.BASE_URL, json=self.VALID_BODY)
        assert resp.status_code == 200
        data = resp.json()
        expected_keys = {
            "guide",
            "city",
            "state",
            "zip_code",
            "trip_date",
            "alert_count",
            "model_used",
            "is_personalized",
        }
        assert expected_keys.issubset(data.keys())
        assert data["city"] == "Austin"
        assert data["state"] == "TX"
        assert data["zip_code"] == "78701"
        assert data["trip_date"] == "2026-06-01"
        assert isinstance(data["alert_count"], int)
        assert data["guide"] == "Packing guide text."
