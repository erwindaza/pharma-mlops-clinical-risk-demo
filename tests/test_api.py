from fastapi.testclient import TestClient

from app.main import app


def test_health():
    with TestClient(app) as client:
        response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_predict(example_payload):
    with TestClient(app) as client:
        response = client.post("/predict", json=example_payload)
    assert response.status_code == 200
    body = response.json()
    assert 0 <= body["risk_score"] <= 1
    assert body["risk_class"] in {"low", "medium", "high"}
    assert body["model_version"] == "v1"
