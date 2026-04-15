from fastapi.testclient import TestClient

import main


client = TestClient(main.app)


def test_home_endpoint_returns_witaj():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "witaj"}


def test_health_endpoint_returns_ok():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_info_endpoint_has_expected_shape():
    response = client.get("/info")
    body = response.json()

    assert response.status_code == 200
    assert body["dataset"] == "iris"
    assert body["n_features"] == 4
    assert body["n_classes"] == 3
    assert body["model_type"] == "LogisticRegression"
    assert len(body["feature_names"]) == 4
    assert len(body["class_names"]) == 3


def test_predict_endpoint_returns_prediction_and_probability(monkeypatch):
    monkeypatch.setattr(main, "insert_prediction", lambda **kwargs: 123)

    payload = {
        "sepal_length": 5.1,
        "sepal_width": 3.5,
        "petal_length": 1.4,
        "petal_width": 0.2,
    }
    response = client.post("/predict", json=payload)
    body = response.json()

    assert response.status_code == 200
    assert body["prediction"] in ["setosa", "versicolor", "virginica"]
    assert 0.0 <= body["probability"] <= 1.0
    assert body["prediction_id"] == 123


def test_predict_endpoint_validates_missing_field():
    payload = {
        "sepal_length": 5.1,
        "sepal_width": 3.5,
        "petal_length": 1.4,
    }
    response = client.post("/predict", json=payload)
    body = response.json()

    assert response.status_code == 422
    assert body["error"] == "nieprawidłowe dane wejściowe"
    assert any(problem["pole"] == "petal_width" for problem in body["problemy"])


def test_predictions_endpoint_returns_db_items(monkeypatch):
    fake_items = [
        {"id": 1, "prediction": "setosa", "probability": 0.99},
        {"id": 2, "prediction": "virginica", "probability": 0.96},
    ]
    monkeypatch.setattr(main, "list_db_predictions", lambda limit=50, offset=0: fake_items)

    response = client.get("/predictions?limit=2&offset=0")
    assert response.status_code == 200
    assert response.json() == {"items": fake_items}
