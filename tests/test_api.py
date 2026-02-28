from unittest.mock import patch

from httpx import AsyncClient
import pytest

from elai_intent_engine.models import PredictionOutput
from elai_intent_engine.utils.enums import PredictionLabels


@pytest.fixture(autouse=True)
def mock_ml_service():
    """Globally mock MLService methods for API tests to avoid loading real model."""
    with (
        patch("elai_intent_engine.services.ml.MLService.load_model") as mock_load,
        patch("elai_intent_engine.services.ml.MLService.predict_batch") as mock_predict,
    ):
        mock_predict.return_value = [PredictionOutput(probability=0.5, label=PredictionLabels.OK)]
        yield (mock_load, mock_predict)


@pytest.mark.asyncio
async def test_predict_single_valid(async_client: AsyncClient):
    """Test single valid record through the API."""
    payload = {"nome": "Mario", "eta": 30, "cliente_attivo": "SI"}
    response = await async_client.post("/predict", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data["probability"] == 0.5
    assert data["label"] == PredictionLabels.OK.value


@pytest.mark.asyncio
async def test_predict_batch_valid(async_client: AsyncClient, mock_ml_service):
    """Test batch valid records."""
    _, mock_predict = mock_ml_service
    mock_predict.return_value = [
        PredictionOutput(probability=0.1, label=PredictionLabels.NO_ACQUISTO),
        PredictionOutput(probability=0.9, label=PredictionLabels.OK),
    ]

    payload = [{"eta": 20, "cliente_attivo": "NO"}, {"eta": 55, "cliente_attivo": "SI"}]
    response = await async_client.post("/predict", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 2
    assert data[0]["label"] == "NO_ACQUISTO"


@pytest.mark.asyncio
async def test_predict_invalid_age(async_client: AsyncClient):
    """Test Pydantic validation for age out of range."""
    payload = {"eta": 150}  # Max is 120
    response = await async_client.post("/predict", json=payload)

    assert response.status_code == 422
    assert "eta" in response.text


@pytest.mark.asyncio
async def test_predict_invalid_active_flag(async_client: AsyncClient):
    """Test Pydantic validation for invalid cliente_attivo flag."""
    payload = {"eta": 30, "cliente_attivo": "MAYBE"}
    response = await async_client.post("/predict", json=payload)

    assert response.status_code == 422
    assert "cliente_attivo" in response.text


@pytest.mark.asyncio
async def test_predict_batch_too_large(async_client: AsyncClient):
    """Test limit on batch size."""
    payload = [{"eta": 30}] * 1001
    response = await async_client.post("/predict", json=payload)

    assert response.status_code == 422
    assert "at most 1000 items" in response.text


@pytest.mark.asyncio
async def test_predict_internal_error(async_client: AsyncClient):
    """Test that internal errors are caught and logged."""
    payload = {"eta": 30}
    # We patch PredictionsService instead of MLService to simulate a generic failure in the service layer
    with patch(
        "elai_intent_engine.services.api.predictions.PredictionsService.process_prediction",
        side_effect=ValueError("Test Error"),
    ):
        response = await async_client.post("/predict", json=payload)

    assert response.status_code == 500
    assert "Test Error" in response.json()["detail"]
