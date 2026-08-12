from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import json
from typing import Dict, Any

from app.schemas import (
    PredictRequest,
    PredictResponse,
    ModelInfoResponse,
    HealthResponse
)
from app.config import ALLOWED_ORIGINS, DATASET_PATH, METRICS_PATH
from app.predictor import predictor

app = FastAPI(
    title="IrisAI — Iris Flower Classification API",
    description="Production-grade Machine Learning API for Iris Flower Species Classification.",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", summary="Root Endpoint")
def read_root():
    return {"message": "IrisAI API is running"}

@app.get("/health", response_model=HealthResponse, summary="Health Check")
def check_health():
    model_status = "loaded" if predictor.is_loaded else "not_loaded"
    return {
        "status": "healthy",
        "message": f"IrisAI API is operational. ML Model status: {model_status}."
    }

@app.get("/model-info", summary="Model Specifications and Performance")
def get_model_info():
    info = predictor.get_model_info()
    return info

@app.get("/dataset-info", summary="Dataset Summary Statistics")
def get_dataset_info() -> Dict[str, Any]:
    if not DATASET_PATH.exists():
        raise HTTPException(
            status_code=status.HTTP_444_NOT_FOUND if hasattr(status, "HTTP_444_NOT_FOUND") else 404,
            detail="Dataset file iris.csv not found."
        )
    
    df = pd.read_csv(DATASET_PATH)
    
    # Normalize column names to check target column
    cols = [str(c).strip().lower() for c in df.columns]
    target_col = None
    for c in df.columns:
        if c.strip().lower() in ["species", "target", "class"]:
            target_col = c
            break
            
    species_counts = {}
    if target_col and target_col in df.columns:
        species_counts = df[target_col].value_counts().to_dict()

    feature_cols = [c for c in df.columns if c != target_col and c.lower() not in ["id", "unnamed: 0", "index"]]
    
    numeric_df = df[feature_cols].select_dtypes(include=["float64", "int64", "float32", "int32"])
    stats = numeric_df.describe().to_dict()

    return {
        "total_samples": len(df),
        "total_features": len(feature_cols),
        "feature_names": feature_cols,
        "class_distribution": species_counts,
        "statistics": stats
    }

@app.post("/predict", response_model=PredictResponse, summary="Predict Species")
def predict(request: PredictRequest):
    try:
        result = predictor.predict(
            sepal_length=request.sepal_length,
            sepal_width=request.sepal_width,
            petal_length=request.petal_length,
            petal_width=request.petal_width
        )
        return result
    except RuntimeError as re:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(re))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred during prediction processing: {str(e)}"
        )
