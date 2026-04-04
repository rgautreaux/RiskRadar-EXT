"""Tests for summary API endpoints."""

import json
from unittest.mock import patch, MagicMock

from db.models import Summary


class TestListSummaries:
    def test_list_all(self, test_client, sample_summary):
        resp = test_client.get("/api/v1/summaries")
        assert resp.status_code == 200
        data = resp.json()
        assert len(data) == 1
        assert data[0]["summary_type"] == "daily"

    def test_filter_by_type(self, test_client, sample_summary):
        resp = test_client.get("/api/v1/summaries?summary_type=daily")
        data = resp.json()
        assert len(data) == 1

    def test_filter_no_match(self, test_client, sample_summary):
        resp = test_client.get("/api/v1/summaries?summary_type=breaking")
        data = resp.json()
        assert len(data) == 0

    def test_empty_database(self, test_client):
        resp = test_client.get("/api/v1/summaries")
        assert resp.status_code == 200
        assert resp.json() == []


class TestLatestSummary:
    def test_returns_latest(self, test_client, sample_summary):
        resp = test_client.get("/api/v1/summaries/latest")
        assert resp.status_code == 200
        data = resp.json()
        assert data["title"] == sample_summary.title

    def test_returns_null_when_empty(self, test_client):
        resp = test_client.get("/api/v1/summaries/latest")
        assert resp.status_code == 200
        assert resp.json() is None


class TestLatestLocalSummary:
    def test_returns_latest_local(self, test_client, db_session, sample_alerts):
        local_summary = Summary(
            title="Local Digest for Los Angeles, CA — Mar 27, 2026",
            content="## Executive Summary\nLocal alerts for LA.",
            summary_type="local",
            alert_ids=json.dumps([sample_alerts[0].id]),
            region="Los Angeles, CA 90001",
            model_used="openai/gpt-5.2",
            token_count=80,
        )
        db_session.add(local_summary)
        db_session.commit()
        db_session.refresh(local_summary)

        resp = test_client.get("/api/v1/summaries/latest/local?zip_code=90001")
        assert resp.status_code == 200
        data = resp.json()
        assert data["summary_type"] == "local"
        assert "Los Angeles" in data["title"]

    def test_returns_null_when_no_local(self, test_client):
        resp = test_client.get("/api/v1/summaries/latest/local?zip_code=90001")
        assert resp.status_code == 200
        assert resp.json() is None

    def test_rejects_invalid_zip(self, test_client):
        resp = test_client.get("/api/v1/summaries/latest/local?zip_code=abc")
        assert resp.status_code == 422


class TestGenerateSummary:
    def test_generate_with_alerts(self, test_client, sample_alerts):
        mock_return = ("## Daily Digest\nTest summary content.", 100, "openai/gpt-5.2")
        with patch("llm.summarizer.Summarizer._call_llm", return_value=mock_return):
            resp = test_client.post("/api/v1/summaries/generate")
        assert resp.status_code == 200
        data = resp.json()
        assert "Daily Digest" in data["content"]
        assert data["summary_type"] == "daily"

    def test_generate_no_alerts(self, test_client):
        resp = test_client.post("/api/v1/summaries/generate")
        assert resp.status_code == 404


class TestGenerateLocalSummary:
    def test_generate_local_with_alerts(self, test_client, sample_alerts):
        mock_location = (34.05, -118.24, "Los Angeles", "CA")
        mock_nws = [
            {
                "source": "nws",
                "source_id": "nws_local_001",
                "alert_type": "weather",
                "severity": "high",
                "title": "Heat Advisory",
                "description": "Excessive heat expected.",
                "latitude": 34.05,
                "longitude": -118.24,
                "location_name": "Los Angeles, CA",
            }
        ]
        mock_llm_return = ("## Local Digest\nHeat advisory for Los Angeles.", 75, "openai/gpt-5.2")

        with (
            patch("api.location._zip_to_coords", return_value=mock_location),
            patch("api.location._fetch_nws_alerts", return_value=mock_nws),
            patch("api.location._fetch_airnow", return_value=[]),
            patch("llm.summarizer.Summarizer._call_llm", return_value=mock_llm_return),
        ):
            resp = test_client.post("/api/v1/summaries/generate/local?zip_code=90001")

        assert resp.status_code == 200
        data = resp.json()
        assert data["summary_type"] == "local"
        assert "Los Angeles" in data["title"]
        assert "Local Digest" in data["content"]

    def test_generate_local_invalid_zip(self, test_client):
        with patch("api.location._zip_to_coords", return_value=None):
            resp = test_client.post("/api/v1/summaries/generate/local?zip_code=00000")
        assert resp.status_code == 404

    def test_generate_local_no_alerts(self, test_client):
        mock_location = (34.05, -118.24, "Los Angeles", "CA")
        with (
            patch("api.location._zip_to_coords", return_value=mock_location),
            patch("api.location._fetch_nws_alerts", return_value=[]),
            patch("api.location._fetch_airnow", return_value=[]),
        ):
            resp = test_client.post("/api/v1/summaries/generate/local?zip_code=90001")
        assert resp.status_code == 404


class TestCallLlm:
    def test_call_llm_returns_text_and_tokens(self):
        from llm.summarizer import Summarizer

        mock_message = MagicMock()
        mock_message.content = "Test response"
        mock_choice = MagicMock()
        mock_choice.message = mock_message
        mock_usage = MagicMock()
        mock_usage.total_tokens = 42
        mock_completion = MagicMock()
        mock_completion.choices = [mock_choice]
        mock_completion.usage = mock_usage

        with (
            patch("config.settings.settings.OPENROUTER_API_KEY", "test-key"),
            patch("config.settings.settings.LLM_MODEL", "test-model"),
            patch("openai.OpenAI") as mock_client_cls,
        ):
            mock_client_cls.return_value.chat.completions.create.return_value = mock_completion
            summarizer = Summarizer()
            text, tokens, model = summarizer._call_llm("system prompt", "user prompt")

        assert text == "Test response"
        assert tokens == 42
        assert model == "test-model"

    def test_call_llm_raises_without_api_key(self):
        from llm.summarizer import Summarizer
        import pytest

        with patch("config.settings.settings.OPENROUTER_API_KEY", ""):
            summarizer = Summarizer()
            with pytest.raises(ValueError, match="No LLM API key configured"):
                summarizer._call_llm("system", "user")

    def test_call_llm_handles_null_usage(self):
        from llm.summarizer import Summarizer

        mock_message = MagicMock()
        mock_message.content = "Response without usage"
        mock_choice = MagicMock()
        mock_choice.message = mock_message
        mock_completion = MagicMock()
        mock_completion.choices = [mock_choice]
        mock_completion.usage = None

        with (
            patch("config.settings.settings.OPENROUTER_API_KEY", "test-key"),
            patch("config.settings.settings.LLM_MODEL", "test-model"),
            patch("openai.OpenAI") as mock_client_cls,
        ):
            mock_client_cls.return_value.chat.completions.create.return_value = mock_completion
            summarizer = Summarizer()
            text, tokens, model = summarizer._call_llm("system", "user")

        assert text == "Response without usage"
        assert tokens == 0
        assert model == "test-model"
