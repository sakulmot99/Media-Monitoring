# preprocessing/preprocessing_main.py
import pandas as pd
from pathlib import Path
from preprocessing.total_preprocessing import cleaning_pipeline

DATA_DIR = Path(__file__).resolve().parent.parent / "datasets"
RAW_DATA_PATH = DATA_DIR / "RAW_DATA.csv"
CLEAN_DATA_PATH = DATA_DIR / "CLEAN_DATA.csv"

def run_preprocessing():
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    # Load RAW_DATA.csv
    if RAW_DATA_PATH.exists():
        df_raw = pd.read_csv(RAW_DATA_PATH)
        print(f"Loaded {len(df_raw)} rows from RAW_DATA.csv")
    else:
        print("RAW_DATA.csv not found. Exiting.")
        return

    # Run cleaning pipeline
    df_clean = cleaning_pipeline(df_raw)

    # Save CLEAN_DATA.csv
    df_clean.to_csv(CLEAN_DATA_PATH, index=False)
    print(f"Saved CLEAN_DATA.csv with {len(df_clean)} rows")

if __name__ == "__main__":
    run_preprocessing()
