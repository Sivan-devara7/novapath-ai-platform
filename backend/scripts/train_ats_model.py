"""
Real ML Training Pipeline for Resume Role-Fit Modeling.
Trains and compares Logistic Regression, Linear SVM, and Gradient Boosting
on the genuine Kaggle Resume Dataset (962 resumes, 25 categories).
Reports accuracy, macro F1, per-class metrics, confusion matrix,
and exports the top-performing model with joblib + metrics.json.
"""

import os
import sys
import re
import json
import io
import joblib
import httpx
import numpy as np
import pandas as pd
from typing import Dict, Any, Tuple

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.calibration import CalibratedClassifierCV
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import accuracy_score, f1_score, classification_report, confusion_matrix
from sklearn.pipeline import Pipeline

RANDOM_SEED = 42
DATASET_URL = "https://raw.githubusercontent.com/2003vivek/TalentTorch/main/UpdatedResumeDataSet.csv"

def clean_and_sanitize_text(text: str) -> str:
    """Removes PII (emails, URLs, phone numbers), HTML, and non-alphanumeric noise."""
    if not isinstance(text, str):
        return ""
    # Strip URLs
    text = re.sub(r"https?://\S+|www\.\S+", " ", text)
    # Strip Email addresses
    text = re.sub(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", " ", text)
    # Strip Phone numbers
    text = re.sub(r"\+?\d[\d -]{8,}\d", " ", text)
    # Strip special characters and excessive whitespace
    text = re.sub(r"[^\w\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip().lower()
    return text

def load_or_fetch_dataset() -> pd.DataFrame:
    """Fetches Kaggle resume dataset from local path or verified public repository."""
    backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    local_data_dir = os.path.join(backend_dir, "data")
    os.makedirs(local_data_dir, exist_ok=True)
    local_csv = os.path.join(local_data_dir, "UpdatedResumeDataSet.csv")

    if os.path.isfile(local_csv):
        print(f"Loading local dataset from: {local_csv}")
        df = pd.read_csv(local_csv)
    else:
        print(f"Fetching verified Kaggle dataset from: {DATASET_URL}")
        resp = httpx.get(DATASET_URL, timeout=30.0)
        if resp.status_code != 200:
            raise RuntimeError(f"Failed to fetch dataset: HTTP {resp.status_code}")
        with open(local_csv, "w", encoding="utf-8") as f:
            f.write(resp.text)
        df = pd.read_csv(io.StringIO(resp.text))

    print(f"Dataset successfully loaded. Total rows: {len(df)}, Columns: {df.columns.tolist()}")
    return df

def train_and_evaluate_models():
    print("=" * 70)
    print("NOVAPATH AI — REAL ML ATS ROLE-FIT MODEL TRAINING PIPELINE")
    print("=" * 70)

    # 1. Ingest Data
    df = load_or_fetch_dataset()
    assert "Category" in df.columns and "Resume" in df.columns, "Expected 'Category' and 'Resume' columns"

    # 2. Clean & Sanitize Text
    print("Sanitizing text and stripping PII...")
    df["Cleaned_Resume"] = df["Resume"].apply(clean_and_sanitize_text)

    # Filter any empty rows
    df = df[df["Cleaned_Resume"].str.len() > 20].copy()
    print(f"Usable resumes after sanitization: {len(df)} across {df['Category'].nunique()} categories.")

    X = np.array(df["Cleaned_Resume"].tolist(), dtype=str)
    y = np.array(df["Category"].tolist(), dtype=str)

    # 3. Stratified Train / Test Split (80% Train, 20% Held-Out Test)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.20,
        random_state=RANDOM_SEED,
        stratify=y
    )
    print(f"Stratified Split: {len(X_train)} Training samples, {len(X_test)} Held-Out Test samples.")

    # 4. Candidate Models (All output calibrated probabilities)
    candidates = {
        "LogisticRegression": Pipeline([
            ("tfidf", TfidfVectorizer(max_features=3500, ngram_range=(1, 2), stop_words="english", sublinear_tf=True)),
            ("clf", LogisticRegression(max_iter=1000, class_weight="balanced", random_state=RANDOM_SEED))
        ]),
        "LinearSVM_Calibrated": Pipeline([
            ("tfidf", TfidfVectorizer(max_features=3500, ngram_range=(1, 2), stop_words="english", sublinear_tf=True)),
            ("clf", CalibratedClassifierCV(LinearSVC(class_weight="balanced", random_state=RANDOM_SEED, dual="auto"), cv=3))
        ]),
        "GradientBoosting": Pipeline([
            ("tfidf", TfidfVectorizer(max_features=2000, ngram_range=(1, 2), stop_words="english", sublinear_tf=True)),
            ("clf", GradientBoostingClassifier(n_estimators=35, max_depth=3, random_state=RANDOM_SEED))
        ])
    }

    results = {}
    best_model_name = None
    best_f1 = -1.0
    best_pipeline = None

    print("\nTraining and benchmarking 3 candidate architectures...")
    print("-" * 70)

    for name, pipeline in candidates.items():
        print(f"\n>>> Training {name}...")
        pipeline.fit(X_train, y_train)
        y_pred = pipeline.predict(X_test)

        acc = accuracy_score(y_test, y_pred)
        macro_f1 = f1_score(y_test, y_pred, average="macro")

        print(f"    Held-Out Test Accuracy: {acc * 100:.2f}%")
        print(f"    Held-Out Macro F1 Score: {macro_f1:.4f}")

        results[name] = {
            "accuracy": round(acc, 4),
            "macro_f1": round(macro_f1, 4),
            "classification_report": classification_report(y_test, y_pred, output_dict=True),
            "confusion_matrix": confusion_matrix(y_test, y_pred).tolist(),
            "classes": sorted(list(set(y_test)))
        }

        if macro_f1 > best_f1:
            best_f1 = macro_f1
            best_model_name = name
            best_pipeline = pipeline

    print("\n" + "=" * 70)
    print(f"BEST ARCHITECTURE: {best_model_name} (Macro F1 = {best_f1:.4f})")
    print("=" * 70)

    # 5. Save Model and Metrics Artifacts
    backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    models_dir = os.path.join(backend_dir, "app", "models")
    os.makedirs(models_dir, exist_ok=True)

    model_save_path = os.path.join(models_dir, "ats_role_model.joblib")
    metrics_save_path = os.path.join(models_dir, "ats_model_metrics.json")

    joblib.dump(best_pipeline, model_save_path)
    print(f"Saved trained joblib model to: {model_save_path}")

    metrics_payload = {
        "best_model": best_model_name,
        "dataset_name": "Kaggle UpdatedResumeDataSet.csv",
        "total_samples": len(df),
        "test_samples": len(X_test),
        "random_seed": RANDOM_SEED,
        "all_models_summary": {k: {"accuracy": v["accuracy"], "macro_f1": v["macro_f1"]} for k, v in results.items()},
        "best_model_details": results[best_model_name]
    }

    with open(metrics_save_path, "w", encoding="utf-8") as f:
        json.dump(metrics_payload, f, indent=2)
    print(f"Saved test evaluation metrics to: {metrics_save_path}")

    # 6. Print Classification Report for Best Model
    print("\nDetailed Per-Class Performance (Held-Out Test Set):")
    best_report = results[best_model_name]["classification_report"]
    for cls_name, metrics in best_report.items():
        if isinstance(metrics, dict) and "f1-score" in metrics:
            print(f"  - {cls_name:25s} Precision: {metrics['precision']:.2f} | Recall: {metrics['recall']:.2f} | F1: {metrics['f1-score']:.2f}")

    print("\nTraining and evaluation pipeline completed successfully!")

if __name__ == "__main__":
    train_and_evaluate_models()
