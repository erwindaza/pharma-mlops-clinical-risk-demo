from __future__ import annotations

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

import joblib
import pandas as pd
from sklearn.metrics import classification_report, roc_auc_score

from training.data_generator import DATA_PATH
from training.features import split_features_target


def evaluate(model_path: Path = Path("artifacts/model.pkl"), data_path: Path = DATA_PATH) -> dict:
    artifact = joblib.load(model_path)
    df = pd.read_csv(data_path)
    x, y = split_features_target(df)
    probabilities = artifact["model"].predict_proba(x)[:, 1]
    predictions = (probabilities >= 0.5).astype(int)
    return {
        "roc_auc": float(roc_auc_score(y, probabilities)),
        "classification_report": classification_report(y, predictions, output_dict=True),
    }


if __name__ == "__main__":
    print(evaluate())
