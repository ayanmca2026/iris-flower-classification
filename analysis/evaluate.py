import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from typing import Dict, Any
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report
)

def evaluate_model_performance(y_true, y_pred, target_names) -> Dict[str, Any]:
    """
    Computes accuracy, precision, recall, f1-score, and classification report dict.
    """
    acc = accuracy_score(y_true, y_pred)
    prec = precision_score(y_true, y_pred, average="weighted", zero_division=0)
    rec = recall_score(y_true, y_pred, average="weighted", zero_division=0)
    f1 = f1_score(y_true, y_pred, average="weighted", zero_division=0)
    
    report_dict = classification_report(y_true, y_pred, target_names=target_names, output_dict=True, zero_division=0)

    return {
        "accuracy": round(float(acc), 4),
        "precision": round(float(prec), 4),
        "recall": round(float(rec), 4),
        "f1_score": round(float(f1), 4),
        "report": report_dict
    }

def save_confusion_matrix_plot(y_true, y_pred, target_names, save_path: Path, model_title: str):
    """
    Generates and saves a confusion matrix heatmap plot.
    """
    cm = confusion_matrix(y_true, y_pred)
    fig, ax = plt.subplots(figsize=(7, 5))
    sns.heatmap(
        cm,
        annot=True,
        fmt="d",
        cmap="Blues",
        xticklabels=target_names,
        yticklabels=target_names,
        ax=ax,
        cbar=False,
        annot_kws={"size": 14, "weight": "bold"}
    )
    ax.set_title(f"Confusion Matrix — {model_title}", fontsize=14, fontweight="bold", pad=15)
    ax.set_xlabel("Predicted Species", fontsize=12, labelpad=10)
    ax.set_ylabel("Actual Species", fontsize=12, labelpad=10)
    plt.tight_layout()
    plt.savefig(save_path, dpi=300)
    plt.close()
    print(f" Saved Confusion Matrix: {save_path.name}")
