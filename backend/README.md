# IrisAI — FastAPI Backend

FastAPI application for Iris Flower species prediction.

## Features
- **Predict Endpoint (`POST /predict`)**: Evaluates sepal and petal dimensions, applying `StandardScaler` and predicting species with exact confidence scores.
- **Model Info (`GET /model-info`)**: Exposes dynamic model metrics, 5-fold cross-validation performance, and model comparison data.
- **Dataset Info (`GET /dataset-info`)**: Returns dataset summary statistics and target class distribution.
- **Health Check (`GET /health`)**: Verifies system operational status and model artifact loading.

## Running Locally

```bash
cd backend
python -m pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

## API Endpoints

- `GET http://localhost:8000/`
- `GET http://localhost:8000/health`
- `GET http://localhost:8000/model-info`
- `GET http://localhost:8000/dataset-info`
- `POST http://localhost:8000/predict`
