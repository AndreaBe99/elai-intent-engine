import pytest

from elai_intent_engine.models import PredictionsRecord
from elai_intent_engine.repositories.predictions import PredictionsRepository


@pytest.mark.asyncio
async def test_save_prediction_inserts_document():
    """Verify that save_prediction correctly persists data using Beanie."""
    repo = PredictionsRepository()
    input_data = {"eta": 25, "cliente_attivo": "SI"}
    output_data = {"probability": 0.5, "label": "OK"}

    await repo.save_prediction(input_data, output_data)

    # Check database
    records = await PredictionsRecord.find_all().to_list()
    assert len(records) == 1
    assert records[0].input_data == input_data
    assert records[0].output_data == output_data


@pytest.mark.asyncio
async def test_save_prediction_batch():
    """Verify that save_prediction handles batch data lists."""
    repo = PredictionsRepository()
    input_data = [{"eta": 25}, {"eta": 30}]
    output_data = [{"label": "OK"}, {"label": "NO_ACQUISTO"}]

    await repo.save_prediction(input_data, output_data)

    records = await PredictionsRecord.find_all().to_list()
    assert len(records) == 1
    assert records[0].input_data == input_data
    assert records[0].output_data == output_data
