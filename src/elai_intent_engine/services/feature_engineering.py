from loguru import logger
import pandas as pd

from elai_intent_engine.models import PredictionInput
from elai_intent_engine.utils.enums import FeatureNames


class FeatureEngineeringService:
    """
    Service responsible for transforming prediction inputs into a model-ready format.
    """

    @staticmethod
    def preprocess(data: list[PredictionInput]) -> pd.DataFrame:
        """
        Apply the feature engineering steps defined in the training report, i.e:

        - Drop the 'nome' feature
        - Keep the 'eta' feature as is
        - Binarize the 'cliente_attivo' feature into 'cliente_attivo_bin'
            - 'SI' -> 1
            - otherwise -> 0

        Args:
            data: List of validated input records.

        Returns:
            A pandas DataFrame ready for the model's predict_proba.
        """
        df = pd.DataFrame([item.model_dump() for item in data])

        # A. Feature 'nome' -> Drop
        if FeatureNames.NOME.value in df.columns:
            df = df.drop(columns=[FeatureNames.NOME.value])

        # B. Feature 'eta' -> None transformation needed, already numeric and model-ready

        # C. Feature 'cliente_attivo' -> Binarization
        if FeatureNames.CLIENTE_ATTIVO.value in df.columns:
            df[FeatureNames.CLIENTE_ATTIVO_BIN.value] = df[
                FeatureNames.CLIENTE_ATTIVO.value
            ].apply(lambda x: 1 if str(x).strip().upper() == "SI" else 0)
        else:
            # If not present somehow, default to 0
            df[FeatureNames.CLIENTE_ATTIVO_BIN.value] = 0

        # Ensure correct column order expected potentially by the model
        features = [
            FeatureNames.ETA.value,
            FeatureNames.CLIENTE_ATTIVO_BIN.value,
        ]
        logger.debug("Features passed to model: {}", features)
        df = df[features]

        return df
