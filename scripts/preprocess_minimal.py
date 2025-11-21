import pandas as pd

def main():
    df = pd.read_csv("data/diabetic_data.csv")

    df = df.replace("?", pd.NA)

    df["label"] = df["readmitted"].apply(lambda x: 1 if x in ["<30"] else 0)

    df = df[[
        "time_in_hospital",
        "num_lab_procedures",
        "num_procedures",
        "num_medications",
        "number_outpatient",
        "number_inpatient",
        "number_emergency",
        "label"
    ]]

    df.to_csv("data/processed_minimal.csv", index=False)
    print("Saved: data/processed_minimal.csv")

if __name__ == "__main__":
    main()
