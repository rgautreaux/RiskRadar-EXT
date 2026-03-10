import os
from pathlib import Path
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    # Database
    DB_PATH: str = str(BASE_DIR / "riskradar.db")

    # API Keys
    AIRNOW_API_KEY: str = ""
    NASA_FIRMS_MAP_KEY: str = ""
    FIRECRAWL_API_KEY: str = ""

    # LLM
    LLM_API_KEY: str = ""
    LLM_PROVIDER: str = "deepseek"
    LLM_MODEL: str = "deepseek-chat"

    # JWT Authentication
    # IMPORTANT: Change JWT_SECRET_KEY in your .env file before production!
    JWT_SECRET_KEY: str = "CHANGE-ME-set-a-real-secret-in-dotenv"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60  # token lifetime in minutes

    # App Config
    DEFAULT_ZIP_CODE: str = "90001"
    DEFAULT_LAT: float = 34.0522
    DEFAULT_LON: float = -118.2437
    SCRAPE_INTERVAL_MINUTES: int = 30
    NWS_USER_AGENT: str = "RiskRadar/1.0 (school-project)"
    SOURCES_CONFIG_PATH: str = str(BASE_DIR / "config" / "sources.yaml")

    class Config:
        env_file = str(BASE_DIR.parent / ".env")
        env_file_encoding = "utf-8"


settings = Settings()
