from typing import Annotated

from fastapi import Depends

from elai_intent_engine.repositories.predictions import PredictionsRepository
from elai_intent_engine.services.api import PredictionsService


def get_predictions_repository() -> PredictionsRepository:
    """
    Dependency provider for the PredictionsRepository.
    Beanie manages the connection globally, so no session needs to be injected.
    """
    return PredictionsRepository()


def get_predictions_service(
    repository: Annotated[PredictionsRepository, Depends(get_predictions_repository)],
) -> PredictionsService:
    """
    Dependency provider for the PredictionsService.
    Builds the service using the injected repository.
    """
    return PredictionsService(repository)
