import json
import numpy as np
from pathlib import Path

model_handler = None

class ModelHandler:
    def __init__(self):
        self.coef = None
        self.intercept = None
        self.mean = None
        self.scale = None
        self.columns = None
        self.load_model()

    def load_model(self):
        try:
            base_dir = Path(__file__).resolve().parent.parent
            model_path = base_dir / "model" / "model_params.json"
            
            with open(model_path, "r") as f:
                params = json.load(f)
                
            self.coef = np.array(params["coef"])
            self.intercept = params["intercept"]
            self.mean = np.array(params["mean"])
            self.scale = np.array(params["scale"])
            self.columns = params["columns"]
            
        except Exception as e:
            print(f"Error loading model: {e}")

    def predict(self, data_dict):
        if self.coef is None:
            self.load_model()
            if self.coef is None:
                raise RuntimeError("Model not loaded")

        # Prepare input vector
        ordered = [data_dict[col] for col in self.columns]
        X = np.array(ordered)
        
        # Scale input: (X - mean) / scale
        X_scaled = (X - self.mean) / self.scale
        
        # Linear combination: dot(X_scaled, coef) + intercept
        z = np.dot(X_scaled, self.coef) + self.intercept
        
        # Sigmoid function: 1 / (1 + exp(-z))
        prob = 1 / (1 + np.exp(-z))
        
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
