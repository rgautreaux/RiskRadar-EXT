from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

try:
    from ..config.settings import settings  # Package/module context
except (ImportError, ValueError):
    try:
        from config.settings import settings  # Script context
    except ImportError:
        from backend.config.settings import settings  # Fallback for direct backend run

database_url = str(settings.DATABASE_URL).strip()
DATABASE_URL = database_url or f"sqlite:///{str(settings.DB_PATH)}"

if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else:
    engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


def get_db():
    """FastAPI dependency — yields a DB session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
