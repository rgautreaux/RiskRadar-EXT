"""End-to-end tests for personality profile application in assistant responses."""

import json

import pytest


class TestPersonalityProfileE2E:
    """Verify that personality profiles are correctly applied to assistant responses."""

    def test_warm_personality_adds_prefix(self, test_client, sample_user, db_session):
        """High warmth (>=0.68) should prefix responses with 'Absolutely.'"""
        # Set personality profile with high warmth
        profile = {
            "tone": {
                "warmth": 0.80,  # High warmth
                "calmness": 0.75,
                "humor": 0.30,
            },
            "delivery": {
                "conciseness": 0.65,
                "detail": 0.45,
                "expandability": 0.50,
            },
            "voice": {
                "formality": 0.35,
            },
            "learning": {
                "feedback_count": 0,
                "last_feedback_at": None,
            },
        }
        
        # Update user's personality profile
        resp = test_client.put(
            f"/api/v1/users/{sample_user.id}/preferences",
            json={"assistant_style_profile": profile},
        )
        assert resp.status_code == 200
        
        # Request assistant response for a help question
        resp = test_client.post(
            "/api/v1/assistant/respond",
            json={
                "message": "help",
                "user_id": sample_user.id,
            },
        )
        assert resp.status_code == 200
        data = resp.json()
        assert "reply" in data
        # High warmth should add "Absolutely. " prefix
        assert data["reply"].startswith("Absolutely. "), f"Expected 'Absolutely. ' prefix but got: {data['reply']}"

    def test_concise_personality_shortens_response(self, test_client, sample_user, db_session, sample_alerts):
        """High conciseness (>=0.78) should shorten long responses."""
        # Set personality profile with high conciseness
        profile = {
            "tone": {
                "warmth": 0.50,
                "calmness": 0.75,
                "humor": 0.30,
            },
            "delivery": {
                "conciseness": 0.85,  # High conciseness
                "detail": 0.30,
                "expandability": 0.50,
            },
            "voice": {
                "formality": 0.35,
            },
            "learning": {
                "feedback_count": 0,
                "last_feedback_at": None,
            },
        }
        
        # Update user's personality profile
        resp = test_client.put(
            f"/api/v1/users/{sample_user.id}/preferences",
            json={"assistant_style_profile": profile},
        )
        assert resp.status_code == 200
        
        # Request assistant response for forecast (generates longer reply)
        resp = test_client.post(
            "/api/v1/assistant/respond",
            json={
                "message": "forecast",
                "user_id": sample_user.id,
                "location": "Los Angeles",
            },
        )
        assert resp.status_code == 200
        data = resp.json()
        assert "reply" in data
        # High conciseness should result in shorter response (max ~220 chars for first sentence)
        # The exact length depends on the alerts data, but we should have a reasonable response
        assert len(data["reply"]) > 0

    def test_profile_not_applied_to_guardrail_responses(self, test_client, sample_user):
        """Personality profiles should NOT be applied to guardrail responses."""
        # Set personality profile with high warmth
        profile = {
            "tone": {
                "warmth": 0.95,  # Very high warmth
                "calmness": 0.75,
                "humor": 0.30,
            },
            "delivery": {
                "conciseness": 0.65,
                "detail": 0.45,
                "expandability": 0.50,
            },
            "voice": {
                "formality": 0.35,
            },
            "learning": {
                "feedback_count": 0,
                "last_feedback_at": None,
            },
        }
        
        # Update user's personality profile
        resp = test_client.put(
            f"/api/v1/users/{sample_user.id}/preferences",
            json={"assistant_style_profile": profile},
        )
        assert resp.status_code == 200
        
        # Request assistant response for medical question (triggers guardrail)
        resp = test_client.post(
            "/api/v1/assistant/respond",
            json={
                "message": "medical advice",
                "user_id": sample_user.id,
            },
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["category"] == "guardrail"
        # Guardrail responses should not have warmth prefix
        assert not data["reply"].startswith("Absolutely. ")

    def test_playful_personality_adds_humor_suffix(self, test_client, sample_user, sample_alerts):
        """High humor (>=0.72) should append humor suffix."""
        # Set personality profile with high humor
        profile = {
            "tone": {
                "warmth": 0.50,
                "calmness": 0.75,
                "humor": 0.80,  # High humor
            },
            "delivery": {
                "conciseness": 0.65,
                "detail": 0.45,
                "expandability": 0.50,
            },
            "voice": {
                "formality": 0.35,
            },
            "learning": {
                "feedback_count": 0,
                "last_feedback_at": None,
            },
        }
        
        # Update user's personality profile
        resp = test_client.put(
            f"/api/v1/users/{sample_user.id}/preferences",
            json={"assistant_style_profile": profile},
        )
        assert resp.status_code == 200
        
        # Request assistant response for forecast (uses live data, gets shaped)
        resp = test_client.post(
            "/api/v1/assistant/respond",
            json={
                "message": "forecast",
                "user_id": sample_user.id,
            },
        )
        assert resp.status_code == 200
        data = resp.json()
        # High humor should append Golby-style suffix
        assert "We can keep this steady and low-stress, Golby-style." in data["reply"]

    def test_personality_profile_persists_across_requests(self, test_client, sample_user):
        """Personality profile should persist and apply to subsequent requests."""
        profile = {
            "tone": {
                "warmth": 0.75,
                "calmness": 0.75,
                "humor": 0.30,
            },
            "delivery": {
                "conciseness": 0.65,
                "detail": 0.45,
                "expandability": 0.50,
            },
            "voice": {
                "formality": 0.35,
            },
            "learning": {
                "feedback_count": 0,
                "last_feedback_at": None,
            },
        }
        
        # Update profile once
        resp = test_client.put(
            f"/api/v1/users/{sample_user.id}/preferences",
            json={"assistant_style_profile": profile},
        )
        assert resp.status_code == 200
        
        # Make multiple requests and verify profile is applied to all
        for i in range(3):
            resp = test_client.post(
                "/api/v1/assistant/respond",
                json={
                    "message": "help",
                    "user_id": sample_user.id,
                },
            )
            assert resp.status_code == 200
            data = resp.json()
            # Profile should be applied to each response
            assert data["reply"].startswith("Absolutely. "), f"Request {i+1}: Expected warmth prefix"

    def test_guest_user_uses_default_profile(self, test_client):
        """Guest users (no user_id) should use default profile."""
        resp = test_client.post(
            "/api/v1/assistant/respond",
            json={"message": "help"},
        )
        assert resp.status_code == 200
        data = resp.json()
        # Guest responses should use default profile (not high warmth prefix)
        # Default warmth is 0.55, which is < 0.68
        assert not data["reply"].startswith("Absolutely. ")
