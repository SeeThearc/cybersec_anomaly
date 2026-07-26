"""FastAPI application bootstrap."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from app.api import router
from app.config import get_settings
from app.ml.predict import PredictionPipeline

logger = logging.getLogger(__name__)
settings = get_settings()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Eagerly load ML models on startup
    logger.info("Starting up: Loading ML models globally...")
    try:
        app.state.predictor = PredictionPipeline()
        logger.info("Successfully loaded ML pipeline into memory.")
    except Exception as e:
        logger.error(f"Failed to load ML pipeline: {str(e)}")
        app.state.predictor = None
        
    yield
    # Cleanup on shutdown (if any)
    logger.info("Shutting down...")

app = FastAPI(
    title="UEBA System",
    description="AI-Driven User & Entity Behavior Analytics Platform",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Since it's a hackathon project, allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
