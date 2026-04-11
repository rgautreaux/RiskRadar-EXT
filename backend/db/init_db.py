"""Create all database tables. Safe to run multiple times — only creates missing tables."""

from db.database import engine, Base
from db.models import (
    Alert,
    AlertArchive,
    CleanupRun,
    MigrationLog,
    NotificationDispatchLog,
    ScrapeLog,
    ScrapeLogArchive,
    Summary,
    SummaryArchive,
    User,
)

REGISTERED_MODELS = (
    Alert,
    AlertArchive,
    CleanupRun,
    MigrationLog,
    NotificationDispatchLog,
    ScrapeLog,
    ScrapeLogArchive,
    Summary,
    SummaryArchive,
    User,
)


def init_database():
    _ = REGISTERED_MODELS
    Base.metadata.create_all(bind=engine)
    print(f"Database ready: {engine.url}")


if __name__ == "__main__":
    init_database()
