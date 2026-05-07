"""API router aggregating all versioned route modules."""

from fastapi import APIRouter
from backend.api.auth import router as auth_router
from backend.api.health import router as health_router
from backend.api.assistant import router as assistant_router
from backend.api.alerts import router as alerts_router
from backend.api.feedback import router as feedback_router
from backend.api.risk import router as risk_router
from backend.api.summaries import router as summaries_router
from backend.api.users import router as users_router
from backend.api.forecast import router as forecast_router
from backend.api.packing import router as packing_router


api_router = APIRouter(prefix="/api/v1")
api_router.include_router(health_router)
api_router.include_router(auth_router)
api_router.include_router(assistant_router)
api_router.include_router(alerts_router)
api_router.include_router(feedback_router)
api_router.include_router(risk_router)
api_router.include_router(summaries_router)
api_router.include_router(users_router)
api_router.include_router(forecast_router)
api_router.include_router(packing_router)