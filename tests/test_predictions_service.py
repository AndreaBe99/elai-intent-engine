from unittest.mock import AsyncMock, patch

import pytest

from elai_intent_engine.models import PredictionInput, PredictionOutput
from elai_intent_engine.services.api.predictions import PredictionsService
from elai_intent_engine.utils.enums import PredictionLabels


@pytest.fixture
def mock_repo():
    return AsyncMock()


@pytest.mark.asyncio
async def test_process_prediction_orchestration(mock_repo):
    """Verify that PredictionsService correctly orchestrates ML and Repository calls."""
    service = PredictionsService(mock_repo)
    payload = PredictionInput(eta=30, cliente_attivo="SI")

    # Mock MLService.predict_batch
    mock_output = [PredictionOutput(probability=0.8, label=PredictionLabels.OK)]
    with patch(
        "elai_intent_engine.services.api.predictions.MLService.predict_batch",
        return_value=mock_output,
    ):
        result = await service.process_prediction(payload)

    # Assertions
    assert isinstance(result, PredictionOutput)
    assert result.label == PredictionLabels.OK.value

    # Verify repository was called
    mock_repo.save_prediction.assert_called_once()
    args, kwargs = mock_repo.save_prediction.call_args
    assert kwargs["input_data"]["eta"] == 30
    assert kwargs["output_data"]["label"] == PredictionLabels.OK.value


@pytest.mark.asyncio
async def test_process_prediction_batch(mock_repo):
    """Verify orchestration for batch inputs."""
    service = PredictionsService(mock_repo)
    payload = [PredictionInput(eta=20), PredictionInput(eta=50)]

    mock_output = [
        PredictionOutput(probability=0.1, label=PredictionLabels.NO_ACQUISTO),
        PredictionOutput(probability=0.9, label=PredictionLabels.OK),
    ]
    with patch(
        "elai_intent_engine.services.api.predictions.MLService.predict_batch",
        return_value=mock_output,
    ):
        result = await service.process_prediction(payload)

    assert isinstance(result, list)
    assert len(result) == 2
    assert result[0].label == PredictionLabels.NO_ACQUISTO.value

    mock_repo.save_prediction.assert_called_once()
    _, kwargs = mock_repo.save_prediction.call_args
    assert isinstance(kwargs["input_data"], list)
    assert len(kwargs["input_data"]) == 2
