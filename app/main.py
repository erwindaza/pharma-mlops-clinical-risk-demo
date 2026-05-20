from __future__ import annotations

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.config import get_settings
from app.features import request_to_feature_array, risk_explanation
from app.model_loader import LoadedModel, load_model
from app.monitoring import configure_logging, service_metrics
from app.schemas import PredictionRequest, PredictionResponse

settings = get_settings()
configure_logging(settings.log_level)
logger = logging.getLogger("clinical-risk-api")
runtime: dict[str, LoadedModel] = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    runtime["model"] = load_model(settings.model_path, settings.model_version)
    logger.info(
        "model_loaded",
        extra={
            "model_path": str(settings.model_path),
            "loaded_from_artifact": runtime["model"].loaded_from_artifact,
        },
    )
    yield


app = FastAPI(
    title="Clinical Trial Risk Scoring API",
    version="0.1.0",
    description="Educational MLOps demo API using synthetic clinical trial risk features.",
    lifespan=lifespan,
)


@app.get("/health")
def health() -> dict:
    return {
        "status": "ok",
        "service": "clinical-risk-api",
        "model_loaded": "model" in runtime,
    }


@app.get("/metadata")
def metadata() -> dict:
    loaded = runtime.get("model") or load_model(settings.model_path, settings.model_version)
    return {
        **loaded.metadata,
        "environment": settings.app_env,
        "loaded_from_artifact": loaded.loaded_from_artifact,
    }


@app.get("/metrics")
def metrics() -> dict:
    return {
        "prediction_count": service_metrics.prediction_count,
        "model_version": settings.model_version,
    }


@app.post("/predict", response_model=PredictionResponse)
def predict(payload: PredictionRequest) -> PredictionResponse:
    loaded = runtime.get("model") or load_model(settings.model_path, settings.model_version)
    payload_dict = payload.model_dump()
    features = request_to_feature_array(payload_dict)
    score = float(loaded.model.predict_proba(features)[0][1])
    service_metrics.prediction_count += 1
    risk_class = "high" if score >= 0.65 else "medium" if score >= 0.35 else "low"
    logger.info(
        "prediction_completed",
        extra={"risk_score": round(score, 4), "risk_class": risk_class},
    )
    return PredictionResponse(
        risk_score=round(score, 4),
        risk_class=risk_class,
        model_version=settings.model_version,
        explanation=risk_explanation(payload_dict),
    )
