import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATASET_PATH = BASE_DIR / "dataset" / "iris.csv"
PLOTS_DIR = BASE_DIR / "analysis" / "plots"
PLOTS_DIR.mkdir(parents=True, exist_ok=True)

# Set global plotting style
plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")
sns.set_theme(style="whitegrid", palette="muted")
plt.rcParams["font.sans-serif"] = "Segoe UI"
plt.rcParams["figure.dpi"] = 300

def load_and_clean_data(csv_path: Path) -> pd.DataFrame:
    """
    Loads raw CSV dataset, performs robust column normalization, removes non-feature ID columns,
    imputes missing values if any exist, and drops duplicate rows.
    """
    print(f"==================================================")
    print(f"1. LOADING DATASET FROM: {csv_path}")
    print(f"==================================================")
    if not csv_path.exists():
        raise FileNotFoundError(f"Dataset CSV not found at {csv_path}")

    df = pd.read_csv(csv_path)
    print(f"Raw dataset shape: {df.shape}")
    print(f"Raw columns: {list(df.columns)}")

    # Column Mapping Dictionary
    column_mapping = {}
    for col in df.columns:
        clean_col = str(col).strip().lower().replace(" ", "_")
        if "sepallength" in clean_col or "sepal_length" in clean_col:
            column_mapping[col] = "sepal_length"
        elif "sepalwidth" in clean_col or "sepal_width" in clean_col:
            column_mapping[col] = "sepal_width"
        elif "petallength" in clean_col or "petal_length" in clean_col:
            column_mapping[col] = "petal_length"
        elif "petalwidth" in clean_col or "petal_width" in clean_col:
            column_mapping[col] = "petal_width"
        elif "species" in clean_col or "target" in clean_col or "class" in clean_col:
            column_mapping[col] = "species"
        elif clean_col in ["id", "unnamed:_0", "index"]:
            column_mapping[col] = "DROP_ID"
        else:
            column_mapping[col] = clean_col

    # Rename & Drop redundant columns
    df = df.rename(columns=column_mapping)
    if "DROP_ID" in df.columns:
        df = df.drop(columns=["DROP_ID"])

    # Drop any remaining unrecognized extra columns if not expected
    expected_cols = ["sepal_length", "sepal_width", "petal_length", "petal_width", "species"]
    present_expected = [c for c in expected_cols if c in df.columns]
    df = df[present_expected]

    print(f"\nNormalized Columns: {list(df.columns)}")

    # Check Missing Values
    print("\n--- Missing Values Check ---")
    missing = df.isnull().sum()
    print(missing)
    if missing.sum() > 0:
        print("Missing values detected. Imputing numerical features with column median...")
        for num_col in ["sepal_length", "sepal_width", "petal_length", "petal_width"]:
            if num_col in df.columns and df[num_col].isnull().sum() > 0:
                df[num_col] = df[num_col].fillna(df[num_col].median())

    # Check Duplicate Rows
    print("\n--- Duplicate Records Check ---")
    num_duplicates = df.duplicated().sum()
    print(f"Duplicate rows found: {num_duplicates}")
    if num_duplicates > 0:
        print("Removing duplicate records...")
        df = df.drop_duplicates().reset_index(drop=True)
        print(f"Shape after removing duplicates: {df.shape}")

    # Convert numeric columns explicitly
    for col in ["sepal_length", "sepal_width", "petal_length", "petal_width"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # Clean target species labels
    if "species" in df.columns:
        df["species"] = df["species"].astype(str).str.strip()

    print(f"\nFinal Cleaned Dataset Shape: {df.shape}")
    return df

def perform_eda(df: pd.DataFrame):
    """
    Displays dataset summaries, statistics, and class distributions.
    """
    print("\n==================================================")
    print("2. EXPLORATORY DATA ANALYSIS (EDA)")
    print("==================================================")
    print("\n--- First 5 Rows ---")
    print(df.head())

    print("\n--- Last 5 Rows ---")
    print(df.tail())

    print("\n--- Dataset Info & Data Types ---")
    print(df.info())

    print("\n--- Statistical Summary ---")
    print(df.describe().T)

    print("\n--- Target Class Distribution ---")
    species_counts = df["species"].value_counts()
    print(species_counts)
    print(f"Unique classes: {df['species'].nunique()}")

def generate_visualizations(df: pd.DataFrame):
    """
    Generates and saves 7 publication-quality EDA plots inside analysis/plots/
    """
    print("\n==================================================")
    print("3. GENERATING AND SAVING EDA PLOTS")
    print("==================================================")
    
    species_colors = {"Iris-setosa": "#3B82F6", "Iris-versicolor": "#10B981", "Iris-virginica": "#8B5CF6"}
    palette = [species_colors.get(s, "#64748B") for s in df["species"].unique()]

    # 1. Class Distribution
    fig, ax = plt.subplots(figsize=(8, 5))
    counts = df["species"].value_counts()
    bars = ax.bar(counts.index, counts.values, color=[species_colors.get(s, "#3B82F6") for s in counts.index], width=0.5, edgecolor="black", alpha=0.85)
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f"{height}", xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3), textcoords="offset points", ha="center", va="bottom", fontweight="bold", fontsize=11)
    ax.set_title("Iris Species Class Distribution", fontsize=14, fontweight="bold", pad=15)
    ax.set_xlabel("Species", fontsize=12, labelpad=10)
    ax.set_ylabel("Count", fontsize=12, labelpad=10)
    plt.tight_layout()
    plt.savefig(PLOTS_DIR / "class_distribution.png", dpi=300)
    plt.close()
    print(" Saved: class_distribution.png")

    # 2. Feature Histograms
    num_cols = ["sepal_length", "sepal_width", "petal_length", "petal_width"]
    fig, axes = plt.subplots(2, 2, figsize=(12, 9))
    axes = axes.flatten()
    for idx, col in enumerate(num_cols):
        sns.histplot(df, x=col, hue="species", kde=True, ax=axes[idx], palette=species_colors, element="step")
        axes[idx].set_title(f"Distribution of {col.replace('_', ' ').title()} (cm)", fontweight="bold", fontsize=12)
        axes[idx].set_xlabel(f"{col.replace('_', ' ').title()} (cm)")
        axes[idx].set_ylabel("Frequency")
    plt.suptitle("Iris Feature Distributions by Species", fontsize=15, fontweight="bold", y=1.02)
    plt.tight_layout()
    plt.savefig(PLOTS_DIR / "feature_distribution.png", dpi=300)
    plt.close()
    print(" Saved: feature_distribution.png")

    # 3. Feature Boxplots
    fig, axes = plt.subplots(2, 2, figsize=(12, 9))
    axes = axes.flatten()
    for idx, col in enumerate(num_cols):
        sns.boxplot(data=df, x="species", y=col, hue="species", ax=axes[idx], palette=species_colors, linewidth=1.5, legend=False)
        axes[idx].set_title(f"{col.replace('_', ' ').title()} Boxplot", fontweight="bold", fontsize=12)
        axes[idx].set_xlabel("Species")
        axes[idx].set_ylabel(f"{col.replace('_', ' ').title()} (cm)")
    plt.suptitle("Feature Variance & Outliers across Species", fontsize=15, fontweight="bold", y=1.02)
    plt.tight_layout()
    plt.savefig(PLOTS_DIR / "feature_boxplots.png", dpi=300)
    plt.close()
    print(" Saved: feature_boxplots.png")

    # 4. Pairplot
    pair_fig = sns.pairplot(df, hue="species", palette=species_colors, corner=False, diag_kind="kde", markers=["o", "s", "D"])
    pair_fig.fig.suptitle("Iris Multi-Feature Pairwise Relationships", y=1.02, fontsize=16, fontweight="bold")
    pair_fig.savefig(PLOTS_DIR / "pairplot.png", dpi=300)
    plt.close()
    print(" Saved: pairplot.png")

    # 5. Correlation Heatmap
    fig, ax = plt.subplots(figsize=(8, 6))
    corr = df[num_cols].corr()
    sns.heatmap(corr, annot=True, cmap="Blues", fmt=".2f", linewidths=1.5, ax=ax, cbar_kws={"shrink": 0.8}, annot_kws={"weight": "bold", "size": 12})
    ax.set_title("Feature Pearson Correlation Heatmap", fontsize=14, fontweight="bold", pad=15)
    plt.tight_layout()
    plt.savefig(PLOTS_DIR / "correlation_heatmap.png", dpi=300)
    plt.close()
    print(" Saved: correlation_heatmap.png")

    # 6. Sepal Scatter Plot
    fig, ax = plt.subplots(figsize=(9, 6))
    sns.scatterplot(data=df, x="sepal_length", y="sepal_width", hue="species", style="species", palette=species_colors, s=90, alpha=0.9, ax=ax)
    ax.set_title("Sepal Length vs Sepal Width by Species", fontsize=14, fontweight="bold", pad=15)
    ax.set_xlabel("Sepal Length (cm)", fontsize=12)
    ax.set_ylabel("Sepal Width (cm)", fontsize=12)
    plt.tight_layout()
    plt.savefig(PLOTS_DIR / "sepal_scatter.png", dpi=300)
    plt.close()
    print(" Saved: sepal_scatter.png")

    # 7. Petal Scatter Plot
    fig, ax = plt.subplots(figsize=(9, 6))
    sns.scatterplot(data=df, x="petal_length", y="petal_width", hue="species", style="species", palette=species_colors, s=90, alpha=0.9, ax=ax)
    ax.set_title("Petal Length vs Petal Width by Species", fontsize=14, fontweight="bold", pad=15)
    ax.set_xlabel("Petal Length (cm)", fontsize=12)
    ax.set_ylabel("Petal Width (cm)", fontsize=12)
    plt.tight_layout()
    plt.savefig(PLOTS_DIR / "petal_scatter.png", dpi=300)
    plt.close()
    print(" Saved: petal_scatter.png")

if __name__ == "__main__":
    df = load_and_clean_data(DATASET_PATH)
    perform_eda(df)
    generate_visualizations(df)
    print("\nEDA script completed successfully!")
