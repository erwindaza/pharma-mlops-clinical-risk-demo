from pathlib import Path

from training.data_generator import generate_synthetic_data
from training.train import train


def test_training_smoke(tmp_path, monkeypatch):
    data_path = tmp_path / "synthetic.csv"
    artifact_path = tmp_path / "model.pkl"
    generate_synthetic_data(rows=120, seed=11).to_csv(data_path, index=False)
    monkeypatch.chdir(tmp_path)
    metadata = train(Path("synthetic.csv"), Path("model.pkl"))
    assert artifact_path.exists()
    assert metadata["metrics"]["roc_auc"] >= 0.5
