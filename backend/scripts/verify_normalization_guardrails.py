from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

from sqlalchemy import inspect

BACKEND_DIR = Path(__file__).resolve().parents[1]
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from backend.db.database import SessionLocal  # noqa: E402
from scripts.backfill_summary_alert_links import backfill_summary_alert_links  # noqa: E402
from scripts.backfill_user_alert_preferences import backfill_user_alert_preferences  # noqa: E402
from scripts.backfill_user_health_conditions import backfill_user_health_conditions  # noqa: E402
from scripts.reconcile_summary_alert_links import reconcile_summary_alert_links  # noqa: E402


LOGGER = logging.getLogger("riskradar.normalization_guardrails")


def _table_exists(session, table_name: str) -> bool:
    inspector = inspect(session.get_bind())
    return table_name in inspector.get_table_names()


def run_guardrails(strict: bool = False, allow_missing_tables: bool = True) -> int:
    session = SessionLocal()
    missing_tables: list[str] = []

    try:
        summary_links_exists = _table_exists(session, "summary_alerts")
        user_alert_pref_exists = _table_exists(session, "user_alert_preferences")
        user_health_exists = _table_exists(session, "user_health_conditions")

        if not summary_links_exists:
            missing_tables.append("summary_alerts")
        if not user_alert_pref_exists:
            missing_tables.append("user_alert_preferences")
        if not user_health_exists:
            missing_tables.append("user_health_conditions")

        if missing_tables and not allow_missing_tables:
            LOGGER.error("Required normalization tables are missing: %s", ", ".join(missing_tables))
            return 2

        if missing_tables:
            LOGGER.warning("Skipping guardrails for missing tables: %s", ", ".join(missing_tables))

        if summary_links_exists:
            summary_backfill = backfill_summary_alert_links(session=session, dry_run=True)
            LOGGER.info("summary_backfill_dry_run %s", summary_backfill)

            report = reconcile_summary_alert_links(session=session)
            LOGGER.info("summary_reconcile checked=%s mismatch_count=%s", report["checked"], report["mismatch_count"])
            if int(report["mismatch_count"]) > 0:
                for mismatch in report["mismatches"]:
                    LOGGER.warning(
                        "summary_mismatch summary_id=%s json_only=%s relational_only=%s",
                        mismatch["summary_id"],
                        mismatch["json_only"],
                        mismatch["relational_only"],
                    )
                if strict:
                    LOGGER.error("Strict mode enabled and summary mismatches detected.")
                    return 1

        if user_alert_pref_exists:
            user_pref_backfill = backfill_user_alert_preferences(session=session, dry_run=True)
            LOGGER.info("user_alert_preferences_backfill_dry_run %s", user_pref_backfill)

        if user_health_exists:
            user_health_backfill = backfill_user_health_conditions(session=session, dry_run=True)
            LOGGER.info("user_health_conditions_backfill_dry_run %s", user_health_backfill)

        LOGGER.info("Normalization guardrails passed.")
        return 0
    finally:
        session.close()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run normalization guardrails: dry-run backfills + summary reconciliation."
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Fail if reconciliation mismatches are detected.",
    )
    parser.add_argument(
        "--allow-missing-tables",
        action="store_true",
        default=False,
        help="Do not fail when normalization tables are missing (pre-migration environments).",
    )
    return parser


def main() -> int:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    args = build_parser().parse_args()
    return run_guardrails(strict=args.strict, allow_missing_tables=args.allow_missing_tables)


if __name__ == "__main__":
    raise SystemExit(main())
