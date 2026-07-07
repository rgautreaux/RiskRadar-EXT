from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

from sqlalchemy import inspect, text

BACKEND_DIR = Path(__file__).resolve().parents[1]
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from auth.security import decrypt_email, encrypt_email, hash_email, is_encrypted_email, normalize_email  # noqa: E402
from backend.db.database import SessionLocal  # noqa: E402


LOGGER = logging.getLogger("riskradar.email_migration")


def _users_table_columns(session) -> set[str]:
    inspector = inspect(session.get_bind())
    return {column["name"] for column in inspector.get_columns("users")}


def _ensure_lookup_column(session, dry_run: bool) -> bool:
    columns = _users_table_columns(session)
    if "email_lookup_hash" in columns:
        return True

    if dry_run:
        LOGGER.info("Schema is missing users.email_lookup_hash; apply the schema migration before production rollout.")
        return False

    dialect = session.get_bind().dialect.name
    if dialect == "sqlite":
        session.execute(text("ALTER TABLE users ADD COLUMN email_lookup_hash TEXT"))
        session.execute(text("CREATE UNIQUE INDEX IF NOT EXISTS uq_users_email_lookup_hash ON users(email_lookup_hash)"))
    else:
        session.execute(text("ALTER TABLE `users` ADD COLUMN `email_lookup_hash` TEXT NULL AFTER `email`"))
        session.execute(text("ALTER TABLE `users` ADD UNIQUE KEY `uq_users_email_lookup_hash` (`email_lookup_hash`)"))

    session.commit()
    LOGGER.info("Added users.email_lookup_hash to the database schema.")
    return True


def migrate_users(batch_size: int = 100, dry_run: bool = False) -> int:
    session = SessionLocal()
    migrated = 0

    try:
        has_lookup_hash = _ensure_lookup_column(session, dry_run=dry_run)
        columns = ["id", "email"]
        if has_lookup_hash:
            columns.append("email_lookup_hash")

        column_sql = ", ".join(columns)
        rows = session.execute(text(f"SELECT {column_sql} FROM users ORDER BY id")).mappings()

        for row in rows:
            raw_email = row["email"]
            if not raw_email:
                continue

            if is_encrypted_email(raw_email):
                plaintext_email = normalize_email(decrypt_email(raw_email))
            else:
                plaintext_email = normalize_email(raw_email)

            encrypted_email = encrypt_email(plaintext_email)
            lookup_hash = hash_email(plaintext_email)

            if dry_run:
                LOGGER.info("Would migrate user_id=%s email=%s", row["id"], plaintext_email)
                continue

            session.execute(
                text("UPDATE users SET email = :email, email_lookup_hash = :lookup_hash WHERE id = :user_id"),
                {"email": encrypted_email, "lookup_hash": lookup_hash, "user_id": row["id"]},
            )
            migrated += 1

            if migrated % batch_size == 0:
                session.commit()

        if dry_run:
            session.rollback()
        else:
            session.commit()

        return migrated
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Encrypt existing RiskRadar user emails.")
    parser.add_argument("--batch-size", type=int, default=100, help="Number of records to process per commit")
    parser.add_argument("--dry-run", action="store_true", help="Report changes without writing row updates")
    return parser


def main() -> int:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    args = build_parser().parse_args()
    migrated = migrate_users(batch_size=args.batch_size, dry_run=args.dry_run)
    LOGGER.info("Completed email migration. Updated %s user records.", migrated)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())