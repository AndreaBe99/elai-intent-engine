from enum import StrEnum


class FeatureNames(StrEnum):
    """Feature names used in the prediction model."""

    NOME = "nome"
    ETA = "eta"
    CLIENTE_ATTIVO = "cliente_attivo"
    CLIENTE_ATTIVO_BIN = "cliente_attivo_bin"


class PredictionLabels(StrEnum):
    """Labels for prediction output."""

    OK = "OK"
    NO_ACQUISTO = "NO_ACQUISTO"
