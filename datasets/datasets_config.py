"""
Dataset configuration

Defines file paths and dataset identifiers used across:
- crawling pipeline
- preprocessing
- party analysis
- dashboard
"""

from pathlib import Path

# Base directory = datasets folder
BASE_DATASET_PATH = Path(__file__).resolve().parent

# ---- Dataset paths ----
RAW_DATA_PATH = BASE_DATASET_PATH / "RAW_DATA.csv"
CLEAN_DATA_PATH = BASE_DATASET_PATH / "CLEAN_DATA.csv"
PARTIES_DATA_PATH = BASE_DATASET_PATH / "PARTIES_DATA.csv"
PARTIES_ANALYSIS_PATH = BASE_DATASET_PATH / "PARTIES_ANALYSIS.csv"

