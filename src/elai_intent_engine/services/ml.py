import warnings

import joblib
from loguru import logger

from elai_intent_engine.models import PredictionInput, PredictionOutput
from elai_intent_engine.services.feature_engineering import FeatureEngineeringService
from elai_intent_engine.utils.config import settings
from elai_intent_engine.utils.enums import PredictionLabels


class MLService:
    """
    Service responsible for loading the ML model, preprocessing data,
    and performing predictions.

    It operates as a singleton to avoid reloading the model on every request.
    """

    _model = None

    @classmethod
    def load_model(cls, model_path: str | None = None) -> None:
        """
        Load the scikit-learn model from the disk.

        Args:
            model_path: Path to the pickled model file.
        """
        if cls._model is None:
            if model_path is None:
                model_path = settings.model_path
            logger.info("Loading model from '{}'...", model_path)
            # Load the model and ignore any potential sklearn version warnings
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                cls._model = joblib.load(model_path)
            logger.info("Model loaded. Type: {}", type(cls._model).__name__)

    @classmethod
    def predict_batch(cls, inputs: list[PredictionInput]) -> list[PredictionOutput]:
        """
        Preprocess and classify a batch of records using the loaded model.

        Args:
            inputs: List of prediction input schemas.

        Returns:
            List of PredictionOutput schemas.

        Raises:
            RuntimeError: If the model has not been loaded or if preprocessing or prediction fails.
        """
        if cls._model is None:
            raise RuntimeError(
                "Model is not loaded. Please call load_model() on startup."
            )

        logger.debug("Running prediction on {} record(s).", len(inputs))
        try:
            df_processed = FeatureEngineeringService.preprocess(inputs)
        except Exception as e:
            logger.exception("Error during preprocessing: {}", e)
            raise RuntimeError("Error during preprocessing")

        try:
            # Get probabilities for the positive class (class 1, i.e. "OK", second column)
            probabilities = cls._model.predict_proba(df_processed)[:, 1]
        except Exception as e:
            logger.exception("Error during prediction: {}", e)
            raise RuntimeError("Error during prediction")

        results = []
        for prob in probabilities:
            label = (
                PredictionLabels.OK
                if prob >= settings.decision_threshold
                else PredictionLabels.NO_ACQUISTO
            )
            results.append(
                PredictionOutput(
                    probability=round(float(prob), settings.probability_round),
                    label=label,
                )
            )

        ok_count = sum(1 for r in results if r.label == PredictionLabels.OK)
        logger.debug(
            "Prediction complete. {}={} | {}={} | threshold={}",
            PredictionLabels.OK.value,
            ok_count,
            PredictionLabels.NO_ACQUISTO.value,
            len(results) - ok_count,
            settings.decision_threshold,
        )
        return results
