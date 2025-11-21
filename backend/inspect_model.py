import joblib
from pathlib import Path
import sys

# Add backend to path
sys.path.append(str(Path(__file__).resolve().parent.parent))

def inspect_model():
    try:
        base_dir = Path(__file__).resolve().parent.parent
        model_dir = base_dir / "model"
        
        columns = joblib.load(model_dir / "feature_columns.pkl")
        print("---COLUMNS_START---")
        for col in columns:
            print(col)
        print("---COLUMNS_END---")
        
        scaler = joblib.load(model_dir / "scaler.pkl")
        print("Scaler Mean:", scaler.mean_)
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    inspect_model()
