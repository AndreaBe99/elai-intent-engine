from datetime import datetime, timezone
from typing import Any

from beanie import Document
from pydantic import Field


class PredictionsRecord(Document):
    """
    Beanie document model for a stored prediction record to the 'predictions'
    MongoDB collection.

    Attributes:
        timestamp: UTC datetime of the prediction.
        input_data: The original input (single dict or list of dicts).
        output_data: The corresponding output (single dict or list of dicts).
    """

    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    input_data: dict[str, Any] | list[dict[str, Any]]
    output_data: dict[str, Any] | list[dict[str, Any]]

    class Settings:
        name = "predictions"
