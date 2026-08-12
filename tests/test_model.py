import sys
from pathlib import Path
import pytest

# Ensure backend app package is importable
BACKEND_DIR = Path(__file__).resolve().parent.parent / "backend"
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from app.config import MODEL_PATH, SCALER_PATH, LABEL_ENCODER_PATH, METRICS_PATH
from app.predictor import IrisPredictor

def test_artifact_files_exist():
    assert MODEL_PATH.exists(), f"Model file missing at {MODEL_PATH}"
    assert SCALER_PATH.exists(), f"Scaler file missing at {SCALER_PATH}"
    assert LABEL_ENCODER_PATH.exists(), f"Label encoder missing at {LABEL_ENCODER_PATH}"
    assert METRICS_PATH.exists(), f"Metrics file missing at {METRICS_PATH}"

def test_predictor_loading():
    predictor = IrisPredictor()
    assert predictor.is_loaded is True
    assert predictor.model is not None
    assert predictor.scaler is not None
    assert predictor.label_encoder is not None

def test_predictor_inference():
    predictor = IrisPredictor()
    
    # Test Setosa sample
    res_setosa = predictor.predict(5.1, 3.5, 1.4, 0.2)
    assert "prediction" in res_setosa
    assert "confidence" in res_setosa
    assert "probabilities" in res_setosa
    assert res_setosa["prediction"] in ["Iris-setosa", "Iris-versicolor", "Iris-virginica"]
    assert 0.0 <= res_setosa["confidence"] <= 1.0

    # Probability sum check
    prob_sum = sum(res_setosa["probabilities"].values())
    assert abs(prob_sum - 1.0) < 0.05

def test_model_info_retrieval():
    predictor = IrisPredictor()
    info = predictor.get_model_info()
    assert "best_algorithm" in info
    assert "accuracy" in info
    assert "f1_score" in info
    assert "features" in info
