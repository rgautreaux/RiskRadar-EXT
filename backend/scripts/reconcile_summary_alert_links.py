from __future__ import annotations

import argparse
import json
import logging
import sys
from pathlib import Path

from sqlalchemy import inspect, text

BACKEND_DIR = Path(__file__).resolve().parents[1]
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from db.database import SessionLocal  # noqa: E402


LOGGER = logging.getLogger("riskradar.summary_alert_reconcile")


def _table_exists(session, table_name: str) -> bool:
    inspector = inspect(session.get_bind())
    return table_name in inspector.get_table_names()


def _parse_alert_ids(raw_value: str | None) -> list[int]:
    if not raw_value:
        return []

    try:
        parsed = json.loads(raw_value)
    except (json.JSONDecodeError, TypeError):
        return []

    if not isinstance(parsed, list):
        return []

    normalized: list[int] = []
    for item in parsed:
        if isinstance(item, bool):
            continue
        try:
            value = int(item)
        except (TypeError, ValueError):
            continue
        if value > 0:
            normalized.append(value)

    return list(dict.fromkeys(normalized))


def reconcile_summary_alert_links(limit: int = 25, session=None) -> dict[str, object]:
    owns_session = session is None
    if session is None:
        session = SessionLocal()

    mismatches: list[dict[str, object]] = []
    checked = 0

    try:
        if not _table_exists(session, "summary_alerts"):
            raise RuntimeError(
                "Missing summary_alerts table. Apply backend/db/migrations/2026-04-11_add_summary_alerts_and_feedback_fk.sql first."
            )

        summary_rows = session.execute(
            text("SELECT id, alert_ids FROM summaries ORDER BY id")
        ).mappings().all()

        for row in summary_rows:
            checked += 1
            summary_id = int(row["id"])
            json_ids = set(_parse_alert_ids(row.get("alert_ids")))
            relational_ids = {
                int(alert_id)
                for alert_id in session.execute(
                    text("SELECT alert_id FROM summary_alerts WHERE summary_id = :summary_id"),
                    {"summary_id": summary_id},
                ).scalars()
            }

            if json_ids == relational_ids:
                continue

            mismatches.append(
                {
                    "summary_id": summary_id,
                    "json_only": sorted(list(json_ids - relational_ids)),
                    "relational_only": sorted(list(relational_ids - json_ids)),
                }
            )

            if len(mismatches) >= limit:
                break

        return {
            "checked": checked,
            "mismatch_count": len(mismatches),
            "mismatches": mismatches,
        }
    finally:
        if owns_session:
            session.close()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Compare summaries.alert_ids JSON links against summary_alerts relational links."
    )
    parser.add_argument("--limit", type=int, default=25, help="Maximum mismatch rows to print")
    parser.add_argument(
        "--fail-on-mismatch",
        action="store_true",
        help="Exit with non-zero status if any mismatches are detected.",
    )
    return parser


def main() -> int:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    args = build_parser().parse_args()
    report = reconcile_summary_alert_links(limit=max(1, args.limit))

    LOGGER.info("Reconciliation report: checked=%s mismatch_count=%s", report["checked"], report["mismatch_count"])
    for mismatch in report["mismatches"]:
        LOGGER.info(
            "summary_id=%s json_only=%s relational_only=%s",
            mismatch["summary_id"],
            mismatch["json_only"],
            mismatch["relational_only"],
        )

    if args.fail_on_mismatch and int(report["mismatch_count"]) > 0:
        LOGGER.error("Detected summary link mismatches while --fail-on-mismatch is enabled.")
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
