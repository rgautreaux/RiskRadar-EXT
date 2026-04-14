"""Create all database tables. Safe to run multiple times — only creates missing tables."""

import logging

from sqlalchemy import inspect, text

from db.database import engine, Base
import db.models  # noqa: F401 (import so models register)

_log = logging.getLogger(__name__)


def _apply_migrations(eng):
    """Apply incremental schema changes that create_all() cannot handle.

    SQLAlchemy's create_all() only creates *missing* tables; it never adds
    columns to existing tables.  Each migration here is idempotent — it checks
    whether the column already exists before issuing ALTER TABLE.
    """
    inspector = inspect(eng)
    with eng.connect() as conn:
        # Migration: add is_admin to users table (introduced in Stage 4)
        users_columns = {col["name"] for col in inspector.get_columns("users")}
        if "is_admin" not in users_columns:
            _log.info("Migration: adding is_admin column to users table")
            conn.execute(text("ALTER TABLE users ADD COLUMN is_admin BOOLEAN NOT NULL DEFAULT 0"))
            conn.commit()


def init_database():
    Base.metadata.create_all(bind=engine)
    _apply_migrations(engine)
    print(f"Database ready: {engine.url}")


if __name__ == "__main__":
    init_database()
