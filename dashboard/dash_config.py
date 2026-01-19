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
        "rolling_window": 2,      
        "rolling_label": "2-week rolling average"
    },
    "talkshows": {
        "freq": "MS",
        "label": "Month", # Monthly
        "date_format": "%Y-%m",
        "rolling_window": 5,      # 3-month rolling average
        "rolling_label": "5-month rolling average"
    }
}


#--------------------------------
# Respective descriptions per news and talkshow graph options
#--------------------------------
TEXT_CONFIG = {
    "news": {
        "total_title": "Total Political Party Mentions in German Online News",
        "total_description": (
            "Explore how often political parties have been mentioned in Germany’s major online newspapers "
            "since January 2026 (Der Spiegel, Die Zeit, Die FAZ, Süddeutsche Zeitung, and Die Bild)."
        ),
        "evolution_title": "Evolution of Political Party Coverage in Online News Over Time",
        "evolution_description": (
            "Track how media coverage of political parties has evolved over time in online news. "
            "Use the controls to view absolute counts or percentages and filter by party or publisher."
        )
    },
    "talkshows": {
        "total_title": "Total Political Party Mentions in German Talkshows",
        "total_description": (
            "Explore mentions of political parties in German talkshows from 2017 to 2025."
        ),
        "evolution_title": "Evolution of Political Party Coverage in Talkshows Over Time",
        "evolution_description": (
            "Explore how often political parties have been mentioned in talk show discourse between 2017 and 2025. "
            "Use the controls to view absolute counts or percentages and filter by party or show."
        )
    }
}



