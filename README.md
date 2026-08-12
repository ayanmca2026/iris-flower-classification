# IrisAI — Iris Flower Species Classification

[![Python Version](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-009688.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18.3-61DAFB.svg)](https://reactjs.org/)
[![Vite](https://img.shields.io/badge/Vite-5.4-646CFF.svg)](https://vitejs.dev/)
[![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-1.4%2B-F7931E.svg)](https://scikit-learn.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

An end-to-end Data Science, Machine Learning, FastAPI Backend, and React Frontend web application that classifies Iris flower species (`Iris-setosa`, `Iris-versicolor`, `Iris-virginica`) based on four physical measurements.

---

##  Project Architecture

```text
iris-flower-classification/
├── dataset/
│   └── iris.csv              # Primary uploaded Iris dataset (150 rows)
├── analysis/
│   ├── eda.py                # Data cleaning, normalization, duplicate removal & plot generator
│   ├── train.py              # Stratified split, scaling, 7 ML models, 5-Fold CV, hyperparameter tuning
│   ├── evaluate.py           # Classification metrics & confusion matrix generator
│   └── plots/                # 7 High-resolution EDA and confusion matrix plots
├── notebooks/
│   └── iris_classification.ipynb # Complete interactive Jupyter Notebook
├── models/
│   ├── iris_model.pkl        # Best trained model artifact (Random Forest)
│   ├── scaler.pkl            # Pre-fitted StandardScaler artifact
│   ├── label_encoder.pkl     # Pre-fitted LabelEncoder artifact
│   └── model_metrics.json    # Metrics and benchmark comparison
├── backend/
│   ├── app/
│   │   ├── main.py           # FastAPI application endpoints
│   │   ├── predictor.py      # Inference engine using loaded joblib artifacts
│   │   ├── schemas.py        # Pydantic v2 schemas and validation
│   │   └── config.py         # CORS and path configuration
│   ├── requirements.txt
│   └── README.md
├── frontend/
│   ├── src/
│   │   ├── components/       # Navbar, Hero, Form, Result, Metrics, Dataset, Workflow, Footer
│   │   ├── services/api.js   # Fetch API wrapper (VITE_API_URL)
│   │   ├── App.jsx
│   │   └── index.css         # Custom Glassmorphic Dark Design System
│   ├── package.json
│   ├── vite.config.js
│   └── README.md
└── tests/
    ├── test_api.py           # Pytest unit tests for FastAPI endpoints
    └── test_model.py         # Pytest unit tests for ML model inference
```

---

##  Exploratory Data Analysis & Visualizations

The dataset contains **150 samples** across **4 numerical features** and **3 target species classes**:

1. **Sepal Length (cm)**: Range 4.3 – 7.9 cm (Mean: 5.86 cm)
2. **Sepal Width (cm)**: Range 2.0 – 4.4 cm (Mean: 3.06 cm)
3. **Petal Length (cm)**: Range 1.0 – 6.9 cm (Mean: 3.78 cm)
4. **Petal Width (cm)**: Range 0.1 – 2.5 cm (Mean: 1.21 cm)

### Cleaned Dataset Distribution
- `Iris-versicolor`: 50 samples
- `Iris-virginica`: 49 samples
- `Iris-setosa`: 48 samples
- *3 duplicate rows automatically removed during cleaning (Final clean shape: 147 × 5).*

### Generated Visualizations (`analysis/plots/`)
- `class_distribution.png`: Species class balance bar chart
- `feature_distribution.png`: Feature KDE distributions by species
- `feature_boxplots.png`: Outliers & variance across species
- `pairplot.png`: Multi-feature pairwise scatter relationships
- `correlation_heatmap.png`: Pearson feature correlation matrix
- `sepal_scatter.png`: Sepal Length vs Sepal Width
- `petal_scatter.png`: Petal Length vs Petal Width
- `confusion_matrix.png`: Test set confusion matrix for selected model

---

## 🤖 Machine Learning Model Benchmarks

7 candidate algorithms were trained on **80% stratified training data** (`random_state=42`) using `StandardScaler` fitted exclusively on training features. Hyperparameters were tuned using 5-Fold `GridSearchCV`.

| Model Algorithm | Test Accuracy | Precision | Recall | F1 Score | 5-Fold CV Mean | Status |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Random Forest** | **96.67%** | **96.97%** | **96.67%** | **96.66%** | **95.69%** | **⭐ Best Model Selected** |
| Support Vector Machine (SVM) | 93.33% | 93.33% | 93.33% | 93.33% | 97.43% | Candidate |
| Gaussian Naive Bayes | 93.33% | 93.33% | 93.33% | 93.33% | 96.56% | Candidate |
| K-Nearest Neighbors (KNN) | 96.67% | 96.97% | 96.67% | 96.66% | 94.89% | Candidate |
| Gradient Boosting | 96.67% | 96.97% | 96.67% | 96.66% | 94.02% | Candidate |
| Logistic Regression | 93.33% | 93.33% | 93.33% | 93.33% | 95.72% | Candidate |
| Decision Tree | 93.33% | 93.33% | 93.33% | 93.33% | 94.86% | Candidate |

### Selected Best Model Specifications
- **Algorithm**: Random Forest Classifier
- **Tuned Hyperparameters**: `n_estimators=100`, `max_depth=3`, `min_samples_split=2`
- **Test Set Accuracy**: 96.67%
- **Test Set F1 Score**: 96.66%
- **5-Fold Cross Validation Accuracy**: 95.69% (±4.76%)

---

## ⚡ Quick Start Guide

### 1. Prerequisites
- Python 3.11+
- Node.js 18+ and npm

### 2. Clone repository & install Python Virtual Environment
```bash
cd iris-flower-classification
python -m venv venv
# On Windows PowerShell:
.\venv\Scripts\Activate.ps1
# On Linux/macOS:
source venv/bin/activate

pip install -r backend/requirements.txt
```

### 3. Run EDA & Model Training
```bash
python analysis/eda.py
python analysis/train.py
```

### 4. Launch FastAPI Backend
```bash
cd backend
uvicorn app.main:app --reload --port 8000
```
Backend API will be live at `http://localhost:8000`. Swagger API docs available at `http://localhost:8000/docs`.

### 5. Launch React Frontend
In a separate terminal window:
```bash
cd frontend
npm install
npm run dev
```
Open `http://localhost:5173` in your browser.

---

## 🧪 Automated Testing

Run the complete Pytest suite for model inference and API endpoints:

```bash
pytest tests/
```

Test Results:
- `tests/test_api.py` (7 tests passed)
- `tests/test_model.py` (4 tests passed)
- **Total: 11 / 11 Passed**

---

## 🛰️ API Documentation

### `POST /predict`
Accepts 4 numerical flower measurements and returns species classification, confidence, and class probability distribution.

#### Request Body
```json
{
  "sepal_length": 5.1,
  "sepal_width": 3.5,
  "petal_length": 1.4,
  "petal_width": 0.2
}
```

#### Response Body
```json
{
  "prediction": "Iris-setosa",
  "confidence": 0.99,
  "probabilities": {
    "Iris-setosa": 0.99,
    "Iris-versicolor": 0.01,
    "Iris-virginica": 0.00
  }
}
```

### Other Endpoints
- `GET /` — API Status Message
- `GET /health` — Operational health check and model loading status
- `GET /model-info` — Returns selected model specs, evaluation metrics, and comparison matrix
- `GET /dataset-info` — Returns dataset sample counts, feature statistics, and class counts

---

## 🚀 Deployment

### Frontend (Vercel)
1. Push `frontend/` to GitHub.
2. Connect repository to Vercel.
3. Set Environment Variable: `VITE_API_URL=https://your-fastapi-backend.onrender.com`
4. Build command: `npm run build`, Output directory: `dist`.

### Backend (Render / Railway)
1. Deploy `backend/` as a Web Service.
2. Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
3. Environment Variable: `FRONTEND_URL=https://your-app.vercel.app`

---

## 📄 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
