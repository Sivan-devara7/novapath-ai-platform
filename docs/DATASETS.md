# NovaPath AI — Machine Learning Datasets Documentation

This document inventories the dataset used for training NovaPath AI's role-fit and ATS scoring models in accordance with open-source licensing and data governance guidelines.

---

## 1. Dataset Inventory

| Dataset Name | Source URL | License | Row Count | Attributes | Primary Use in NovaPath AI |
|---|---|---|---|---|---|
| **Updated Resume Dataset** | [Kaggle Dataset](https://www.kaggle.com/datasets/gauravduttakiit/resume-dataset) | **CC0: Public Domain** | **962** | `Category` (Target class, 25 categories)<br>`Resume` (Full unstructured text) | Pretrained text classification for role-fit matching (probability of matching target technical career role). |

---

## 2. Dataset Classification & Domain Categories

The dataset encompasses 25 technical and professional domains:
- **Core AI & Data:** `Data Science`, `Python Developer`, `Database`
- **Software Engineering:** `Java Developer`, `DotNet Developer`, `Web Designing`, `DevOps Engineer`
- **Systems & Infrastructure:** `Network Security Engineer`, `Hadoop`, `SAP Developer`, `Testing`
- **Other Disciplines:** `Mechanical Engineer`, `Electrical Engineering`, `Civil Engineer`, `Operations Manager`, `Sales`, `HR`, `Advocate`, `Arts`, `Business Analyst`, `Health and fitness`, `PMO`

---

## 3. Honest Architectural Scope: Role-Fit vs. ATS Score

> [!IMPORTANT]
> **Transparency Declaration:**  
> The Kaggle dataset contains historical resumes categorized by occupational field—it does **not** contain ground-truth ATS scores or numerical candidate ratings.  
> 
> Therefore, in NovaPath AI:
> 1. The trained Machine Learning model predicts **Role-Fit Probability** (the likelihood that the candidate's resume belongs to the target job category like Data Science or Python Developer).
> 2. The **ATS Compatibility Score (estimate)** is a deterministic, documented weighted blend:
>    - **40%** ML Role-Fit Probability
>    - **25%** Taxonomy-Based Keyword & Competency Coverage
>    - **15%** Section Completeness (Contact, Summary, Experience, Education, Skills, Projects)
>    - **10%** Formatting & Parsability Checks (bullet counts, length, table/image interference)
>    - **10%** Quantified Impact Bullets (percentages, numerical metrics, measurable outcomes)
> 3. Large Language Models (LLMs) are **never** the source of truth for numerical scores; they only assist in semantic bullet rewrites.

---

## 4. Licensing & Privacy Compliance

- **License:** CC0: Public Domain (No copyright restrictions on commercial or non-commercial research use).
- **PII Sanitation:** Text preprocessing pipelines in `scripts/train_ats_model.py` remove emails, URLs, telephone numbers, and special characters prior to feature extraction to preserve privacy.
- **Git Storage Policy:** Raw `.csv` files are explicitly ignored via `.gitignore` (`*.csv`). Only the training code and trained `.joblib` model artifacts are committed to version control.
