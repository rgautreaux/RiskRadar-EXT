"""Quick test: scrape data from free APIs and generate a summary.

Run from the backend directory:
    python test_scrape_and_summarize.py

For repeatable local/CI checks without paid LLM credits:
    python test_scrape_and_summarize.py --mock-summary
"""

import argparse
import logging
from contextlib import nullcontext
from unittest.mock import patch

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(name)s %(levelname)s %(message)s",
)
logger = logging.getLogger("test")


def _build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run scraper + database + summary smoke test."
    )
    parser.add_argument(
        "--mock-summary",
        action="store_true",
        help="Mock the LLM call so summary generation is deterministic and offline-friendly.",
    )
    parser.add_argument(
        "--skip-summary",
        action="store_true",
        help="Skip the summary generation step.",
    )
    parser.add_argument(
        "--since-hours",
        type=int,
        default=24,
        help="How far back to look for alerts when generating summary (default: 24).",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _build_arg_parser().parse_args(argv)

    # --- Step 1: Initialize database ---
    logger.info("=== Step 1: Initializing database ===")
    from db.init_db import init_database

    init_database()
    logger.info("Database initialized.\n")

    # --- Step 2: Run scrapers (no API key needed) ---
    from scrapers.nws_scraper import NWSScraper
    from scrapers.epa_scraper import EPAScraper

    scrapers_to_test = [
        ("NWS (weather)", NWSScraper()),
        ("EPA (pollution)", EPAScraper()),
    ]

    # Also test the USGS config-driven scraper if sources.yaml has it
    try:
        from scrapers.registry import _load_yaml_config
        from scrapers.generic_api_scraper import GenericAPIScraper

        config = _load_yaml_config()
        for api_cfg in config.get("api_sources", []):
            if api_cfg.get("enabled", True) and api_cfg.get("auth", {}).get("type", "none") == "none":
                scrapers_to_test.append(
                    (f"Generic API: {api_cfg['name']}", GenericAPIScraper(api_cfg))
                )
    except Exception as e:
        logger.warning("Could not load config-driven scrapers: %s", e)

    scraper_failures = 0
    for name, scraper in scrapers_to_test:
        logger.info("=== Step 2: Running %s scraper ===", name)
        try:
            scraper.run()
        except Exception as e:
            scraper_failures += 1
            logger.error("%s scraper failed: %s", name, e)
        print()

    # --- Step 3: Check what we scraped ---
    logger.info("=== Step 3: Checking scraped alerts ===")
    from db.database import SessionLocal
    from db.models import Alert

    db = SessionLocal()
    try:
        alerts = db.query(Alert).all()
        logger.info("Total alerts in database: %s", len(alerts))

        if not alerts:
            logger.warning("No alerts were scraped. Cannot generate summary.")
            logger.info("This may be normal if there are no active weather alerts in your area.")
            return 1

        # Show a few examples
        for a in alerts[:5]:
            print(f"  [{a.source}] {a.severity.upper():10s} | {a.title[:70]}")
        if len(alerts) > 5:
            print(f"  ... and {len(alerts) - 5} more")
        print()

        # --- Step 4: Generate summary ---
        summary_failed = False
        if args.skip_summary:
            logger.info("=== Step 4: Skipped summary generation (--skip-summary) ===")
        else:
            logger.info("=== Step 4: Generating daily digest summary ===")
            from llm.summarizer import Summarizer

            summarizer = Summarizer()

            patch_ctx = (
                patch.object(
                    Summarizer,
                    "_call_llm",
                    return_value=(
                        "[MOCK] Daily digest generated for integration verification.",
                        42,
                    ),
                )
                if args.mock_summary
                else nullcontext()
            )
            try:
                with patch_ctx:
                    summary = summarizer.generate_daily_digest(db, since_hours=args.since_hours)

                if summary:
                    logger.info(
                        "Summary generated! (model=%s, tokens=%s)",
                        summary.model_used,
                        summary.token_count,
                    )
                    print()
                    print("--- DAILY DIGEST ---")
                    print(summary.content)
                    print("--- END ---")
                else:
                    logger.warning("No summary generated (no recent alerts).")
                    summary_failed = True
            except Exception as e:
                summary_failed = True
                logger.error("Summary generation failed: %s", e)
                if args.mock_summary:
                    logger.error("Mock summary mode failed unexpectedly.")
                else:
                    logger.info(
                        "If this is an auth/credits issue, rerun with --mock-summary for deterministic checks."
                    )

    finally:
        db.close()

    logger.info("\nTest complete!")
    if scraper_failures > 0:
        logger.error("Scraper failures: %s", scraper_failures)
    if not args.skip_summary and summary_failed:
        return 1
    if scraper_failures > 0:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
