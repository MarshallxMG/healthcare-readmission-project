# scripts/preprocess_full.py
import os
import pandas as pd
import numpy as np

# -------------- config --------------
RAW = "data/diabetic_data.csv"
OUT = "data/processed_full.csv"
FEATURES_OUT = "model/feature_columns.pkl"
os.makedirs("data", exist_ok=True)
os.makedirs("model", exist_ok=True)

# -------------- helpers --------------
def diag_to_group(x):
    try:
        if pd.isna(x): return "missing"
        s = str(x).strip()
        if s == "" or s == "?": return "missing"
        if s[0] in ("V", "E"): return "other"
        num = int(float(s))
        if 390 <= num <= 459: return "circulatory"
        if 460 <= num <= 519: return "respiratory"
        if 520 <= num <= 579: return "digestive"
        if 250 <= num <= 250: return "diabetes"
        if 580 <= num <= 629: return "genitourinary"
        if 140 <= num <= 239: return "neoplasms"
        if 800 <= num <= 999: return "injury"
        if 710 <= num <= 739: return "musculoskeletal"
        return "other"
    except:
        return "other"

def age_to_mid(a):
    try:
        s = str(a).replace("[", "").replace(")", "")
        lo, hi = s.split("-")
        return (int(lo) + int(hi)) / 2
    except:
        return np.nan

# -------------- load --------------
print("Loading raw data...")
df = pd.read_csv(RAW, low_memory=False)
df = df.replace("?", np.nan)

# -------------- label --------------
print("Creating label...")
df["label"] = df["readmitted"].apply(lambda x: 1 if x == "<30" else 0)

# -------------- drop ids --------------
for col in ("encounter_id", "patient_nbr", "weight"):
    if col in df.columns:
        df.drop(columns=[col], inplace=True)

# -------------- diag groups --------------
for col in ("diag_1", "diag_2", "diag_3"):
    if col in df.columns:
        df[col] = df[col].astype(str).fillna("missing")
        df[col + "_grp"] = df[col].apply(diag_to_group)
        df.drop(columns=[col], inplace=True)

# -------------- age --------------
if "age" in df.columns:
    df["age_mid"] = df["age"].apply(age_to_mid)
    df.drop(columns=["age"], inplace=True)

# -------------- meds mapping --------------
med_map = {"No": 0, "Steady": 1, "Up": 2, "Down": 2}
med_cols = [c for c in df.columns if c.lower() in {
    "metformin","repaglinide","nateglinide","chlorpropamide","glimepiride",
    "acetohexamide","glipizide","glyburide","tolbutamide","pioglitazone",
    "rosiglitazone","acarbose","miglitol","tolazamide","insulin",
    "glyburide-metformin","glipizide-metformin","glimepiride-pioglitazone",
    "metformin-rosiglitazone","metformin-pioglitazone"
}]
for m in med_cols:
    df[m] = df[m].map(med_map).fillna(0).astype(int)

# -------------- fill and dummies --------------
print("Converting remaining categoricals to dummies...")
# Fill objects
for c in df.select_dtypes(include=["object"]).columns:
    df[c] = df[c].fillna("missing").astype(str)

# One-hot encode all object columns (will produce numeric-only DF)
cat_cols = df.select_dtypes(include=["object"]).columns.tolist()
if cat_cols:
    df = pd.get_dummies(df, columns=cat_cols, dummy_na=False)

# Ensure numeric
df = df.fillna(0)

# -------------- save --------------
print("Saving processed dataset to:", OUT)
df.to_csv(OUT, index=False)

# feature columns (exclude label)
feature_cols = [c for c in df.columns if c != "label"]
pd.Series(feature_cols).to_pickle(FEATURES_OUT)

print("Saved feature_columns ->", FEATURES_OUT)
print("Processed shape:", df.shape)
