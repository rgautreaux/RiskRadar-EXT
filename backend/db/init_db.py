"""Create all database tables. Safe to run multiple times — only creates missing tables."""

import sqlite3

from db.database import engine, Base
from db.models import Alert, Summary, User, ScrapeLog  # noqa: F401 (import so models register)


def _migrate_users_table():
    """Add columns introduced after initial schema (email_encrypted, email_hmac)."""
    if not str(engine.url).startswith("sqlite"):
        return
    db_path = str(engine.url).replace("sqlite:///", "")
    if not db_path:
        return  # safety guard: never connect to an empty path
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    # Check the table exists before trying to alter it
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
    if not cursor.fetchone():
        conn.close()
        return
    cursor.execute("PRAGMA table_info(users)")
    existing = {row[1] for row in cursor.fetchall()}
    if "email_encrypted" not in existing:
        cursor.execute("ALTER TABLE users ADD COLUMN email_encrypted TEXT")
    if "email_hmac" not in existing:
        cursor.execute("ALTER TABLE users ADD COLUMN email_hmac TEXT")
    conn.commit()
    conn.close()


def init_database():
    Base.metadata.create_all(bind=engine)
    _migrate_users_table()
    print(f"Database ready: {engine.url}")


if __name__ == "__main__":
    init_database()
