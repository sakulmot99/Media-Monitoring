# parties/parties_main.py

"""
Main Script for Partisan Bias Analysis

This script ties together the preprocessing, party mention collection,
and aggregation functions to analyze partisan bias in cleaned articles.

Workflow:
1. Load CLEAN_DATA.csv (produced by preprocessing pipeline)
2. Preprocess the text (lowercasing, removing punctuation and extra spaces)
3. Count mentions of political parties using PARTY_SYNONYM_DICT
4. Aggregate weekly counts and percentages per publisher
5. Save outputs as:
    - PARTIES_DATA.csv : per-article party mentions
    - PARTIES_ANALYSIS.csv : weekly aggregated mentions per publisher

Absolute Imports:
    - parties_config: PARTY_SYNONYM_DICT, PARTIES, PUBLISHERS
    - parties_preprocessing: main_discourse_preprocessing
    - parties_functions: party_mention_collect, party_counts_aggregation

Inputs:
    - datasets/CLEAN_DATA.csv : cleaned articles DataFrame

Outputs:
    - datasets/PARTIES_DATA.csv : per-article party mentions
    - datasets/PARTIES_ANALYSIS.csv : weekly aggregation per publisher

Usage:
    python parties/parties_main.py

"""

from pathlib import Path
import pandas as pd

from parties.parties_config import PARTY_SYNONYM_DICT, PARTIES, PUBLISHERS
from parties.parties_preprocessing import main_discourse_preprocessing
from parties.parties_functions import party_mention_collect, party_counts_aggregation

# ------------------------------
# File paths
# ------------------------------
DATA_DIR = Path(__file__).resolve().parent.parent / "datasets"
CLEAN_DATA_PATH = DATA_DIR / "CLEAN_DATA.csv"
PARTIES_DATA_PATH = DATA_DIR / "PARTIES_DATA.csv"
PARTIES_ANALYSIS_PATH = DATA_DIR / "PARTIES_ANALYSIS.csv"

# ------------------------------
# Main parties pipeline
# ------------------------------
def run_parties_analysis():
    """
    Run the full pipeline for party mentions analysis.

    Steps:
    1. Load CLEAN_DATA.csv from datasets/
    2. Preprocess the 'content' column
    3. Count party mentions per article using synonyms
    4. Aggregate mentions weekly per publisher
    5. Save PARTIES_DATA.csv and PARTIES_ANALYSIS.csv in datasets/

    Returns:
        None
    """
    # Load cleaned data
    if not CLEAN_DATA_PATH.exists():
        print("CLEAN_DATA.csv not found. Exiting.")
        return

    df_clean = pd.read_csv(CLEAN_DATA_PATH)
    print(f"Loaded CLEAN_DATA.csv with {len(df_clean)} rows")

    # Run main parties pipeline
    df_parties, df_parties_analysis = main_parties(df_clean, PARTY_SYNONYM_DICT, PARTIES, PUBLISHERS)

    # Save outputs
    df_parties.to_csv(PARTIES_DATA_PATH, index=False)
    df_parties_analysis.to_csv(PARTIES_ANALYSIS_PATH, index=False)
    print(f"Saved PARTIES_DATA.csv with {len(df_parties)} rows")
    print(f"Saved PARTIES_ANALYSIS.csv with {len(df_parties_analysis)} rows")


if __name__ == "__main__":
    run_parties_analysis()
