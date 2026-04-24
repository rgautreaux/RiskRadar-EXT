"""Health check endpoints for liveness and readiness probes."""

from __future__ import annotations


from fastapi import APIRouter
from fastapi.responses import JSONResponse
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from db.database import Base, engine
from db.init_db import CRITICAL_SCHEMA_TABLES
from db.schema_validator import build_required_schema_from_models, validate_required_schema  # type: ignore[import]

router = APIRouter(prefix="/health", tags=["Health"])  # type: ignore[misc]


@router.get("")
def health_live() -> dict[str, object]:
    """Return a simple liveness response indicating the API process is running."""
    return {
        "status": "ok",
        "service": "riskradar-api",  # cspell:ignore riskradar
        "checks": {
            "api": "pass",
        },
    }


@router.get("/ready")
def health_ready() -> dict[str, object] | JSONResponse:
    """Check database connectivity and schema validity, returning readiness status."""
    checks: dict[str, str] = {
        "database": "pass",
        "schema": "pass",
    }
    details: dict[str, list[str]] = {
        "schema_issues": [],
    }

    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
    except SQLAlchemyError as error:  # pragma: no cover - defensive runtime capture
        checks["database"] = "fail"
        details["database_error"] = [str(error)]

    required_schema: dict[str, set[str]] = build_required_schema_from_models(Base, CRITICAL_SCHEMA_TABLES)
    outcome = validate_required_schema(engine, required_schema)
    if not outcome.ok:
        checks["schema"] = "fail"
        details["schema_issues"] = outcome.issues

    is_ready = all(status == "pass" for status in checks.values())
    payload: dict[str, object] = {
        "status": "ready" if is_ready else "not_ready",
        "checks": checks,
        "details": details,
    }
    if is_ready:
        return payload

    return JSONResponse(status_code=503, content=payload)