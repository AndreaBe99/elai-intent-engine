from loguru import logger

from elai_intent_engine.models import PredictionInput, PredictionOutput
from elai_intent_engine.repositories.predictions import PredictionsRepository
from elai_intent_engine.services.ml import MLService


class PredictionsService:
    """
    Application service that orchestrates the flow of data between the
    API controllers, the ML prediction engine, and the Database repository.
    """

    def __init__(self, repository: PredictionsRepository) -> None:
        """
        Initialize the service.

        Args:
            repository: Data access object for the predictions collection.
        """
        self.repository = repository

    async def process_prediction(
        self, payload: PredictionInput | list[PredictionInput]
    ) -> PredictionOutput | list[PredictionOutput]:
        """
        Process single or batch predictions, format the result, and save to DB.

        Args:
            payload: A single PredictionInput or a list of them.

        Returns:
            A PredictionOutput or a list of them corresponding to the input.

        Raises:
            RuntimeError: If the model has not been loaded or if preprocessing or prediction fails.
        """
        # Check if the payload is a list (batch) or a single item
        if isinstance(payload, list):
            is_batch = True
            inputs = payload
        else:
            is_batch = False
            inputs = [payload]

        batch_size = len(inputs)

        logger.info("Processing {} prediction(s). batch={}", batch_size, is_batch)

        # Execute ML prediction
        outputs: list[PredictionOutput] = MLService.predict_batch(inputs)

        # Prepare data for storage
        input_dump = [item.model_dump() for item in inputs]
        output_dump = [item.model_dump() for item in outputs]

        # Persist asynchronously
        await self.repository.save_prediction(
            input_data=input_dump if is_batch else input_dump[0],
            output_data=output_dump if is_batch else output_dump[0],
        )
        logger.debug("Prediction record persisted to MongoDB.")

        # Return response in the appropriate shape
        return outputs if is_batch else outputs[0]
