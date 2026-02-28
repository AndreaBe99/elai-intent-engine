from pydantic import BaseModel, Field

from elai_intent_engine.utils.enums import PredictionLabels


class PredictionInput(BaseModel):
    """
    Schema for a single prediction request.

    Attributes:
        nome: Name of the customer (optional, max 100 chars).
        eta: Age of the customer (0-120).
        cliente_attivo: Active flag ("SI" or "NO").
    """

    nome: str | None = Field(
        default=None,
        max_length=100,
        description="Customer name.",
    )
    eta: float = Field(
        ...,
        ge=0,
        le=120,
        description="Customer age in years (must be between 0 and 120).",
    )
    cliente_attivo: str | None = Field(
        default="NO",
        pattern="^(?i:SI|NO)$",
        description="Active status flag. Accepted values: 'SI', 'NO' (case-insensitive).",
    )


class PredictionOutput(BaseModel):
    """
    Schema for a single prediction response.

    Attributes:
        probability: The predicted probability of purchase (0.0 to 1.0).
        label: The classification result.
    """

    probability: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Propensity probability.",
    )
    label: PredictionLabels = Field(
        ...,
        description="Classification label based on the threshold.",
    )
