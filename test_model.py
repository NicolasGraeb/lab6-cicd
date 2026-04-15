import numpy as np
import pytest
from sklearn.metrics import accuracy_score

from main import X, y, model


@pytest.fixture()
def predictions():
    preds = model.predict(X)
    return preds


def test_predictions_not_none(predictions):
    assert predictions is not None, "Predictions should not be None."


def test_predictions_length(predictions):
    assert len(predictions) > 0, "Predictions should contain at least one element."
    assert len(predictions) == len(y), "Predictions length should match labels length."


def test_predictions_value_range(predictions):
    unique_preds = np.unique(predictions)
    assert set(unique_preds).issubset({0, 1, 2}), "Predictions should only contain classes 0, 1, 2."


def test_model_accuracy():
    preds = model.predict(X)
    accuracy = accuracy_score(y, preds)
    assert accuracy >= 0.7, f"Model accuracy too low: {accuracy:.3f}. Expected at least 0.7."
