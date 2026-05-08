"""Tests for summary API endpoints."""

import json
from unittest.mock import patch

from db.models import Summary, SummaryAlertLink


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


class TestGetSummary:
    def test_get_existing_summary(self, test_client, sample_summary):
        resp = test_client.get(f"/api/v1/summaries/{sample_summary.id}")
        assert resp.status_code == 200
        data = resp.json()
        assert data["id"] == sample_summary.id
        assert data["title"] == sample_summary.title
        assert data["summary_type"] == "daily"

    def test_get_existing_summary_includes_read_path_explainability(self, test_client, db_session, sample_alerts):
        summary = Summary(
            title="Environmental Digest — Mar 03, 2026",
            content=(
                "## Daily Safety Briefing\n"
                "Strong weather and air-quality conditions are creating mixed travel risk.\n\n"
                "## Top Alerts\n"
                "- Los Angeles: severe thunderstorm warning\n"
                "- Pasadena: pollution advisory\n\n"
                "## Regional Highlights\n"
                "Southern California has the most concentrated alert activity.\n\n"
                "## Traveler Recommendations\n"
                "- Check conditions before leaving\n"
                "- Carry water and a backup route\n"
            ),
            summary_type="daily",
            alert_ids=json.dumps([a.id for a in sample_alerts]),
            region="US",
            generated_at="2026-03-03T08:00:00+00:00",
            model_used="gpt-4o-mini",
            token_count=160,
            created_at="2026-03-03T08:00:00+00:00",
        )
        db_session.add(summary)
        db_session.commit()
        db_session.refresh(summary)

        resp = test_client.get(f"/api/v1/summaries/{summary.id}")
        assert resp.status_code == 200
        data = resp.json()
        assert data["summary_insight"] == "Strong weather and air-quality conditions are creating mixed travel risk."
        assert data["context_notes"] == "Southern California has the most concentrated alert activity."
        assert data["why_it_matters"] == "Check conditions before leaving Carry water and a backup route"
        assert data["key_takeaways"] == ["Los Angeles: severe thunderstorm warning", "Pasadena: pollution advisory"]

    def test_get_summary_not_found(self, test_client):
        resp = test_client.get("/api/v1/summaries/99999")
        assert resp.status_code == 404
        assert "Summary not found" in resp.json()["detail"]


class TestSummaryAlertIds:
    def test_prefers_relational_links(self, test_client, db_session, sample_summary, sample_alerts):
        db_session.add(SummaryAlertLink(summary_id=sample_summary.id, alert_id=sample_alerts[0].id))
        db_session.commit()

        resp = test_client.get(f"/api/v1/summaries/{sample_summary.id}/alert-ids")
        assert resp.status_code == 200
        data = resp.json()
        assert data["summary_id"] == sample_summary.id
        assert data["source"] == "summary_alerts"
        assert data["alert_ids"] == [sample_alerts[0].id]

    def test_falls_back_to_json_when_no_relational_rows(self, test_client, sample_summary):
        resp = test_client.get(f"/api/v1/summaries/{sample_summary.id}/alert-ids")
        assert resp.status_code == 200
        data = resp.json()
        assert data["source"] == "summaries.alert_ids"
        assert data["alert_ids"] == json.loads(sample_summary.alert_ids)


class TestGenerateSummary:
    def test_generate_with_alerts(self, test_client, sample_alerts):
        mock_return = ("## Daily Digest\nTest summary content.", 100, "gpt-4o-mini")
        with patch("llm.summarizer.Summarizer._call_llm", return_value=mock_return):
            resp = test_client.post("/api/v1/summaries/generate")
        assert resp.status_code == 200
        data = resp.json()
        assert "Daily Digest" in data["content"]
        assert data["summary_type"] == "daily"

    def test_generate_no_alerts(self, test_client):
        resp = test_client.post("/api/v1/summaries/generate")
        assert resp.status_code == 404
