from unittest.mock import MagicMock, patch

import pandas as pd
import pytest

from elai_intent_engine.models import PredictionInput, PredictionOutput
from elai_intent_engine.services.ml import MLService
from elai_intent_engine.utils.enums import PredictionLabels


@pytest.fixture
def mock_model():
    model = MagicMock()
    # Mock predict_proba to return 0.8 for the second class (OK)
    model.predict_proba.return_value = MagicMock(
        __getitem__=lambda self, idx: [[0.2, 0.8]][idx]
    )
    # Actually, a simpler way to mock numpy array slicing:
    import numpy as np

    model.predict_proba.return_value = np.array([[0.2, 0.8]])
    return model


def test_load_model():
    """Test model loading singleton pattern."""
    with patch("joblib.load") as mock_joblib_load:
        mock_joblib_load.return_value = MagicMock()

        # Reset singleton state for test
        MLService._model = None

        MLService.load_model("mock_path.pkl")
        MLService.load_model("mock_path.pkl")

        assert mock_joblib_load.call_count == 1
        assert MLService._model is not None


def test_predict_batch_success(mock_model):
    """Test successful batch prediction."""
    MLService._model = mock_model
    inputs = [PredictionInput(eta=30, cliente_attivo="SI")]

    # Mock FeatureEngineeringService.preprocess
    mock_df = pd.DataFrame({"eta": [30], "cliente_attivo_bin": [1]})
    with patch(
        "elai_intent_engine.services.ml.FeatureEngineeringService.preprocess",
        return_value=mock_df,
    ):
        results = MLService.predict_batch(inputs)

    assert len(results) == 1
    assert isinstance(results[0], PredictionOutput)
    assert results[0].probability == 0.8
    assert results[0].label == PredictionLabels.OK


def test_predict_batch_not_loaded():
    """Test error when model is not loaded."""
    MLService._model = None
    with pytest.raises(RuntimeError, match="Model is not loaded"):
        MLService.predict_batch([])
