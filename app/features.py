from __future__ import annotations

from collections.abc import Mapping

import numpy as np

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


def request_to_feature_array(payload: Mapping[str, float | int]) -> np.ndarray:
    return np.array([[float(payload[column]) for column in FEATURE_COLUMNS]], dtype=float)


def risk_explanation(payload: Mapping[str, float | int]) -> str:
    drivers = []
    if float(payload["visit_adherence_rate"]) < 0.8:
        drivers.append("low visit adherence")
    if int(payload["site_delay_days"]) >= 5:
        drivers.append("site delay")
    if float(payload["protocol_complexity_score"]) >= 7:
        drivers.append("protocol complexity")
    if abs(float(payload["lab_score_delta"])) >= 0.1:
        drivers.append("lab deviation")
    if int(payload["previous_dropout_signal"]) == 1:
        drivers.append("previous dropout signal")
    if not drivers:
        return "No dominant operational risk driver crossed the configured threshold."
    return "Elevated operational risk based on " + ", ".join(drivers) + "."
