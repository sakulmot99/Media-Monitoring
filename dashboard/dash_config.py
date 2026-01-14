# dashboard/dash_config.py

import pandas as pd

# ----------------------------
# Color Coding
# ----------------------------
COLOR_CODING = {
    "CDU/CSU": "black",
    "SPD": "red",
    "Grüne": "green",
    "FDP": "yellow",
    "AfD": "blue",
    "Die Linke": "purple",
}

# ----------------------------
# Visualization start date
# ----------------------------
VIS_START_DATE_TALKS = pd.to_datetime("2017-09-01")  # for talkshows
VIS_START_DATE_ONLINE = pd.to_datetime("2025-08-01")  # for online news


# ----------------------------
# Election result DataFrame
# ----------------------------
DF_ELECTION = pd.DataFrame({
    "party": ["CDU/CSU", "SPD", "Grüne", "FDP", "AfD", "Die Linke"],
    "election_date": ["2025-02-01"] * 6,
    "bundestag_share": [0.33, 0.19, 0.13, 0.00, 0.24, 0.10],
})

# ----------------------------
# Font / Style Settings
# ----------------------------
FONT_FAMILY = "Segoe UI, sans-serif"   # global font
TEXT_COLOR = "#333333"              # default text color

#-----------------------------
# Time Aggregation per Dataset
#-----------------------------

TIME_AGGREGATION = {
    "news": {
        "freq": "W-MON",
        "label": "Week", # Weekly
        "date_format": "%Y-%m-%d",
        "rolling_window": 3,      
        "rolling_label": "3-week rolling average"
    },
    "talkshows": {
        "freq": "MS",
        "label": "Month", # Monthly
        "date_format": "%Y-%m",
        "rolling_window": 5,      # 3-month rolling average
        "rolling_label": "5-month rolling average"
    }
}

