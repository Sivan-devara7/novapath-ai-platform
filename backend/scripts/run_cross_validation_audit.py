"""
5-Fold Stratified Cross-Validation on Deduplicated Real Kaggle Resumes (102 samples).
Compares:
(a) Real-only training
(b) Real + Synthetic (equal sample weights)
(c) Real + Synthetic with synthetic down-weighted (sample weight 0.20)
Evaluated ONLY on held-out real folds.
Reports accuracy with 95% confidence intervals, macro F1, and per-role results.
Also computes Probability Calibration metrics (Brier Score, Reliability).
"""

import os
import sys
import re
import json
import random
import numpy as np
import pandas as pd
from typing import Dict, Any, List, Tuple

from sklearn.model_selection import StratifiedKFold
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.calibration import CalibratedClassifierCV
from sklearn.metrics import accuracy_score, f1_score, classification_report, brier_score_loss
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import label_binarize

RANDOM_SEED = 42
random.seed(RANDOM_SEED)
np.random.seed(RANDOM_SEED)

backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data_dir = os.path.join(backend_dir, "data")
roles_dir = os.path.join(data_dir, "roles")
sys.path.insert(0, backend_dir)

from scripts.train_ats_model import (
    load_and_deduplicate_kaggle,
    clean_and_sanitize_text,
    ALL_TARGET_ROLES
)

def run_cross_validation():
    print("=" * 85)
    print("5-FOLD STRATIFIED CROSS-VALIDATION ON REAL RESUMES (EVALUATION ON REAL FOLDS ONLY)")
    print("=" * 85)

    # 1. Load deduplicated Kaggle data
    df_kaggle, raw_count, dupes_removed = load_and_deduplicate_kaggle(data_dir)
    print(f"Loaded {len(df_kaggle)} unique mapped real resumes.")

    # Merge Frontend Developer (4 samples) into Software Engineer (generic) to enable valid 5-fold stratification
    df_kaggle = df_kaggle.copy()
    orig_frontend_mask = df_kaggle["Category"] == "Frontend Developer"
    df_kaggle.loc[orig_frontend_mask, "Category"] = "Software Engineer (generic)"
    print("Note: Merged 'Frontend Developer' (4 samples) into 'Software Engineer (generic)' for 5-fold stratification (min class count >= 5).")

    classes_list = sorted(df_kaggle["Category"].unique().tolist())
    print(f"9 Stratified Real Classes: {classes_list}")
    for c in classes_list:
        print(f"  - {c}: {sum(df_kaggle['Category'] == c)} samples")

    # 2. Load Synthetic Resumes
    print("\nLoading synthetic resumes from generation pipeline...")
    # Load or generate synthetic dataset
    from scripts.train_ats_model import generate_diverse_synthetic_resume
    synthetic_records = []
    for role in ALL_TARGET_ROLES:
        slug = re.sub(r"[^a-zA-Z0-9]+", "-", role.lower()).strip("-")
        bench_path = os.path.join(roles_dir, f"{slug}.json")
        with open(bench_path, "r", encoding="utf-8") as f:
            bench_data = json.load(f)
        for i in range(55):
            doc = generate_diverse_synthetic_resume(role, bench_data, i)
            # Map Frontend Developer in synthetic data to SWE as well for fair 9-class real comparison in CV
            cat = doc["Category"]
            if cat == "Frontend Developer":
                cat = "Software Engineer (generic)"
            synthetic_records.append({
                "Category": cat,
                "Cleaned_Resume": doc["Cleaned_Resume"],
                "is_synthetic": True
            })
    df_synth = pd.DataFrame(synthetic_records)
    print(f"Loaded {len(df_synth)} synthetic samples across all roles.")

    # 3. Setup 5-Fold Stratified K-Fold on REAL data only
    skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=RANDOM_SEED)

    X_real = np.array(df_kaggle["Cleaned_Resume"].tolist(), dtype=str)
    y_real = np.array(df_kaggle["Category"].tolist(), dtype=str)

    regimes = ["(a) Real-Only Training", "(b) Real + Synthetic (Equal Weights)", "(c) Real + Synthetic (Down-Weighted 0.20)"]
    fold_metrics = {r: {"accuracy": [], "macro_f1": [], "brier": [], "reports": []} for r in regimes}

    for fold_idx, (train_idx, test_idx) in enumerate(skf.split(X_real, y_real), 1):
        print(f"\n--- Running Fold {fold_idx}/5 (Real Train: {len(train_idx)}, Real Test: {len(test_idx)}) ---")
        X_real_train, y_real_train = X_real[train_idx], y_real[train_idx]
        X_real_test, y_real_test = X_real[test_idx], y_real[test_idx]

        # Regime (a): Real-Only Training
        pipe_a = Pipeline([
            ("tfidf", TfidfVectorizer(max_features=5000, ngram_range=(1, 2), stop_words="english", sublinear_tf=True)),
            ("clf", CalibratedClassifierCV(LinearSVC(class_weight="balanced", random_state=RANDOM_SEED, dual="auto"), cv=3))
        ])
        pipe_a.fit(X_real_train, y_real_train)
        pred_a = pipe_a.predict(X_real_test)
        prob_a = pipe_a.predict_proba(X_real_test)
        acc_a = accuracy_score(y_real_test, pred_a)
        f1_a = f1_score(y_real_test, pred_a, average="macro", zero_division=0)
        rep_a = classification_report(y_real_test, pred_a, output_dict=True, zero_division=0)

        # Multi-class Brier score
        classes_a = list(pipe_a.classes_)
        y_test_bin_a = label_binarize(y_real_test, classes=classes_a)
        brier_a = np.mean(np.sum((prob_a - y_test_bin_a) ** 2, axis=1))

        fold_metrics["(a) Real-Only Training"]["accuracy"].append(acc_a)
        fold_metrics["(a) Real-Only Training"]["macro_f1"].append(f1_a)
        fold_metrics["(a) Real-Only Training"]["brier"].append(brier_a)
        fold_metrics["(a) Real-Only Training"]["reports"].append(rep_a)

        # Prepare combined data for (b) and (c)
        X_comb = np.concatenate([X_real_train, df_synth["Cleaned_Resume"].values])
        y_comb = np.concatenate([y_real_train, df_synth["Category"].values])

        # Regime (b): Real + Synthetic (Equal Weights)
        pipe_b = Pipeline([
            ("tfidf", TfidfVectorizer(max_features=5000, ngram_range=(1, 2), stop_words="english", sublinear_tf=True)),
            ("clf", CalibratedClassifierCV(LinearSVC(class_weight="balanced", random_state=RANDOM_SEED, dual="auto"), cv=3))
        ])
        pipe_b.fit(X_comb, y_comb)
        pred_b = pipe_b.predict(X_real_test)
        prob_b = pipe_b.predict_proba(X_real_test)
        acc_b = accuracy_score(y_real_test, pred_b)
        f1_b = f1_score(y_real_test, pred_b, average="macro", zero_division=0)
        rep_b = classification_report(y_real_test, pred_b, output_dict=True, zero_division=0)

        classes_b = list(pipe_b.classes_)
        y_test_bin_b = label_binarize(y_real_test, classes=classes_b)
        brier_b = np.mean(np.sum((prob_b - y_test_bin_b) ** 2, axis=1))

        fold_metrics["(b) Real + Synthetic (Equal Weights)"]["accuracy"].append(acc_b)
        fold_metrics["(b) Real + Synthetic (Equal Weights)"]["macro_f1"].append(f1_b)
        fold_metrics["(b) Real + Synthetic (Equal Weights)"]["brier"].append(brier_b)
        fold_metrics["(b) Real + Synthetic (Equal Weights)"]["reports"].append(rep_b)

        # Regime (c): Real + Synthetic (Down-Weighted 0.20)
        weights_c = np.concatenate([np.ones(len(X_real_train)), np.full(len(df_synth), 0.20)])
        # In scikit-learn Pipeline with CalibratedClassifierCV, sample_weight passes to fit via clf__sample_weight
        pipe_c = Pipeline([
            ("tfidf", TfidfVectorizer(max_features=5000, ngram_range=(1, 2), stop_words="english", sublinear_tf=True)),
            ("clf", CalibratedClassifierCV(LinearSVC(class_weight="balanced", random_state=RANDOM_SEED, dual="auto"), cv=3))
        ])
        # Transform tfidf first
        X_comb_vec = pipe_c.named_steps["tfidf"].fit_transform(X_comb)
        pipe_c.named_steps["clf"].fit(X_comb_vec, y_comb, sample_weight=weights_c)
        X_test_vec = pipe_c.named_steps["tfidf"].transform(X_real_test)
        pred_c = pipe_c.named_steps["clf"].predict(X_test_vec)
        prob_c = pipe_c.named_steps["clf"].predict_proba(X_test_vec)

        acc_c = accuracy_score(y_real_test, pred_c)
        f1_c = f1_score(y_real_test, pred_c, average="macro", zero_division=0)
        rep_c = classification_report(y_real_test, pred_c, output_dict=True, zero_division=0)

        classes_c = list(pipe_c.named_steps["clf"].classes_)
        y_test_bin_c = label_binarize(y_real_test, classes=classes_c)
        brier_c = np.mean(np.sum((prob_c - y_test_bin_c) ** 2, axis=1))

        fold_metrics["(c) Real + Synthetic (Down-Weighted 0.20)"]["accuracy"].append(acc_c)
        fold_metrics["(c) Real + Synthetic (Down-Weighted 0.20)"]["macro_f1"].append(f1_c)
        fold_metrics["(c) Real + Synthetic (Down-Weighted 0.20)"]["brier"].append(brier_c)
        fold_metrics["(c) Real + Synthetic (Down-Weighted 0.20)"]["reports"].append(rep_c)

        print(f"  Regime (a) Real-Only     -> Acc: {acc_a*100:.1f}%, Macro F1: {f1_a:.4f}, Brier: {brier_a:.4f}")
        print(f"  Regime (b) Real + Synth  -> Acc: {acc_b*100:.1f}%, Macro F1: {f1_b:.4f}, Brier: {brier_b:.4f}")
        print(f"  Regime (c) Down-Weighted -> Acc: {acc_c*100:.1f}%, Macro F1: {f1_c:.4f}, Brier: {brier_c:.4f}")

    # Compute Summary Statistics & 95% Confidence Intervals
    summary = {}
    for r in regimes:
        accs = np.array(fold_metrics[r]["accuracy"])
        f1s = np.array(fold_metrics[r]["macro_f1"])
        briers = np.array(fold_metrics[r]["brier"])

        acc_mean = float(np.mean(accs))
        acc_std = float(np.std(accs, ddof=1))
        acc_ci = float(1.96 * acc_std / np.sqrt(5))

        f1_mean = float(np.mean(f1s))
        f1_std = float(np.std(f1s, ddof=1))
        f1_ci = float(1.96 * f1_std / np.sqrt(5))

        brier_mean = float(np.mean(briers))

        summary[r] = {
            "accuracy_mean": round(acc_mean, 4),
            "accuracy_ci_95": round(acc_ci, 4),
            "accuracy_formatted": f"{acc_mean*100:.2f}% ± {acc_ci*100:.2f}%",
            "macro_f1_mean": round(f1_mean, 4),
            "macro_f1_ci_95": round(f1_ci, 4),
            "macro_f1_formatted": f"{f1_mean:.4f} ± {f1_ci:.4f}",
            "brier_score_mean": round(brier_mean, 4),
            "folds_accuracy": [round(a, 4) for a in accs.tolist()],
            "folds_f1": [round(f, 4) for f in f1s.tolist()]
        }

    # Aggregate per-role metrics across the 5 folds for each regime
    per_role_summary = {r: {} for r in regimes}
    for r in regimes:
        for c in classes_list:
            precisions = [rep[c]["precision"] for rep in fold_metrics[r]["reports"] if c in rep]
            recalls = [rep[c]["recall"] for rep in fold_metrics[r]["reports"] if c in rep]
            f1_scores = [rep[c]["f1-score"] for rep in fold_metrics[r]["reports"] if c in rep]
            supports = [rep[c]["support"] for rep in fold_metrics[r]["reports"] if c in rep]
            per_role_summary[r][c] = {
                "precision": round(float(np.mean(precisions)), 2) if precisions else 0.0,
                "recall": round(float(np.mean(recalls)), 2) if recalls else 0.0,
                "f1": round(float(np.mean(f1_scores)), 2) if f1_scores else 0.0,
                "total_support": int(sum(supports))
            }

    # Save artifact
    output_path = os.path.join(data_dir, "cv_audit_results.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump({
            "stratified_folds": 5,
            "classes": classes_list,
            "summary": summary,
            "per_role_summary": per_role_summary
        }, f, indent=2)

    print("\n" + "=" * 85)
    print("5-FOLD CROSS-VALIDATION SUMMARY (EVALUATED ONLY ON HELD-OUT REAL RESUMES)")
    print("=" * 85)
    print(f"{'Training Regime':<42} | {'Mean Accuracy (95% CI)':24s} | {'Macro F1 (95% CI)':20s} | {'Brier Score':12s}")
    print("-" * 105)
    for r in regimes:
        s = summary[r]
        print(f"{r:<42} | {s['accuracy_formatted']:24s} | {s['macro_f1_formatted']:20s} | {s['brier_score_mean']:<12.4f}")

    print("\nPer-Role F1 Score by Training Regime Across Held-Out Real Folds:")
    print(f"{'Role':<32} | {'Support':7s} | {'(a) Real-Only':14s} | {'(b) Real+Synth':15s} | {'(c) Down-Weighted':18s}")
    print("-" * 92)
    for c in classes_list:
        f1_a = per_role_summary["(a) Real-Only Training"][c]["f1"]
        f1_b = per_role_summary["(b) Real + Synthetic (Equal Weights)"][c]["f1"]
        f1_c = per_role_summary["(c) Real + Synthetic (Down-Weighted 0.20)"][c]["f1"]
        sup = per_role_summary["(a) Real-Only Training"][c]["total_support"]
        print(f"{c:<32} | {sup:<7d} | {f1_a:<14.2f} | {f1_b:<15.2f} | {f1_c:<18.2f}")

    print(f"\nAudit results successfully saved to: {output_path}")

if __name__ == "__main__":
    run_cross_validation()
