from __future__ import annotations

import pandas as pd

FEATURE_COLUMNS = [
    "age",
    "sex_encoded",
    "prior_conditions_count",
    "baseline_lab_score",
    "lab_score_delta",
    "visit_adherence_rate",
    "site_delay_days",
    "protocol_complexity_score",
    "previous_dropout_signal",
    "medication_count",
    "adverse_event_history_count",
    "country_risk_index",
    "site_enrollment_rate",
    "days_since_last_visit",
]

TARGET_COLUMN = "risk_label"


def split_features_target(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series]:
    missing = set(FEATURE_COLUMNS + [TARGET_COLUMN]) - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")
    return df[FEATURE_COLUMNS], df[TARGET_COLUMN]
