import joblib
import json
import numpy as np
from pathlib import Path

def extract_params():
    base_dir = Path(__file__).resolve().parent.parent
    model_dir = base_dir / "model"

    print("Loading model files...")
    model = joblib.load(model_dir / "best_model.pkl")
    scaler = joblib.load(model_dir / "scaler.pkl")
    columns = joblib.load(model_dir / "feature_columns.pkl")

    # Extract LogisticRegression parameters
    # coef_ is shape (1, n_features) for binary classification
    coef = model.coef_.flatten().tolist()
    intercept = float(model.intercept_[0])

    # Extract StandardScaler parameters
    # mean_ and scale_ are shape (n_features,)
    mean = scaler.mean_.tolist()
    scale = scaler.scale_.tolist()

    params = {
        "coef": coef,
        "intercept": intercept,
        "mean": mean,
        "scale": scale,
        "columns": columns
    }

    output_path = model_dir / "model_params.json"
    with open(output_path, "w") as f:
        json.dump(params, f, indent=2)
    
    print(f"Successfully saved model parameters to {output_path}")

if __name__ == "__main__":
    extract_params()
