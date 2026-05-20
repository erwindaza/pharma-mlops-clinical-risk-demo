from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

DATA_PATH = Path("data/synthetic_clinical_trial_risk.csv")


def generate_synthetic_data(rows: int = 2500, seed: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    df = pd.DataFrame(
        {
            "age": rng.integers(18, 86, rows),
            "sex_encoded": rng.integers(0, 2, rows),
            "prior_conditions_count": rng.poisson(2.0, rows).clip(0, 12),
            "baseline_lab_score": rng.beta(5, 4, rows).clip(0, 1),
            "lab_score_delta": rng.normal(0, 0.11, rows).clip(-0.6, 0.6),
            "visit_adherence_rate": rng.beta(8, 2, rows).clip(0, 1),
            "site_delay_days": rng.gamma(2.0, 2.8, rows).astype(int).clip(0, 60),
            "protocol_complexity_score": rng.normal(5.4, 1.8, rows).clip(0, 10),
            "previous_dropout_signal": rng.binomial(1, 0.18, rows),
            "medication_count": rng.poisson(3.2, rows).clip(0, 18),
            "adverse_event_history_count": rng.poisson(0.8, rows).clip(0, 10),
            "country_risk_index": rng.beta(2.5, 4.0, rows).clip(0, 1),
            "site_enrollment_rate": rng.beta(5, 3, rows).clip(0, 1),
            "days_since_last_visit": rng.gamma(3.0, 7.5, rows).astype(int).clip(0, 180),
        }
    )
    logit = (
        0.018 * (df["age"] - 45)
        + 0.20 * df["prior_conditions_count"]
        + 1.4 * df["lab_score_delta"].abs()
        + 2.1 * (1 - df["visit_adherence_rate"])
        + 0.085 * df["site_delay_days"]
        + 0.25 * df["protocol_complexity_score"]
        + 1.05 * df["previous_dropout_signal"]
        + 0.13 * df["adverse_event_history_count"]
        + 0.85 * df["country_risk_index"]
        + 0.75 * (1 - df["site_enrollment_rate"])
        + 0.01 * df["days_since_last_visit"]
        - 4.4
    )
    probability = 1 / (1 + np.exp(-logit))
    df["risk_label"] = rng.binomial(1, probability)
    return df


def main() -> None:
    DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    generate_synthetic_data().to_csv(DATA_PATH, index=False)
    print(f"Wrote synthetic dataset to {DATA_PATH}")


if __name__ == "__main__":
    main()
