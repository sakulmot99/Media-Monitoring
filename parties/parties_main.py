# parties/parties_main.py

"""
Main Script for Partisan Bias Analysis

This script ties together the preprocessing, party mention collection,
and aggregation functions to analyze partisan bias in cleaned articles.

Workflow:
1. Load CLEAN_DATA.csv (produed by preprocessing pipeline)
2. Preprocess the text (lowercasing, removing punctuation and extra spaces)
3. Count mentions of political parties using PARTY_SYNONYM_DICT
4. Aggregate weekly counts and percentages per publisher
5. Save outputs as:
    - PARTIES_DATA.csv : per-article party mentions
    - PARTIES_ANALYSIS.csv : weekly aggregated mentions per publisher

Usage:
    python -m parties.parties_main
"""

from pathlib import Path
import pandas as pd

from parties.parties_config import PARTY_SYNONYM_DICT, PARTIES, PUBLISHERS
from parties.parties_preprocessing import main_discourse_preprocessing
from parties.parties_functions import (
    party_mention_collect,
    party_counts_aggregation,
)

# ------------------------------
# File paths
# ------------------------------
DATA_DIR = Path(__file__).resolve().parent.parent / "datasets"
CLEAN_DATA_PATH = DATA_DIR / "CLEAN_DATA.csv"
PARTIES_DATA_PATH = DATA_DIR / "PARTIES_DATA.csv"
PARTIES_ANALYSIS_PATH = DATA_DIR / "PARTIES_ANALYSIS.csv"

# ------------------------------
# Core pipeline logic
# ------------------------------
def main_parties(df, PARTY_SYNONYM_DICT, PARTIES, PUBLISHERS):
    """
    Run preprocessing, party mention collection, and aggregation.

    Returns:
        df_parties (pd.DataFrame)
        df_parties_analysis (pd.DataFrame)
    """
    df = df.copy()

    # Step 1: preprocess text
    df = main_discourse_preprocessing(df)

    # Step 2: count party mentions
    df_parties = party_mention_collect(df, PARTY_SYNONYM_DICT)

    # Step 3: aggregate weekly
    df_parties_analysis = party_counts_aggregation(
        df_parties, PARTIES, PUBLISHERS
    )

    return df_parties, df_parties_analysis

# ------------------------------
# Entry point (GitHub Actions)
# ------------------------------
def run_parties_analysis():
    """
    Run the full pipeline and write outputs to datasets/.
    """
    if not CLEAN_DATA_PATH.exists():
        raise FileNotFoundError("CLEAN_DATA.csv not found")

    df_clean = pd.read_csv(CLEAN_DATA_PATH)
    print(f"Loaded CLEAN_DATA.csv with {len(df_clean)} rows")

    df_parties, df_parties_analysis = main_parties(
        df_clean,
        PARTY_SYNONYM_DICT,
        PARTIES,
        PUBLISHERS
    )

    DATA_DIR.mkdir(exist_ok=True)

    df_parties.to_csv(PARTIES_DATA_PATH, index=False)
    df_parties_analysis.to_csv(PARTIES_ANALYSIS_PATH, index=False)

    print(f"Saved PARTIES_DATA.csv ({len(df_parties)} rows)")
    print(f"Saved PARTIES_ANALYSIS.csv ({len(df_parties_analysis)} rows)")

# ------------------------------
# Module execution
# ------------------------------
if __name__ == "__main__":
    run_parties_analysis()
