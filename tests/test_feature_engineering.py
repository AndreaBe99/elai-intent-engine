from elai_intent_engine.models import PredictionInput
from elai_intent_engine.services.feature_engineering import FeatureEngineeringService


def test_preprocess_drops_nome():
    """Verify that the 'nome' feature is properly dropped from the dataset."""
    inputs = [PredictionInput(nome="Mario Rossi", eta=30, cliente_attivo="SI")]
    df = FeatureEngineeringService.preprocess(inputs)

    assert "nome" not in df.columns
    assert "eta" in df.columns
    assert "cliente_attivo_bin" in df.columns
    assert "cliente_attivo" not in df.columns


def test_preprocess_binarizes_cliente_attivo():
    """Verify that 'cliente_attivo' is correctly binarized into 'cliente_attivo_bin'."""
    inputs = [
        PredictionInput(eta=30, cliente_attivo="SI"),
        PredictionInput(eta=20, cliente_attivo="NO"),
        PredictionInput(eta=40, cliente_attivo=None),  # Uses default "NO"
        PredictionInput(eta=50, cliente_attivo="si"),  # Case insensitive
    ]
    df = FeatureEngineeringService.preprocess(inputs)

    # "SI" -> 1, "NO" -> 0, default -> 0
    assert df["cliente_attivo_bin"].tolist() == [1, 0, 0, 1]


def test_preprocess_preserves_eta():
    """Verify that 'eta' passes through without modification."""
    inputs = [PredictionInput(eta=18.5, cliente_attivo="SI")]
    df = FeatureEngineeringService.preprocess(inputs)

    assert df["eta"].iloc[0] == 18.5


def test_feature_ordering():
    """Verify that features are in the order expected by the model."""
    inputs = [PredictionInput(eta=30, cliente_attivo="SI")]
    df = FeatureEngineeringService.preprocess(inputs)

    assert df.columns.tolist() == ["eta", "cliente_attivo_bin"]
