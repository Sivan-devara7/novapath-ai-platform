# NovaPath AI — Machine Learning Datasets Documentation

This document inventories the dataset used for training NovaPath AI's role-fit and ATS scoring models in accordance with open-source licensing and data governance guidelines.

---

## 1. Dataset Inventory

| Dataset Name | Source URL | License | Row Count | Attributes | Primary Use in NovaPath AI |
|---|---|---|---|---|---|
| **Updated Resume Dataset** | [Kaggle Dataset](https://www.kaggle.com/datasets/gauravduttakiit/resume-dataset) | **CC0: Public Domain** | **962** | `Category` (25 categories)<br>`Resume` (Full unstructured text) | Historical baseline text classification mapped to primary technical career roles. |
| **Augmented Multi-Role Resume Dataset** | Local pipeline (`backend/data/augmented_resume_dataset.csv`) | Generated + CC0 Derived | **1,154** (634 Public Kaggle, 520 Synthetic) | `Category` (16 Target Roles)<br>`Resume`<br>`is_synthetic` (Boolean flag) | Stratified multi-class role-fit model training across all 16 career roles. |

---

## 2. Dataset Classification & 16 Target Career Roles

The expanded library covers 16 engineering, product, data, and design roles:
- **Software Engineering:** `Frontend Developer`, `Backend Developer`, `Full Stack Developer`, `Software Engineer (generic)`, `Mobile App Developer`
- **AI, ML & Data:** `AI Engineer`, `Data Scientist/ML Engineer`, `Data Analyst`, `Data Engineer`
- **Cloud, Systems & Security:** `Cloud & DevOps Engineer`, `Site Reliability Engineer (SRE)`, `Cybersecurity Analyst`, `QA/Test Automation Engineer`
- **Product, Design & Business:** `Product Manager`, `UI/UX Designer`, `Business Analyst`

---

## 3. Honest Architectural Scope: Role-Fit vs. ATS Score

> [!IMPORTANT]
> **Transparency Declaration:**  
> The Kaggle dataset contains historical resumes categorized by occupational field—it does **not** contain ground-truth ATS scores or numerical candidate ratings.  
> Synthetic resumes generated to cover underrepresented tracks (e.g. SRE, Mobile App Developer, UI/UX Designer) are explicitly flagged with `is_synthetic: true`.
> 
> In NovaPath AI, the scoring weights stay strictly unchanged:
> 1. The trained Machine Learning model predicts **Role-Fit Probability** across 16 target roles.
> 2. The **ATS Compatibility Score (estimate)** is a deterministic, documented weighted blend:
>    - **40%** ML Role-Fit Probability
>    - **25%** Taxonomy-Based Keyword & Competency Coverage (Normalized via `SkillNormalizer`)
>    - **15%** Section Completeness (Standard sections + role-specific rules like mandatory portfolio links)
>    - **10%** Formatting & Parsability Checks (bullet counts, length, monolithic text prevention)
>    - **10%** Quantified Impact Bullets (percentages, numerical metrics, measurable outcomes)
> 3. Large Language Models (LLMs) are **never** the source of truth for numerical scores; they only assist in semantic bullet rewrites.

---

## 4. Licensing & Privacy Compliance

- **License:** CC0: Public Domain (No copyright restrictions on commercial or non-commercial research use).
- **Synthetic Transparency:** Every synthetic sample is explicitly marked with `is_synthetic: true` in `backend/data/augmented_resume_dataset.csv`.
- **PII Sanitation:** Text preprocessing pipelines in `scripts/train_ats_model.py` remove emails, URLs, telephone numbers, and special characters prior to feature extraction to preserve privacy.
- **Git Storage Policy:** Raw `.csv` files are explicitly ignored via `.gitignore` (`*.csv`). Only the training code, versioned role JSONs in `backend/data/roles/`, and trained `.joblib` model artifacts are committed to version control.
