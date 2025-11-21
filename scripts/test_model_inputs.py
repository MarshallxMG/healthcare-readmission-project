# scripts/test_model_inputs.py
import joblib, os, json
import pandas as pd

MODEL = "model/best_model.pkl"
SCALER = "model/scaler.pkl"
FEATURES = "model/feature_columns.pkl"

def load():
    model = joblib.load(MODEL)
    scaler = joblib.load(SCALER)
    cols = joblib.load(FEATURES)
    return model, scaler, cols

def prepare_row(cols, scaler, input_dict):
    row = {c: 0 for c in cols}
    for k,v in input_dict.items():
        if k in row:
            row[k] = v
        else:
            # show unmatched keys
            print(f"WARNING: input key '{k}' not found in feature columns")
            row.setdefault(k, v)
    df = pd.DataFrame([row])
    # transform numeric
    num_cols = df.select_dtypes(include=['number']).columns.tolist()
    try:
        df[num_cols] = scaler.transform(df[num_cols])
    except Exception as e:
        print("Scaler transform failed:", e)
    return df

def run_case(name, model, scaler, cols, d):
    print("\n=== CASE:", name, "===")
    df = prepare_row(cols, scaler, d)
    print("prepared row (first 50 cols shown):")
    print(df.iloc[0].iloc[:50].to_dict())
    prob = model.predict_proba(df)[:,1][0]
    pred = int(prob >= 0.5)
    print("probability:", prob, "pred:", pred)
    return prob

if __name__ == "__main__":
    model, scaler, cols = load()
    # low
    low = {
      "time_in_hospital": 2,
      "num_lab_procedures": 22,
      "num_procedures": 0,
      "num_medications": 10,
      "number_outpatient": 0,
      "number_inpatient": 0,
      "number_emergency": 0
    }
    # medium
    med = {
      "time_in_hospital": 7,
      "num_lab_procedures": 55,
      "num_procedures": 2,
      "num_medications": 22,
      "number_outpatient": 2,
      "number_inpatient": 1,
      "number_emergency": 1
    }
    # high
    high = {
      "time_in_hospital": 14,
      "num_lab_procedures": 90,
      "num_procedures": 5,
      "num_medications": 45,
      "number_outpatient": 8,
      "number_inpatient": 6,
      "number_emergency": 4
    }

    run_case("LOW", model, scaler, cols, low)
    run_case("MEDIUM", model, scaler, cols, med)
    run_case("HIGH", model, scaler, cols, high)
