"""Migration Script: Encrypt and HMAC Existing User Emails.

This script migrates all users in the database:
- Encrypts the plaintext email into email_encrypted
- Computes HMAC for email_hmac
- Sets legacy email field to None (for privacy)
- Logs batch start/end and per-user actions to MigrationLog

Run this script in a safe environment after backing up the database.
"""

from datetime import datetime, timezone
import os
import re
import sys
from importlib import import_module
from pathlib import Path

from sqlalchemy import inspect, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

BACKEND_DIR = Path(__file__).resolve().parents[2]
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

security_module = import_module("auth.security")
database_module = import_module("db.database")
models_module = import_module("db.models")

encrypt_email = security_module.encrypt_email
email_hmac = security_module.email_hmac
SessionLocal = database_module.SessionLocal
Base = database_module.Base
MigrationLog = models_module.MigrationLog
User = models_module.User


EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
MAX_ERROR_LENGTH = 500
BATCH_SIZE = int(os.getenv("MIGRATION_BATCH_SIZE", "100"))


def _now_utc() -> datetime:
    return datetime.now(timezone.utc)


def safe_error_message(exc: Exception) -> str:
    """Sanitize exception text to avoid leaking sensitive values into logs."""
    message = str(exc) if exc else "unknown error"
    message = EMAIL_RE.sub("[REDACTED_EMAIL]", message)
    if len(message) > MAX_ERROR_LENGTH:
        return f"{message[:MAX_ERROR_LENGTH]}..."
    return message


def _log(
    db: Session,
    *,
    action: str,
    status: str,
    user_id: int | None = None,
    error_message: str | None = None,
) -> None:
    db.add(
        MigrationLog(
            timestamp=_now_utc(),
            user_id=user_id,
            action=action,
            status=status,
            error_message=error_message,
        )
    )


def _ensure_phase3_schema(db: Session) -> None:
    """Create the migration log table and add missing email columns if needed."""
    bind = db.get_bind()
    if bind is None:
        raise RuntimeError("Could not resolve database bind for email migration")

    Base.metadata.create_all(bind=bind)

    inspector = inspect(bind)
    user_columns = {column["name"] for column in inspector.get_columns("users")}

    if "email_encrypted" not in user_columns:
        db.execute(text("ALTER TABLE users ADD COLUMN email_encrypted TEXT"))

    if "email_hmac" not in user_columns:
        db.execute(text("ALTER TABLE users ADD COLUMN email_hmac TEXT"))

    db.commit()


def migrate_emails() -> int:
    db: Session = SessionLocal()
    processed = 0
    succeeded = 0
    failed = 0

    try:
        _ensure_phase3_schema(db)

        _log(db, action="email_encryption_batch", status="started")
        db.commit()

        last_id = 0
        while True:
            batch = (
                db.query(User)
                .filter(User.email.isnot(None), User.id > last_id)
                .order_by(User.id.asc())
                .limit(BATCH_SIZE)
                .all()
            )
            if not batch:
                        user.email_hmac = email_hmac(original_email)
                        user.email = None

                        _log(db, action="email_encryption", status="success", user_id=user_id)
                    succeeded += 1
                except (ValueError, TypeError, OSError, RuntimeError, SQLAlchemyError) as exc:
                    failed += 1
                    _log(
                        db,
                        action="email_encryption",
                        status="error",
                        user_id=user_id,
                        error_message=safe_error_message(exc),
                    )

            db.commit()
            last_id = batch[-1].id
            if len(batch) < BATCH_SIZE:
                break

        summary = f"processed={processed},succeeded={succeeded},failed={failed}"
        _log(db, action="email_encryption_batch", status="completed", error_message=summary)
        db.commit()
        return 0 if failed == 0 else 2
    except (ValueError, TypeError, OSError, RuntimeError, SQLAlchemyError) as exc:
        db.rollback()
        _log(
            db,
            action="email_encryption_batch",
            status="failed",
            error_message=safe_error_message(exc),
        )
        db.commit()
        return 1
    finally:
        db.close()


if __name__ == "__main__":
    code = migrate_emails()
    print("Migration complete." if code == 0 else "Migration finished with errors.")
    sys.exit(code)
