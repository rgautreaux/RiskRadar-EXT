from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config.settings import settings
from db.models import Base  # noqa: F401 — re-exported so callers can use `from db.database import Base`

database_url = str(settings.DATABASE_URL).strip()
DATABASE_URL = database_url or f"sqlite:///{str(settings.DB_PATH)}"

if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else:
    engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)


def get_db():
    """FastAPI dependency — yields a DB session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
