from typing import AsyncGenerator

from beanie import init_beanie
from httpx import ASGITransport, AsyncClient
from mongomock_motor import AsyncMongoMockClient
import pytest_asyncio

from elai_intent_engine.main import app
from elai_intent_engine.models import PredictionsRecord


@pytest_asyncio.fixture(autouse=True)
async def init_test_db() -> AsyncGenerator:
    """
    Initialise Beanie with an Async Mongo Mock client.
    This runs automatically for every test to ensure a clean state.
    """
    client = AsyncMongoMockClient()
    await init_beanie(
        database=client.get_database("test_db"),
        document_models=[PredictionsRecord],
    )
    yield
    # Clean up collections after each test if needed
    await PredictionsRecord.delete_all()


@pytest_asyncio.fixture
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    """
    Fixture for making async requests to the FastAPI application.
    """
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        yield client
