from pydantic import BaseModel, Field, field_validator
from typing import Dict, List, Any, Optional
import math

class PredictRequest(BaseModel):
    sepal_length: float = Field(..., gt=0.0, lt=15.0, description="Sepal Length in cm (0 < val < 15)")
    sepal_width: float = Field(..., gt=0.0, lt=15.0, description="Sepal Width in cm (0 < val < 15)")
    petal_length: float = Field(..., gt=0.0, lt=15.0, description="Petal Length in cm (0 < val < 15)")
    petal_width: float = Field(..., gt=0.0, lt=15.0, description="Petal Width in cm (0 < val < 15)")

    @field_validator("sepal_length", "sepal_width", "petal_length", "petal_width")

    def check_nan_inf(cls, v: float) -> float:
        if math.isnan(v) or math.isinf(v):
            raise ValueError("Measurement value cannot be NaN or Infinite.")
        return round(float(v), 2)

    model_config = {
        "json_schema_extra": {
            "example": {
                "sepal_length": 5.1,
                "sepal_width": 3.5,
                "petal_length": 1.4,
                "petal_width": 0.2
            }
        }
    }

class PredictResponse(BaseModel):
    prediction: str
    confidence: float
    probabilities: Dict[str, float]

class ModelInfoResponse(BaseModel):
    model_name: str
    best_algorithm: str
    accuracy: float
    precision: float
    recall: float
    f1_score: float
    cv_mean_accuracy: float
    cv_std: float
    features: List[str]
    target_classes: List[str]
    model_comparison: Optional[List[Dict[str, Any]]] = None

class HealthResponse(BaseModel):
    status: str
    message: str
