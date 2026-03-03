"""Scheduler — runs each scraper on a timed interval."""

import logging
from datetime import datetime, timedelta, timezone

from apscheduler.schedulers.background import BackgroundScheduler

from config.settings import settings
from scrapers.registry import load_all_scrapers

logger = logging.getLogger(__name__)


def start_scheduler() -> BackgroundScheduler:
    scheduler = BackgroundScheduler()
    default_interval = settings.SCRAPE_INTERVAL_MINUTES
    now = datetime.now(timezone.utc)

    scrapers = load_all_scrapers()

    for entry in scrapers:
        interval = entry["interval_minutes"] or default_interval
        offset = entry["stagger_offset_minutes"]

        scheduler.add_job(
            entry["scraper"].run,
            "interval",
            minutes=interval,
            next_run_time=now + timedelta(minutes=offset),
            id=entry["id"],
        )
        logger.info(
            f"Registered scraper '{entry['id']}': "
            f"interval={interval}m, first_run=+{offset}m"
        )

    scheduler.start()
    logger.info(f"Scheduler started — {len(scrapers)} scrapers registered")
    return scheduler
