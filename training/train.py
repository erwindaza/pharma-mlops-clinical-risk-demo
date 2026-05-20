from __future__ import annotations

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

import joblib
import mlflow
import pandas as pd
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, roc_auc_score
from sklearn.model_selection import train_test_split

from training.data_generator import DATA_PATH, generate_synthetic_data
from training.features import FEATURE_COLUMNS, split_features_target
from training.registry import write_model_metadata

ARTIFACT_PATH = Path("artifacts/model.pkl")
SEED = 42


def build_model():
    try:
        from xgboost import XGBClassifier

        return XGBClassifier(
            n_estimators=80,
            max_depth=3,
            learning_rate=0.08,
            subsample=0.9,
            colsample_bytree=0.9,
            eval_metric="logloss",
            random_state=SEED,
        ), "xgboost"
    except Exception:
        from sklearn.ensemble import GradientBoostingClassifier

        return GradientBoostingClassifier(random_state=SEED), "sklearn-gradient-boosting"


def train(data_path: Path = DATA_PATH, artifact_path: Path = ARTIFACT_PATH) -> dict:
    if not data_path.exists():
        data_path.parent.mkdir(parents=True, exist_ok=True)
        generate_synthetic_data().to_csv(data_path, index=False)

    df = pd.read_csv(data_path)
    x, y = split_features_target(df)
    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.2, random_state=SEED, stratify=y
    )

    model, framework = build_model()
    mlflow.set_tracking_uri("file:./mlruns")
    mlflow.set_experiment("clinical-risk-scoring")
    with mlflow.start_run() as run:
        model.fit(x_train, y_train)
        probabilities = model.predict_proba(x_test)[:, 1]
        predictions = (probabilities >= 0.5).astype(int)
        metrics = {
            "roc_auc": float(roc_auc_score(y_test, probabilities)),
            "f1": float(f1_score(y_test, predictions)),
            "precision": float(precision_score(y_test, predictions, zero_division=0)),
            "recall": float(recall_score(y_test, predictions, zero_division=0)),
            "accuracy": float(accuracy_score(y_test, predictions)),
        }
        metadata = {
            "model_name": "clinical_risk_xgboost",
            "model_version": "v1",
            "framework": framework,
            "dataset": str(data_path),
            "features": FEATURE_COLUMNS,
            "mlflow_run_id": run.info.run_id,
            "seed": SEED,
            "metrics": metrics,
        }
        mlflow.log_params({"seed": SEED, "rows": len(df), "framework": framework})
        mlflow.log_metrics(metrics)
        artifact_path.parent.mkdir(parents=True, exist_ok=True)
        joblib.dump({"model": model, "metadata": metadata}, artifact_path)
        mlflow.log_artifact(str(artifact_path))
        write_model_metadata(metadata)
    return metadata


def main() -> None:
    metadata = train()
    print(f"Model written to {ARTIFACT_PATH}")
    print(metadata["metrics"])


if __name__ == "__main__":
    main()
