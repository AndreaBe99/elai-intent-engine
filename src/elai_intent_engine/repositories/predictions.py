from elai_intent_engine.models import PredictionsRecord


class PredictionsRepository:
    """Repository layer for persisting prediction records via Beanie."""

    async def save_prediction(
        self,
        input_data: dict | list[dict],
        output_data: dict | list[dict],
    ) -> None:
        """
        Persist a single prediction record into the MongoDB collection.

        Args:
            input_data: The raw input dict or list of dicts.
            output_data: The raw output dict or list of dicts.
        """
        record = PredictionsRecord(
            input_data=input_data,
            output_data=output_data,
        )
        await record.insert()
