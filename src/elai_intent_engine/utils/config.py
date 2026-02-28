from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables and .env file.

    Attributes:
        mongodb_uri: Connection string for MongoDB.
        mongodb_db_name: Name of the database for storing predictions.
        api_host: Hostname or IP to bind the API to.
        api_port: Port to expose the API on.
        model_path: Path to the pickled ML model file.
        max_batch_size: Maximum number of records to process in a single batch.
        decision_threshold: Threshold for classifying a prediction as positive.
        probability_round: Number of decimal places to round probabilities to.
    """

    # MongoDB
    mongodb_uri: str = "mongodb://localhost:27017/"
    mongodb_db_name: str = "predictions_db"

    # API
    api_host: str = "0.0.0.0"
    api_port: int = 5000

    # ML
    model_path: str = "resources/models/model.pkl"
    max_batch_size: int = 1000
    decision_threshold: float = 0.10
    probability_round: int = 4

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        # Allow extra fields in case the environment has them
        extra="ignore",
        # Allow fields starting with 'model_' (like model_path)
        protected_namespaces=(),
    )


# Instantiate settings to be imported by the application
settings = Settings()
