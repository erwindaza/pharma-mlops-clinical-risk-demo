from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Protocol

import joblib
import numpy as np


class ProbabilityModel(Protocol):
    def predict_proba(self, features: np.ndarray) -> np.ndarray: ...


@dataclass
class LoadedModel:
    model: ProbabilityModel
    metadata: dict
    loaded_from_artifact: bool


class HeuristicRiskModel:
    """Deterministic fallback so the API is testable before training artifacts exist."""

    def predict_proba(self, features: np.ndarray) -> np.ndarray:
        row = features[0]
        score = (
            0.018 * (row[0] - 45)
            + 0.18 * row[2]
            + 1.2 * abs(row[4])
            + 1.8 * (1 - row[5])
            + 0.08 * row[6]
            + 0.24 * row[7]
            + 1.1 * row[8]
            + 0.16 * row[10]
            + 0.8 * row[11]
            + 0.9 * (1 - row[12])
            + 0.012 * row[13]
            - 4.2
        )
        probability = 1 / (1 + np.exp(-score))
        return np.array([[1 - probability, probability]])


def load_model(model_path: Path, model_version: str) -> LoadedModel:
    if model_path.exists():
        artifact = joblib.load(model_path)
        return LoadedModel(
            model=artifact["model"],
            metadata=artifact.get(
                "metadata",
                {
                    "model_name": "clinical_risk_xgboost",
                    "model_version": model_version,
                    "framework": "xgboost",
                },
            ),
            loaded_from_artifact=True,
        )
    return LoadedModel(
        model=HeuristicRiskModel(),
        metadata={
            "model_name": "clinical_risk_heuristic_fallback",
            "model_version": model_version,
            "framework": "deterministic-python",
        },
        loaded_from_artifact=False,
    )
