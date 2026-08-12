import sys
from pathlib import Path
import pytest
from fastapi.testclient import TestClient

# Ensure backend directory is in sys.path
BACKEND_DIR = Path(__file__).resolve().parent.parent / "backend"
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from app.main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "IrisAI API is running"}

def test_check_health():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"

def test_get_model_info():
    response = client.get("/model-info")
    assert response.status_code == 200
    data = response.json()
    assert "best_algorithm" in data
    assert "accuracy" in data
    assert "f1_score" in data

def test_get_dataset_info():
    response = client.get("/dataset-info")
    assert response.status_code == 200
    data = response.json()
    assert "total_samples" in data
    assert data["total_samples"] > 0
    assert "feature_names" in data

def test_predict_endpoint_valid():
    payload = {
        "sepal_length": 5.1,
        "sepal_width": 3.5,
        "petal_length": 1.4,
        "petal_width": 0.2
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "prediction" in data
    assert data["prediction"] in ["Iris-setosa", "Iris-versicolor", "Iris-virginica"]
    assert "confidence" in data
    assert "probabilities" in data

def test_predict_endpoint_invalid_negative():
    payload = {
        "sepal_length": -5.1,
        "sepal_width": 3.5,
        "petal_length": 1.4,
        "petal_width": 0.2
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 422  # Pydantic validation error

def test_predict_endpoint_invalid_type():
    payload = {
        "sepal_length": "invalid_string",
        "sepal_width": 3.5,
        "petal_length": 1.4,
        "petal_width": 0.2
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 422  # Pydantic validation error
