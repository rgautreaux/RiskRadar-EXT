from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(extra="allow")

    pythonpath: str = ""
    # Database
    DATABASE_URL: str = ""
    DB_PATH: str = str(BASE_DIR / "riskradar.db")

    # JWT Authentication
    JWT_SECRET_KEY: str = "CHANGE-ME-set-a-real-secret-in-dotenv"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # User data protection
    EMAIL_ENCRYPTION_KEY: str = ""
    EMAIL_HASH_SECRET: str = ""
    PASSWORD_MIN_LENGTH: int = 12

    # API Keys
    AIRNOW_API_KEY: str = ""
    OpenAQ_API_KEY: str = ""
    NASA_FIRMS_MAP_KEY: str = ""
    OPENWEATHER_API_KEY: str = ""

    # Firecrawl API Key
    FIRECRAWL_API_KEY: str = ""

    # LLM
    OPENROUTER_API_KEY: str = ""
    LLM_API_KEY: str = ""  # fallback key if OPENROUTER_API_KEY is not set
    LLM_MODEL: str = "x-ai/grok-4.1-fast"
    LLM_MODEL_GUEST: str = ""   # model for unauthenticated users (falls back to LLM_MODEL)
    LLM_MODEL_PREMIUM: str = ""  # model for authenticated users (falls back to LLM_MODEL)

    # App Config
    DEFAULT_ZIP_CODE: str = "90001"
    DEFAULT_LAT: float = 34.0522
    DEFAULT_LON: float = -118.2437
    SCRAPE_INTERVAL_MINUTES: int = 30
    NWS_USER_AGENT: str = "RiskRadar/1.0 (school-project)"
    SOURCES_CONFIG_PATH: str = str(BASE_DIR / "config" / "sources.yaml")

    # CORS
    CORS_ALLOWED_ORIGINS: str = "http://127.0.0.1:8080,http://localhost:8080"

    # Startup safety
    SCHEMA_VALIDATION_STRICT: bool = True

settings = Settings()