"""Tests for summary API endpoints."""

from unittest.mock import patch

from db.models import Summary


def _mock_local_alert(source: str, source_id: str, title: str) -> dict:
    return {
        "source": source,
        "source_id": source_id,
        "alert_type": "weather" if source == "nws" else "air_quality",
        "severity": "high" if source == "nws" else "moderate",
        "title": title,
        "description": f"{title} description",
        "latitude": 34.05,
        "longitude": -118.24,
        "location_name": "Los Angeles, CA",
        "event_start": "2026-04-10T12:00:00Z",
        "event_end": None,
    }


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


class TestLocalSummaryFlow:
    def test_generate_local_summary(self, test_client, db_session, monkeypatch):
        monkeypatch.setattr("api.location._zip_to_coords", lambda zip_code: (34.05, -118.24, "Los Angeles", "CA"))
        monkeypatch.setattr(
            "api.location._fetch_nws_alerts",
            lambda lat, lon, state: [_mock_local_alert("nws", "nws_001", "Local Severe Weather")],
        )
        monkeypatch.setattr(
            "api.location._fetch_airnow",
            lambda zip_code: [_mock_local_alert("airnow", f"{zip_code}_PM25_2026-04-10", "Local Air Quality")],
        )

        mock_return = ("## Local Digest\nTest local summary.", 42)
        with patch("llm.summarizer.Summarizer._call_llm", return_value=mock_return):
            resp = test_client.post("/api/v1/summaries/generate/local?zip_code=90001")

        assert resp.status_code == 200
        data = resp.json()
        assert data["summary_type"] == "local"
        assert data["region"] == "Los Angeles, CA 90001"
        assert "Local Digest for Los Angeles, CA" in data["title"]
        assert data["content"] == "## Local Digest\nTest local summary."
        assert db_session.query(Summary).count() == 1

        latest = test_client.get("/api/v1/summaries/latest/local?zip_code=90001")
        assert latest.status_code == 200
        latest_data = latest.json()
        assert latest_data["id"] == data["id"]
        assert latest_data["summary_type"] == "local"

    def test_generate_local_summary_not_found(self, test_client, monkeypatch):
        monkeypatch.setattr("api.location._zip_to_coords", lambda zip_code: None)

        resp = test_client.post("/api/v1/summaries/generate/local?zip_code=99999")
        assert resp.status_code == 404
        assert "Could not find location" in resp.json()["detail"]

    def test_latest_local_summary_returns_none_when_missing(self, test_client):
        resp = test_client.get("/api/v1/summaries/latest/local?zip_code=90001")
        assert resp.status_code == 200
        assert resp.json() is None
