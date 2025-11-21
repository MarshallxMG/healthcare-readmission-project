import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
import joblib
import numpy as np

def main():
    df = pd.read_csv("data/processed_minimal.csv")

    X = df.drop("label", axis=1)
    y = df["label"]

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y, test_size=0.2, random_state=42, stratify=y
    )

    model = LogisticRegression(max_iter=2000)
    model.fit(X_train, y_train)

    preds = model.predict_proba(X_test)[:, 1]
    auc = roc_auc_score(y_test, preds)

    print("AUC:", auc)

    joblib.dump(model, "model/best_model.pkl")
    joblib.dump(list(X.columns), "model/feature_columns.pkl")
    joblib.dump(scaler, "model/scaler.pkl")

    print("Saved model & features successfully.")

if __name__ == "__main__":
    main()
