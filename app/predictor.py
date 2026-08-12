import json
import joblib
import numpy as np
from pathlib import Path
from typing import Dict, Any, Tuple
from app.config import MODEL_PATH, SCALER_PATH, LABEL_ENCODER_PATH, METRICS_PATH

class IrisPredictor:
    def __init__(self):
        self.model = None
        self.scaler = None
        self.label_encoder = None
        self.metrics = None
        self.is_loaded = False
        self.load_artifacts()

    def load_artifacts(self) -> bool:
        """Load trained ML model, scaler, label encoder, and metrics artifacts."""
        try:
            if MODEL_PATH.exists() and SCALER_PATH.exists() and LABEL_ENCODER_PATH.exists():
                self.model = joblib.load(MODEL_PATH)
                self.scaler = joblib.load(SCALER_PATH)
                self.label_encoder = joblib.load(LABEL_ENCODER_PATH)
                self.is_loaded = True

            if METRICS_PATH.exists():
                with open(METRICS_PATH, "r", encoding="utf-8") as f:
                    self.metrics = json.load(f)
            return self.is_loaded
        except Exception as e:
            print(f"Error loading artifacts: {e}")
            self.is_loaded = False
            return False

    def predict(
        self,
        sepal_length: float,
        sepal_width: float,
        petal_length: float,
        petal_width: float
    ) -> Dict[str, Any]:
        """Perform scaling and inference for input flower measurements."""
        if not self.is_loaded:
            loaded = self.load_artifacts()
            if not loaded:
                raise RuntimeError("ML model artifacts are not loaded or missing. Please run model training first.")

        # Prepare feature array in correct column order
        import pandas as pd
        raw_features = pd.DataFrame(
            [[sepal_length, sepal_width, petal_length, petal_width]],
            columns=["sepal_length", "sepal_width", "petal_length", "petal_width"]
        )
        scaled_features = self.scaler.transform(raw_features)

        # Predict class index
        pred_idx = self.model.predict(scaled_features)[0]
        
        # Determine class label string
        if hasattr(self.label_encoder, "inverse_transform"):
            predicted_species = self.label_encoder.inverse_transform([pred_idx])[0]
            classes = list(self.label_encoder.classes_)
        else:
            classes = ["Iris-setosa", "Iris-versicolor", "Iris-virginica"]
            predicted_species = classes[pred_idx]

        # Calculate prediction probabilities
        if hasattr(self.model, "predict_proba"):
            probs = self.model.predict_proba(scaled_features)[0]
        else:
            # Fallback for models without predict_proba
            probs = np.zeros(len(classes))
            probs[pred_idx] = 1.0

        confidence = float(np.max(probs))

        # Map species to probabilities rounded to 4 decimals
        probabilities_dict = {}
        for cls_name, prob_val in zip(classes, probs):
            probabilities_dict[str(cls_name)] = round(float(prob_val), 4)

        return {
            "prediction": str(predicted_species),
            "confidence": round(confidence, 4),
            "probabilities": probabilities_dict
        }

    def get_model_info(self) -> Dict[str, Any]:
        """Return model metadata and metrics."""
        if not self.metrics and METRICS_PATH.exists():
            with open(METRICS_PATH, "r", encoding="utf-8") as f:
                self.metrics = json.load(f)

        if self.metrics:
            return self.metrics

        return {
            "best_model": type(self.model).__name__ if self.model else "Unknown",
            "accuracy": 0.0,
            "precision": 0.0,
            "recall": 0.0,
            "f1_score": 0.0,
            "cv_mean_accuracy": 0.0,
            "cv_std": 0.0,
            "features": ["sepal_length", "sepal_width", "petal_length", "petal_width"],
            "target_classes": ["Iris-setosa", "Iris-versicolor", "Iris-virginica"]
        }

predictor = IrisPredictor()
