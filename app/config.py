from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_env: str = Field(default="local", alias="APP_ENV")
    model_path: Path = Field(default=Path("artifacts/model.pkl"), alias="MODEL_PATH")
    model_version: str = Field(default="v1", alias="MODEL_VERSION")
    mlflow_tracking_uri: str = Field(default="file:./mlruns", alias="MLFLOW_TRACKING_URI")
    aws_region: str = Field(default="us-east-1", alias="AWS_REGION")
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()
