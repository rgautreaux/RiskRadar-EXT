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

from ..db.database import SessionLocal  # noqa: E402


LOGGER = logging.getLogger("riskradar.summary_alert_backfill")


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

    normalized_ids: list[int] = []
    for item in parsed:
        if isinstance(item, bool):
            continue

        try:
            alert_id = int(item)
        except (TypeError, ValueError):
            continue

        if alert_id > 0:
            normalized_ids.append(alert_id)

    return normalized_ids


def backfill_summary_alert_links(
    batch_size: int = 100,
    dry_run: bool = False,
    session=None,
) -> dict[str, int]:
    owns_session = session is None
    if session is None:
        session = SessionLocal()
    inserted = 0
    skipped_existing = 0
    skipped_missing_alert = 0
    skipped_invalid_summary = 0

    try:
        if not _table_exists(session, "summary_alerts"):
            raise RuntimeError(
                "Missing summary_alerts table. Apply backend/db/migrations/2026-04-11_add_summary_alerts_and_feedback_fk.sql first."
            )

        summary_rows = session.execute(
            text("SELECT id, alert_ids, created_at, generated_at FROM summaries ORDER BY id")
        ).mappings().all()

        for row in summary_rows:
            summary_id = int(row["id"])
            parsed_ids = _parse_alert_ids(row.get("alert_ids"))
            if not parsed_ids:
                skipped_invalid_summary += 1
                continue

            # Keep deterministic ordering and remove duplicates from malformed JSON arrays.
            unique_alert_ids = list(dict.fromkeys(parsed_ids))

            existing_ids = {
                int(alert_id)
                for alert_id in session.execute(
                    text("SELECT alert_id FROM summary_alerts WHERE summary_id = :summary_id"),
                    {"summary_id": summary_id},
                ).scalars()
            }

            available_alert_ids = {
                int(alert_id)
                for alert_id in session.execute(
                    text(
                        "SELECT id FROM alerts WHERE id IN ("
                        + ",".join(f":a{i}" for i in range(len(unique_alert_ids)))
                        + ")"
                    ),
                    {f"a{i}": alert_id for i, alert_id in enumerate(unique_alert_ids)},
                ).scalars()
            }

            for alert_id in unique_alert_ids:
                if alert_id in existing_ids:
                    skipped_existing += 1
                    continue

                if alert_id not in available_alert_ids:
                    skipped_missing_alert += 1
                    continue

                if dry_run:
                    inserted += 1
                    continue

                session.execute(
                    text(
                        "INSERT INTO summary_alerts (summary_id, alert_id, created_at) "
                        "VALUES (:summary_id, :alert_id, :created_at)"
                    ),
                    {
                        "summary_id": summary_id,
                        "alert_id": alert_id,
                        "created_at": row.get("created_at")
                        if "created_at" in row and row.get("created_at")
                        else row.get("generated_at")
                        if "generated_at" in row and row.get("generated_at")
                        else "",
                    },
                )
                inserted += 1

                if inserted % batch_size == 0:
                    session.commit()

        if dry_run:
            session.rollback()
        else:
            session.commit()

        return {
            "inserted": inserted,
            "skipped_existing": skipped_existing,
            "skipped_missing_alert": skipped_missing_alert,
            "skipped_invalid_summary": skipped_invalid_summary,
        }
    except Exception:
        session.rollback()
        raise
    finally:
        if owns_session:
            session.close()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Backfill summary_alerts rows from summaries.alert_ids JSON arrays."
    )
    parser.add_argument("--batch-size", type=int, default=100, help="Number of inserts per commit")
    parser.add_argument("--dry-run", action="store_true", help="Report inserts without writing rows")
    return parser


def main() -> int:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    args = build_parser().parse_args()

    stats = backfill_summary_alert_links(batch_size=max(1, args.batch_size), dry_run=args.dry_run)
    LOGGER.info(
        "Backfill complete. inserted=%s skipped_existing=%s skipped_missing_alert=%s skipped_invalid_summary=%s",
        stats["inserted"],
        stats["skipped_existing"],
        stats["skipped_missing_alert"],
        stats["skipped_invalid_summary"],
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
