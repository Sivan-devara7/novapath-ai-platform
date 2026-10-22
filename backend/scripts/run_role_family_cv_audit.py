"""
Role Family Prototype Audit:
Compares current strict multi-class accuracy vs family-aware accuracy on 5-fold CV across 102 real Kaggle resumes.
Role Families:
1. Software & Web: Backend Developer, Software Engineer (generic), Full Stack Developer, Frontend Developer
2. Cloud & Operations: Cloud & DevOps Engineer, SRE
3. Data & AI: Data Engineer, Data Scientist/ML Engineer, Data Analyst, AI Engineer
4. Standalone: Cybersecurity Analyst, Product Manager, QA/Test Automation Engineer, UI/UX Designer, Business Analyst, Mobile App Developer

Report only; does not change default prediction behavior.
"""

import os
import sys
import json
import numpy as np
from sklearn.model_selection import StratifiedKFold
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, backend_dir)

from scripts.train_ats_model import (
    load_and_deduplicate_kaggle,
    clean_and_sanitize_text
)

ROLE_FAMILIES = {
    "Backend Developer": "Software & Web",
    "Software Engineer (generic)": "Software & Web",
    "Full Stack Developer": "Software & Web",
    "Frontend Developer": "Software & Web",
    
    "Cloud & DevOps Engineer": "Cloud & Operations",
    "SRE": "Cloud & Operations",
    
    "Data Engineer": "Data & AI",
    "Data Scientist/ML Engineer": "Data & AI",
    "Data Analyst": "Data & AI",
    "AI Engineer": "Data & AI",
    
    "Cybersecurity Analyst": "Cybersecurity",
    "Product Manager": "Product Management",
    "QA/Test Automation Engineer": "QA & Testing",
    "UI/UX Designer": "Design",
    "Business Analyst": "Business Analysis",
    "Mobile App Developer": "Mobile"
}

def load_real_resumes():
    data_dir = os.path.join(backend_dir, "data")
    df_kaggle, _, _ = load_and_deduplicate_kaggle(data_dir)
    
    # Merge Frontend Developer (4 samples) into Software Engineer (generic)
    df_kaggle = df_kaggle.copy()
    orig_frontend_mask = df_kaggle["Category"] == "Frontend Developer"
    df_kaggle.loc[orig_frontend_mask, "Category"] = "Software Engineer (generic)"
    
    texts = [clean_and_sanitize_text(t) for t in df_kaggle["Resume"].tolist()]
    labels = df_kaggle["Category"].tolist()
    return texts, labels

from sklearn.svm import LinearSVC
from sklearn.calibration import CalibratedClassifierCV
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score

def run_family_audit():
    texts, labels = load_real_resumes()
    X_real = np.array(texts, dtype=str)
    y_real = np.array(labels, dtype=str)

    # Load synthetic data
    roles_dir = os.path.join(backend_dir, "data", "roles")
    synthetic_records = []
    for fname in os.listdir(roles_dir):
        if fname.endswith(".json"):
            with open(os.path.join(roles_dir, fname), "r", encoding="utf-8") as f:
                rdata = json.load(f)
            cat = rdata["role"]
            for s in rdata.get("synthetic_samples", []):
                cleaned = clean_and_sanitize_text(s["text"])
                synthetic_records.append({"Category": cat, "Cleaned_Resume": cleaned})

    X_synth = np.array([r["Cleaned_Resume"] for r in synthetic_records], dtype=str)
    y_synth = np.array([r["Category"] for r in synthetic_records], dtype=str)

    skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

    regimes_results = {}

    for regime_name, use_synthetic in [("(a) Real-Only Training", False), ("(b) Real + Synthetic (Equal)", True)]:
        fold_strict = []
        fold_family = []

        for train_idx, val_idx in skf.split(X_real, y_real):
            X_train, y_train = X_real[train_idx], y_real[train_idx]
            X_val, y_val = X_real[val_idx], y_real[val_idx]

            if use_synthetic:
                X_train = np.concatenate([X_train, X_synth])
                y_train = np.concatenate([y_train, y_synth])

            pipeline = Pipeline([
                ("tfidf", TfidfVectorizer(max_features=5000, ngram_range=(1, 2), stop_words="english", sublinear_tf=True)),
                ("clf", CalibratedClassifierCV(LinearSVC(class_weight="balanced", random_state=42, dual="auto"), cv=3))
            ])
            pipeline.fit(X_train, y_train)

            preds = pipeline.predict(X_val)

            # Strict Accuracy
            strict_acc = accuracy_score(y_val, preds)
            fold_strict.append(strict_acc)

            # Family-Aware Accuracy
            family_correct = sum(
                ROLE_FAMILIES.get(true_r, true_r) == ROLE_FAMILIES.get(pred_r, pred_r)
                for true_r, pred_r in zip(y_val, preds)
            )
            family_acc = family_correct / len(y_val)
            fold_family.append(family_acc)

        mean_strict = np.mean(fold_strict)
        ci_strict = 1.96 * (np.std(fold_strict) / np.sqrt(len(fold_strict)))
        mean_family = np.mean(fold_family)
        ci_family = 1.96 * (np.std(fold_family) / np.sqrt(len(fold_family)))

        regimes_results[regime_name] = {
            "strict_accuracy": round(mean_strict * 100, 2),
            "strict_ci_95": round(ci_strict * 100, 2),
            "family_accuracy": round(mean_family * 100, 2),
            "family_ci_95": round(ci_family * 100, 2),
            "gain": round((mean_family - mean_strict) * 100, 2)
        }

    print("\n=== ROLE FAMILY PROTOTYPE AUDIT (5-FOLD CV ON REAL DATA) ===")
    print(f"{'Regime':<30} | {'Strict Multi-Class Acc':<22} | {'Family-Aware Acc':<20} | {'Family Gain':<10}")
    print("-" * 90)
    for reg, res in regimes_results.items():
        print(f"{reg:<30} | {res['strict_accuracy']}% ± {res['strict_ci_95']}%{'':<6} | {res['family_accuracy']}% ± {res['family_ci_95']}%{'':<4} | +{res['gain']}%")

    out_path = os.path.join(backend_dir, "data", "role_family_cv_audit.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(regimes_results, f, indent=2)

if __name__ == "__main__":
    run_family_audit()
