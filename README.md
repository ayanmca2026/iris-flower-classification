# IrisAI — Iris Flower Species Classification

[![Live Frontend](https://img.shields.io/badge/Vercel-Live--Demo-000000?style=for-the-badge&logo=vercel)](https://iris-flower-classification-peach.vercel.app/)
[![Live Backend](https://img.shields.io/badge/Render-API--Status-46E3B7?style=for-the-badge&logo=render)](https://iris-flower-classification-zc3w.onrender.com/health)

An end-to-end Data Science, Machine Learning, FastAPI Backend, and React Frontend web application that classifies Iris flower species (`Iris-setosa`, `Iris-versicolor`, `Iris-virginica`) based on four physical measurements.

---

## 🌐 Production Live URLs

- **Frontend App (Vercel)**: [https://iris-flower-classification-peach.vercel.app](https://iris-flower-classification-peach.vercel.app)
- **Backend API (Render)**: [https://iris-flower-classification-zc3w.onrender.com](https://iris-flower-classification-zc3w.onrender.com)
- **API Health Check**: [https://iris-flower-classification-zc3w.onrender.com/health](https://iris-flower-classification-zc3w.onrender.com/health)
- **Swagger Interactive API Docs**: [https://iris-flower-classification-zc3w.onrender.com/docs](https://iris-flower-classification-zc3w.onrender.com/docs)

---

##  Project Architecture

```text
iris-flower-classification/
├── app/                      # Root FastAPI application package
├── dataset/
│   └── iris.csv              # Source uploaded Iris dataset (147 clean rows)
├── analysis/
│   ├── eda.py                # Data cleaning, normalization & plot generator
│   ├── train.py              # Stratified split, scaling, 7 ML models, 5-Fold CV, hyperparameter tuning
│   ├── evaluate.py           # Classification metrics & confusion matrix generator
│   └── plots/                # 8 High-resolution EDA and confusion matrix plots
├── notebooks/
│   └── iris_classification.ipynb # Complete interactive Jupyter Notebook
├── models/
│   ├── iris_model.pkl        # Best trained model artifact (Random Forest)
│   ├── scaler.pkl            # Pre-fitted StandardScaler artifact
│   ├── label_encoder.pkl     # Pre-fitted LabelEncoder artifact
│   └── model_metrics.json    # Metrics and benchmark comparison
├── backend/
│   └── app/                  # Backend subfolder package
├── frontend/
│   ├── src/
│   │   ├── components/       # Navbar, Hero, Form, Result, Metrics, Dataset, Workflow, Footer
│   │   ├── services/api.js   # Fetch API wrapper (VITE_API_URL)
│   │   ├── App.jsx
│   │   └── index.css         # Custom Glassmorphic Dark Design System
│   ├── package.json
│   ├── vite.config.js
│   └── README.md
├── tests/
│   ├── test_api.py           # Pytest unit tests for FastAPI endpoints
│   └── test_model.py         # Pytest unit tests for ML model inference
├── Procfile                  # Render/Railway deployment entry point
├── render.yaml               # Render Blueprint configuration
├── vercel.json               # Vercel SPA build & rewrite configuration
└── README.md
```

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

---

## 🛰️ API Documentation & Prediction Example

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
  "confidence": 1.0,
  "probabilities": {
    "Iris-setosa": 1.0,
    "Iris-versicolor": 0.0,
    "Iris-virginica": 0.0
  }
}
```

---

## 📄 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
