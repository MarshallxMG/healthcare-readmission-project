# backend/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

# Correct import — utils is inside backend folder
from backend.utils import model_handler

app = FastAPI(title="Healthcare Readmission Prediction API")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # Allow all origins for local development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request model
class PredictRequest(BaseModel):
    data: dict

@app.get("/")
def home():
    return {"status": "API running"}

@app.get("/health")
def health_check():
    """Quick health check endpoint."""
    return {"status": "ok", "model_loaded": model_handler.coef is not None}

@app.post("/predict")
def predict(req: PredictRequest):
    """
    Returns:
      - prediction (0/1)
      - probability (float)
      - risk_label ("LOW", "MEDIUM", "HIGH")
    """
    # Ensure model is loaded (lazy loading check)
    if model_handler.coef is None:
        model_handler.load_model()
        
    pred, prob, risk_label = model_handler.predict(req.data)
    return {
        "prediction": int(pred),
        "probability": float(prob),
        "risk_label": risk_label
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
