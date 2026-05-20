import pytest


@pytest.fixture
def example_payload():
    return {
        "age": 58,
        "sex_encoded": 1,
        "prior_conditions_count": 3,
        "baseline_lab_score": 0.62,
        "lab_score_delta": 0.12,
        "visit_adherence_rate": 0.78,
        "site_delay_days": 6,
        "protocol_complexity_score": 7.4,
        "previous_dropout_signal": 0,
        "medication_count": 4,
        "adverse_event_history_count": 1,
        "country_risk_index": 0.35,
        "site_enrollment_rate": 0.66,
        "days_since_last_visit": 21,
    }
