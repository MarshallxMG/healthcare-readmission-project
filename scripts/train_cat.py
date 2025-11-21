# scripts/train_cat.py
import os
import joblib
import pandas as pd
import numpy as np
from catboost import CatBoostClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import roc_auc_score
from imblearn.over_sampling import SMOTE

os.makedirs("model", exist_ok=True)

DATA = "data/processed_full.csv"
FEATURES_IN = "model/feature_columns.pkl"

print("Loading processed data...")
df = pd.read_csv(DATA)
if "label" not in df.columns:
    raise SystemExit("No 'label' column found in processed data.")

X = df.drop("label", axis=1)
y = df["label"].astype(int)

# numeric columns for scaling
numeric_cols = X.select_dtypes(include=[np.number]).columns.tolist()

print("Train/test split...")
X_train, X_hold, y_train, y_hold = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print("Scaling numeric columns...")
scaler = StandardScaler()
X_train[numeric_cols] = scaler.fit_transform(X_train[numeric_cols])
X_hold[numeric_cols] = scaler.transform(X_hold[numeric_cols])

print("Applying SMOTE to balance classes...")
sm = SMOTE(random_state=42)
X_res, y_res = sm.fit_resample(X_train, y_train)

print("Training CatBoost (may take a while)...")
model = CatBoostClassifier(
    iterations=1000,
    learning_rate=0.03,
    depth=8,
    random_seed=42,
    verbose=200
)
# no categorical indices since we used get_dummies
model.fit(X_res, y_res)

print("Evaluating...")
probs = model.predict_proba(X_hold)[:, 1]
auc = roc_auc_score(y_hold, probs)
print("CatBoost AUC:", auc)

print("Saving model and scaler...")
joblib.dump(model, "model/best_model.pkl")
joblib.dump(scaler, "model/scaler.pkl")
joblib.dump(X.columns.tolist(), "model/feature_columns.pkl")

print("Saved -> model/best_model.pkl, model/scaler.pkl, model/feature_columns.pkl")
