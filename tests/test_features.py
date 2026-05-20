import numpy as np

from app.features import FEATURE_COLUMNS, request_to_feature_array
from training.data_generator import generate_synthetic_data
from training.features import split_features_target


def test_request_feature_order(example_payload):
    features = request_to_feature_array(example_payload)
    assert features.shape == (1, len(FEATURE_COLUMNS))
    assert np.isclose(features[0][0], example_payload["age"])


def test_generated_data_has_training_columns():
    df = generate_synthetic_data(rows=50, seed=7)
    x, y = split_features_target(df)
    assert x.shape[0] == 50
    assert set(y.unique()).issubset({0, 1})
