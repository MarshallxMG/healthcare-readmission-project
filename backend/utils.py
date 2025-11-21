import joblib
import numpy as np
from pathlib import Path

model_handler = None

class ModelHandler:
    def __init__(self):
        self.model = None
        self.columns = None
        self.scaler = None
        self.load_model()

    def load_model(self):
        try:
            base_dir = Path(__file__).resolve().parent.parent
            model_dir = base_dir / "model"
            
            self.model = joblib.load(model_dir / "best_model.pkl")
            self.columns = joblib.load(model_dir / "feature_columns.pkl")
            self.scaler = joblib.load(model_dir / "scaler.pkl")
        except Exception as e:
            print(f"Error loading model: {e}")

    def predict(self, data_dict):
        if not self.model:
            self.load_model()
            if not self.model:
                raise RuntimeError("Model not loaded")

        ordered = [data_dict[col] for col in self.columns]
        X = np.array([ordered])
        X_scaled = self.scaler.transform(X)

        prob = self.model.predict_proba(X_scaled)[0][1]
        pred = 1 if prob >= 0.50 else 0
        
        risk_label = self.get_risk_label(prob)

        return pred, float(prob), risk_label

    def get_risk_label(self, prob):
        # Thresholds adjusted for better calibration based on model output distribution
        # < 15%: Low Risk
        # 15% - 35%: Medium Risk
        # > 35%: High Risk
        if prob < 0.15: return "LOW RISK"
        if prob < 0.35: return "MEDIUM RISK"
        return "HIGH RISK"

model_handler = ModelHandler()
