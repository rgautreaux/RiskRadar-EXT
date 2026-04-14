"""RiskRadar — FastAPI entry point."""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.config.settings import settings
from db.init_db import init_database
from scrapers.scheduler import start_scheduler
from api.router import api_router

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(name)s %(levelname)s %(message)s")


@asynccontextmanager
async def lifespan(_app: FastAPI):
    # Startup
    init_database(strict=settings.SCHEMA_VALIDATION_STRICT)
    scheduler = start_scheduler()
    yield
    # Shutdown
    scheduler.shutdown()


app = FastAPI(title="RiskRadar API", version="1.0.0", lifespan=lifespan)

_DEFAULT_LOCAL_ORIGINS = [
    "http://127.0.0.1:8080",
    "http://localhost:8080",
]


def _parse_allowed_origins(raw_origins: str) -> list[str]:
    origins = [origin.strip() for origin in raw_origins.split(",") if origin.strip()]
    if origins:
        return origins

    logging.getLogger(__name__).warning(
        "CORS_ALLOWED_ORIGINS was empty; falling back to default local development origins"
    )
    return _DEFAULT_LOCAL_ORIGINS


allowed_origins = _parse_allowed_origins(settings.CORS_ALLOWED_ORIGINS)
logging.getLogger(__name__).info("Configured CORS allowed origins: %s", ", ".join(allowed_origins))
if "http://127.0.0.1:8080" not in allowed_origins and "http://localhost:8080" not in allowed_origins:
    logging.getLogger(__name__).warning(
        "Canonical frontend origin not found in CORS_ALLOWED_ORIGINS; browser requests may fail in local runs"
    )

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

app.include_router(api_router)


@app.get("/")
def root():
    return {"name": "RiskRadar API", "version": "1.0.0", "status": "running"}
