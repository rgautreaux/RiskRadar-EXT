"""Create all database tables. Safe to run multiple times — only creates missing tables."""

import logging

from sqlalchemy import inspect, text

from backend.db.database import engine, Base
import backend.db.models  # noqa: F401 (import so models register)
from backend.db.schema_validator import (
    SchemaValidationOutcome,
    build_required_schema_from_models,
    validate_required_schema,
)

_log = logging.getLogger(__name__)

CRITICAL_SCHEMA_TABLES = {
    "users",
    "alerts",
    "summaries",
    "summary_alerts",
    "feedback",
}


def _apply_migrations(eng):
    """Apply incremental schema changes that create_all() cannot handle.

    SQLAlchemy's create_all() only creates *missing* tables; it never adds
    columns to existing tables.  Each migration here is idempotent — it checks
    whether the column already exists before issuing ALTER TABLE.
    """
    inspector = inspect(eng)
    with eng.connect() as conn:
        users_columns = {col["name"] for col in inspector.get_columns("users")}
        # Migration: add is_admin to users table (introduced in Stage 4)
        if "is_admin" not in users_columns:
            _log.info("Migration: adding is_admin column to users table")
            conn.execute(text("ALTER TABLE users ADD COLUMN is_admin BOOLEAN NOT NULL DEFAULT 0"))
            conn.commit()
        # Migration: add is_guest to users table (guest restriction enforcement)
        if "is_guest" not in users_columns:
            _log.info("Migration: adding is_guest column to users table")
            conn.execute(text("ALTER TABLE users ADD COLUMN is_guest BOOLEAN NOT NULL DEFAULT 0"))
            conn.commit()


def init_database(*, strict: bool = True) -> SchemaValidationOutcome:
    Base.metadata.create_all(bind=engine)
    _apply_migrations(engine)
    print(f"Database ready: {engine.url}")

    required_schema = build_required_schema_from_models(Base, CRITICAL_SCHEMA_TABLES)
    outcome = validate_required_schema(engine, required_schema)
    if outcome.ok:
        _log.info("Database schema validation passed for critical tables")
        return outcome

    issue_block = "\n".join(f"- {issue}" for issue in outcome.issues)
    remediation = (
        "Schema drift detected. Rebuild local DB if needed, then rerun connectivity checks.\n"
        "Suggested local command:\n"
        "c:/Users/rebec/OneDrive/Documents/GitHub/cmps-357-sp26-final-project-cmps357-team-3/.venv/Scripts/python.exe "
        "backend/demo/seed_demo_data.py --mode fresh --db-path backend/riskradar.db"
    )
    message = f"Database schema validation failed:\n{issue_block}\n{remediation}"
    if strict:
        raise RuntimeError(message)

    _log.warning(message)
    return outcome


if __name__ == "__main__":
    init_database()
