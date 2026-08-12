import os
import json
import joblib
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, Any

from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB

from eda import load_and_clean_data
from evaluate import evaluate_model_performance, save_confusion_matrix_plot

# Directory Paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATASET_PATH = BASE_DIR / "dataset" / "iris.csv"
MODELS_DIR = BASE_DIR / "models"
PLOTS_DIR = BASE_DIR / "analysis" / "plots"
MODELS_DIR.mkdir(parents=True, exist_ok=True)
PLOTS_DIR.mkdir(parents=True, exist_ok=True)

def train_and_evaluate_pipeline():
    print("==================================================")
    print("STARTING IRIS MODEL TRAINING PIPELINE")
    print("==================================================")

    # 1. Load Clean Data
    df = load_and_clean_data(DATASET_PATH)

    # Features and Target
    feature_cols = ["sepal_length", "sepal_width", "petal_length", "petal_width"]
    X = df[feature_cols]
    y_raw = df["species"]

    # Encode Target Labels
    label_encoder = LabelEncoder()
    y = label_encoder.fit_transform(y_raw)
    target_classes = list(label_encoder.classes_)
    print(f"Target classes encoded: {dict(zip(range(len(target_classes)), target_classes))}")

    # 2. Train/Test Split (80% Train, 20% Test, Stratified)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y
    )
    print(f"Training set size: {X_train.shape[0]} | Testing set size: {X_test.shape[0]}")

    # 3. Feature Scaling (Fit on Train ONLY)
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # 4. Define Model Candidates
    candidate_models = {
        "Logistic Regression": LogisticRegression(max_iter=1000, random_state=42),
        "K-Nearest Neighbors": KNeighborsClassifier(),
        "Decision Tree": DecisionTreeClassifier(random_state=42),
        "Random Forest": RandomForestClassifier(n_estimators=100, random_state=42),
        "Support Vector Machine": SVC(probability=True, random_state=42),
        "Gaussian Naive Bayes": GaussianNB(),
        "Gradient Boosting": GradientBoostingClassifier(random_state=42)
    }

    # 5. Hyperparameter Tuning Grids
    param_grids = {
        "Random Forest": {
            "n_estimators": [50, 100, 150],
            "max_depth": [None, 3, 5, 7],
            "min_samples_split": [2, 5]
        },
        "K-Nearest Neighbors": {
            "n_neighbors": [3, 5, 7, 9],
            "weights": ["uniform", "distance"],
            "metric": ["euclidean", "manhattan"]
        },
        "Support Vector Machine": {
            "C": [0.1, 1.0, 10.0],
            "kernel": ["linear", "rbf"],
            "gamma": ["scale", "auto"]
        }
    }

    model_results = []
    trained_estimators = {}

    print("\n==================================================")
    print("EVALUATING MULTIPLE ML MODELS & CROSS-VALIDATION")
    print("==================================================")

    for model_name, model_obj in candidate_models.items():
        print(f"\n--- Training: {model_name} ---")
        
        # Check if hyperparameter tuning applies
        if model_name in param_grids:
            print(f" Running GridSearchCV hyperparameter tuning for {model_name}...")
            grid_search = GridSearchCV(
                estimator=model_obj,
                param_grid=param_grids[model_name],
                cv=5,
                scoring="f1_weighted",
                n_jobs=-1
            )
            grid_search.fit(X_train_scaled, y_train)
            best_model = grid_search.best_estimator_
            print(f" Best Params for {model_name}: {grid_search.best_params_}")
        else:
            best_model = model_obj
            best_model.fit(X_train_scaled, y_train)

        # 5-Fold Cross-Validation on Training Data
        cv_scores = cross_val_score(best_model, X_train_scaled, y_train, cv=5, scoring="accuracy")
        cv_mean = float(np.mean(cv_scores))
        cv_std = float(np.std(cv_scores))

        # Evaluate on Test Set
        y_pred = best_model.predict(X_test_scaled)
        metrics = evaluate_model_performance(y_test, y_pred, target_classes)
        metrics["cv_mean_accuracy"] = round(cv_mean, 4)
        metrics["cv_std"] = round(cv_std, 4)
        metrics["model_name"] = model_name

        print(f" Test Accuracy: {metrics['accuracy']:.4f} | F1 Score: {metrics['f1_score']:.4f} | 5-Fold CV Mean: {cv_mean:.4f}")

        model_results.append(metrics)
        trained_estimators[model_name] = best_model

    # 6. Sort and Select Best Model
    # Sort primarily by Test F1 Score, then CV Mean Accuracy
    sorted_results = sorted(
        model_results,
        key=lambda x: (x["f1_score"], x["accuracy"], x["cv_mean_accuracy"]),
        reverse=True
    )

    best_result = sorted_results[0]
    best_model_name = best_result["model_name"]
    best_estimator = trained_estimators[best_model_name]

    print("\n==================================================")
    print(f"BEST MODEL SELECTED: {best_model_name}")
    print(f"Test Accuracy: {best_result['accuracy'] * 100:.2f}%")
    print(f"Test Precision: {best_result['precision'] * 100:.2f}%")
    print(f"Test Recall: {best_result['recall'] * 100:.2f}%")
    print(f"Test F1 Score: {best_result['f1_score'] * 100:.2f}%")
    print(f"5-Fold CV Accuracy: {best_result['cv_mean_accuracy'] * 100:.2f}% (±{best_result['cv_std'] * 100:.2f}%)")
    print("==================================================")

    # 7. Save Confusion Matrix plot for Best Model
    y_pred_best = best_estimator.predict(X_test_scaled)
    save_confusion_matrix_plot(y_test, y_pred_best, target_classes, PLOTS_DIR / "confusion_matrix.png", best_model_name)

    # 8. Save Model Artifacts
    joblib.dump(best_estimator, MODELS_DIR / "iris_model.pkl")
    joblib.dump(scaler, MODELS_DIR / "scaler.pkl")
    joblib.dump(label_encoder, MODELS_DIR / "label_encoder.pkl")
    print("\n Saved Model Artifacts:")
    print("  - models/iris_model.pkl")
    print("  - models/scaler.pkl")
    print("  - models/label_encoder.pkl")

    # 9. Save Metrics Summary JSON
    metrics_summary = {
        "best_algorithm": best_model_name,
        "accuracy": best_result["accuracy"],
        "precision": best_result["precision"],
        "recall": best_result["recall"],
        "f1_score": best_result["f1_score"],
        "cv_mean_accuracy": best_result["cv_mean_accuracy"],
        "cv_std": best_result["cv_std"],
        "features": feature_cols,
        "target_classes": target_classes,
        "model_comparison": [
            {
                "model": res["model_name"],
                "accuracy": res["accuracy"],
                "precision": res["precision"],
                "recall": res["recall"],
                "f1_score": res["f1_score"],
                "cv_mean": res["cv_mean_accuracy"]
            }
            for res in sorted_results
        ]
    }

    with open(MODELS_DIR / "model_metrics.json", "w", encoding="utf-8") as f:
        json.dump(metrics_summary, f, indent=2)
    print(" Saved Metrics JSON: models/model_metrics.json")

    return best_model_name, best_result

if __name__ == "__main__":
    train_and_evaluate_pipeline()
