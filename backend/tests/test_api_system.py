"""Tests for system API endpoints."""

from datetime import datetime, timezone

from auth.security import create_access_token
from db.models import ScrapeLog


def _auth_headers(user_id: int) -> dict[str, str]:
    token = create_access_token(data={"sub": str(user_id)})
    return {"Authorization": f"Bearer {token}"}


def test_health_endpoint(test_client, sample_alerts):
    resp = test_client.get("/api/v1/health")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "healthy"
    assert data["database"] == "connected"
    assert "alert_count" in data


def test_health_endpoint_includes_last_scrape(test_client, db_session, sample_alerts):
    scrape_log = ScrapeLog(
        source="nws",
        status="success",
        alerts_fetched=3,
        alerts_new=2,
        started_at=datetime.now(timezone.utc),
        completed_at=datetime.now(timezone.utc),
    )
    db_session.add(scrape_log)
    db_session.commit()

    resp = test_client.get("/api/v1/health")
    assert resp.status_code == 200
    data = resp.json()
    assert data["last_scrape"]["source"] == "nws"
    assert data["last_scrape"]["status"] == "success"


def test_trigger_scrape_requires_auth(test_client):
    resp = test_client.post("/api/v1/scrape/trigger")
    assert resp.status_code == 401


def test_trigger_scrape_runs_registered_scrapers(test_client, sample_user, monkeypatch):
    class FakeScraper:
        def run(self):
            return 2

    def _fake_load_all_scrapers():
        return [
            {"id": "fake_one", "scraper": FakeScraper()},
            {"id": "fake_two", "scraper": FakeScraper()},
        ]

    monkeypatch.setattr("scrapers.registry.load_all_scrapers", _fake_load_all_scrapers)

    resp = test_client.post(
        "/api/v1/scrape/trigger",
        headers=_auth_headers(sample_user.id),
    )
    assert resp.status_code == 200
    data = resp.json()
    assert len(data["results"]) == 2
    assert all(item["status"] == "success" for item in data["results"])
    assert all(item["alerts_stored"] == 2 for item in data["results"])


def test_trigger_scrape_reports_partial_failure(test_client, sample_user, monkeypatch):
    class FakeScraper:
        def run(self):
            return 2

    class FailingScraper:
        def run(self):
            raise RuntimeError("scraper exploded")

    def _fake_load_all_scrapers():
        return [
            {"id": "working", "scraper": FakeScraper()},
            {"id": "broken", "scraper": FailingScraper()},
        ]

    monkeypatch.setattr("scrapers.registry.load_all_scrapers", _fake_load_all_scrapers)

    resp = test_client.post(
        "/api/v1/scrape/trigger",
        headers=_auth_headers(sample_user.id),
    )
    assert resp.status_code == 200
    data = resp.json()
    assert len(data["results"]) == 2
    assert data["results"][0]["status"] == "success"
    assert data["results"][1]["status"] == "error"
    assert "scraper exploded" in data["results"][1]["error"]
