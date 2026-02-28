from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from loguru import logger
from pydantic import Field

from elai_intent_engine.api.dependencies import get_predictions_service
from elai_intent_engine.models import PredictionInput, PredictionOutput
from elai_intent_engine.services.api.predictions import PredictionsService
from elai_intent_engine.utils.config import settings

router = APIRouter()

# Type for max MAX_BATCH_SIZE items in a batch prediction
BatchPredictionInput = Annotated[
    list[PredictionInput],
    Field(
        min_length=1,
        max_length=settings.max_batch_size,
    ),
]
BatchPredictionOutput = Annotated[
    list[PredictionOutput],
    Field(
        min_length=1,
        max_length=settings.max_batch_size,
    ),
]


@router.post(
    "/predict",
    response_model=PredictionOutput | BatchPredictionOutput,
    summary="Predict customer purchase propensity",
)
async def predict(
    payload: PredictionInput | BatchPredictionInput,
    predictions_service: Annotated[
        PredictionsService, Depends(get_predictions_service)
    ],
) -> PredictionOutput | BatchPredictionOutput:
    """
    Endpoint for performing predictions based on input customer data.

    Accepts either a single dictionary or a JSON array of up to 1000 objects.
    Each input includes the model features, processes them, returns probabilities
    with labels, and persists both input and output asynchronously in MongoDB.

    Args:
        payload (PredictionInput | BatchPredictionInput): Input data for prediction.
        predictions_service (PredictionsService): Service for processing predictions.

    Returns:
        PredictionOutput | BatchPredictionOutput: Prediction result or list of results.

    Raises:
        HTTPException: If an error occurs during prediction processing.
    """
    try:
        result = await predictions_service.process_prediction(payload)
        return result
    except Exception as e:
        logger.exception("Unhandled error during /predict: {}", e)
        raise HTTPException(status_code=500, detail=str(e))
