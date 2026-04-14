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


LOGGER = logging.getLogger("riskradar.user_health_conditions_backfill")


def _table_exists(session, table_name: str) -> bool:
    inspector = inspect(session.get_bind())
    return table_name in inspector.get_table_names()


def _parse_health_conditions(raw_value: str | None) -> list[str]:
    if not raw_value:
        return []

    try:
        parsed = json.loads(raw_value)
    except (json.JSONDecodeError, TypeError):
        return []

    if not isinstance(parsed, list):
        return []

    cleaned: list[str] = []
    for item in parsed:
        normalized = str(item).strip().lower()
        if normalized:
            cleaned.append(normalized)

    return list(dict.fromkeys(cleaned))


def backfill_user_health_conditions(
    batch_size: int = 100,
    dry_run: bool = False,
    session=None,
) -> dict[str, int]:
    owns_session = session is None
    if session is None:
        session = SessionLocal()

    inserted = 0
    skipped_existing = 0
    skipped_invalid_user = 0

    try:
        if not _table_exists(session, "user_health_conditions"):
            raise RuntimeError(
                "Missing user_health_conditions table. Apply backend/db/migrations/2026-04-12_add_user_health_conditions.sql first."
            )

        user_rows = session.execute(
            text("SELECT id, health_conditions, created_at FROM users ORDER BY id")
        ).mappings().all()

        for row in user_rows:
            user_id = int(row["id"])
            condition_keys = _parse_health_conditions(row.get("health_conditions"))
            if not condition_keys:
                skipped_invalid_user += 1
                continue

            existing_keys = {
                str(condition_key)
                for condition_key in session.execute(
                    text(
                        "SELECT condition_key FROM user_health_conditions WHERE user_id = :user_id"
                    ),
                    {"user_id": user_id},
                ).scalars()
            }

            for condition_key in condition_keys:
                if condition_key in existing_keys:
                    skipped_existing += 1
                    continue

                if dry_run:
                    inserted += 1
                    continue

                session.execute(
                    text(
                        "INSERT INTO user_health_conditions (user_id, condition_key, created_at) "
                        "VALUES (:user_id, :condition_key, :created_at)"
                    ),
                    {
                        "user_id": user_id,
                        "condition_key": condition_key,
                        "created_at": row.get("created_at") or "",
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
            "skipped_invalid_user": skipped_invalid_user,
        }
    except Exception:
        session.rollback()
        raise
    finally:
        if owns_session:
            session.close()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Backfill user_health_conditions from users.health_conditions JSON arrays."
    )
    parser.add_argument("--batch-size", type=int, default=100, help="Number of inserts per commit")
    parser.add_argument("--dry-run", action="store_true", help="Report inserts without writing rows")
    return parser


def main() -> int:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    args = build_parser().parse_args()

    stats = backfill_user_health_conditions(batch_size=max(1, args.batch_size), dry_run=args.dry_run)
    LOGGER.info(
        "Backfill complete. inserted=%s skipped_existing=%s skipped_invalid_user=%s",
        stats["inserted"],
        stats["skipped_existing"],
        stats["skipped_invalid_user"],
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
