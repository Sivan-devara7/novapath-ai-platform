import pandas as pd
import hashlib
import re

def clean_text(text):
    if not isinstance(text, str):
        return ""
    text = re.sub(r"https?://\S+|www\.\S+", " ", text)
    text = re.sub(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", " ", text)
    text = re.sub(r"\+?\d[\d -]{8,}\d", " ", text)
    text = re.sub(r"[^\w\s]", " ", text)
    return re.sub(r"\s+", " ", text).strip().lower()

df = pd.read_csv("backend/data/UpdatedResumeDataSet.csv")
print("=" * 60)
print("KAGGLE DATASET DUPLICATION AUDIT")
print("=" * 60)
print(f"Total rows in Kaggle dataset: {len(df)}")
print(f"Exact string unique resumes: {df['Resume'].nunique()}")
print(f"Exact string duplicates: {df['Resume'].duplicated().sum()}")

# Cleaned text deduplication
df["Cleaned"] = df["Resume"].apply(clean_text)
print(f"Unique after text sanitation: {df['Cleaned'].nunique()}")
print(f"Duplicates after text sanitation: {df['Cleaned'].duplicated().sum()}")

# Per category duplication
print("\nDuplicates per category:")
for cat, group in df.groupby("Category"):
    dups = group["Cleaned"].duplicated().sum()
    print(f"  - {cat:26s}: Total={len(group):2d} | Unique={group['Cleaned'].nunique():2d} | Duplicates={dups:2d}")
