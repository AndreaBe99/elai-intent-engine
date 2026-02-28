from beanie import init_beanie
from loguru import logger
from motor.motor_asyncio import AsyncIOMotorClient

from elai_intent_engine.models import PredictionsRecord
from elai_intent_engine.utils.config import settings


class DatabaseService:
    """
    MongoDB client and Beanie ODM initializer.
    Maintains a single AsyncIOMotorClient connection pool.
    """

    client: AsyncIOMotorClient | None = None

    @classmethod
    async def connect(cls) -> None:
        """
        Initialize the Motor connection pool and register Beanie document models.
        Must be awaited during application startup.
        """
        if cls.client is None:
            cls.client = AsyncIOMotorClient(settings.mongodb_uri)
            logger.debug("Motor client created. URI: {}", settings.mongodb_uri)

        await init_beanie(
            database=cls.client[settings.mongodb_db_name],
            document_models=[PredictionsRecord],
        )
        logger.info(
            "Beanie initialised. DB: {} | Collections: predictions",
            settings.mongodb_db_name,
        )

    @classmethod
    def close(cls) -> None:
        """Close the MongoDB connection pool."""
        if cls.client is not None:
            cls.client.close()
            cls.client = None
            logger.info("MongoDB connection pool closed.")
