from pydantic import BaseModel, Field


class PredictionRequest(BaseModel):
    age: int = Field(ge=18, le=95)
    sex_encoded: int = Field(ge=0, le=1)
    prior_conditions_count: int = Field(ge=0, le=20)
    baseline_lab_score: float = Field(ge=0, le=1)
    lab_score_delta: float = Field(ge=-1, le=1)
    visit_adherence_rate: float = Field(ge=0, le=1)
    site_delay_days: int = Field(ge=0, le=120)
    protocol_complexity_score: float = Field(ge=0, le=10)
    previous_dropout_signal: int = Field(ge=0, le=1)
    medication_count: int = Field(ge=0, le=30)
    adverse_event_history_count: int = Field(ge=0, le=20)
    country_risk_index: float = Field(ge=0, le=1)
    site_enrollment_rate: float = Field(ge=0, le=1)
    days_since_last_visit: int = Field(ge=0, le=365)


class PredictionResponse(BaseModel):
    risk_score: float
    risk_class: str
    model_version: str
    explanation: str
