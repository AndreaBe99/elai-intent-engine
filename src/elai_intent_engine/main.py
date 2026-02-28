from contextlib import asynccontextmanager

from fastapi import FastAPI
from loguru import logger

from elai_intent_engine.api.routers import predictions_router
from elai_intent_engine.services.database import DatabaseService
from elai_intent_engine.services.ml import MLService
from elai_intent_engine.utils.logging import configure_logging


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    FastAPI lifecycle context manager.
    Handles startup configuration (logging, DB init, ML loading)
    and teardown routines (graceful connection close).
    """
    # 0. Configure loguru (console + rotating file)
    configure_logging()
    logger.info("Starting AI Predictive API...")

    # 1. Connect to MongoDB and initialise Beanie
    logger.info("Connecting to MongoDB and initialising Beanie...")
    await DatabaseService.connect()
    logger.info("Database ready.")

    # 2. Preload the scikit-learn model
    logger.info("Loading ML model...")
    MLService.load_model()
    logger.info("ML model loaded successfully.")

    yield

    # Shutdown
    logger.info("Shutting down — closing MongoDB connection pool.")
    DatabaseService.close()
    logger.info("Shutdown complete.")


app = FastAPI(
    title="ELAI Intent Engine API",
    description="API for machine learning batch and real-time predictions.",
    version="1.0.0",
    lifespan=lifespan,
)

# Attach API endpoints
app.include_router(predictions_router)
