"""Tests for summary API endpoints."""

from unittest.mock import patch


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


class TestGenerateSummary:
    def test_generate_with_alerts(self, test_client, sample_alerts):
        mock_return = ("## Daily Digest\nTest summary content.", 100)
        with patch("llm.summarizer.Summarizer._call_llm", return_value=mock_return):
            resp = test_client.post("/api/v1/summaries/generate")
        assert resp.status_code == 200
        data = resp.json()
        assert "Daily Digest" in data["content"]
        assert data["summary_type"] == "daily"

    def test_generate_no_alerts(self, test_client):
        resp = test_client.post("/api/v1/summaries/generate")
        assert resp.status_code == 404
