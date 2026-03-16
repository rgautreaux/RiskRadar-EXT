"""
RiskRadar - FastAPI entry point.

This file:
  1. Creates the FastAPI app with lifespan (startup/shutdown).
  2. On startup: initializes the database and starts APScheduler.
  3. Mounts the REST API at /api/v1/* (see api/router.py).
  4. Serves the HTML frontend at / using Jinja2 templates.
  5. Serves static CSS/JS files from /static/.

HOW TO RUN:
  cd backend
  python -m uvicorn main:app --reload --port 8000

Then open http://localhost:8000 in your browser for the web frontend,
or http://localhost:8000/docs for the Swagger API docs.
"""

import logging
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from db.init_db import init_database
from scrapers.scheduler import start_scheduler
from api.router import api_router
from frontend.routes import router as frontend_router

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(name)s %(levelname)s %(message)s")

BASE_DIR = Path(__file__).resolve().parent


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup: init DB + start scrapers. Shutdown: stop scheduler."""
    init_database()
    scheduler = start_scheduler()
    yield
    scheduler.shutdown()


app = FastAPI(title="RiskRadar API", version="1.0.0", lifespan=lifespan)

# --- CORS middleware -------------------------------------------------------
# Allows the React Native app (or any frontend) to call the API.
# TODO: Before production, replace "*" with your actual frontend origins.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Static files (CSS, JS) -----------------------------------------------
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")

# --- API routes (REST JSON) ------------------------------------------------
app.include_router(api_router)

# --- Frontend routes (HTML pages) ------------------------------------------
# These must be included AFTER the API routes so /api/v1/* takes priority.
app.include_router(frontend_router)
