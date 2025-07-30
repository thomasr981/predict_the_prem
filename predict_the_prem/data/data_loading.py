import os
from pathlib import Path
from typing import Dict

import pandas as pd
import requests

BASE_URL = "https://fantasy.premierleague.com/api/"
DATA_DIRECTORY_PATH = Path(__file__).parent


def get_fixtures_df() -> pd.DataFrame:
    renaming_dict = {
        "code": "global_match_id",
        "id": "match_id",
        "event": "game_week",
        "finished": "is_finished",
        "finished_provisional": "is_finished_provisional",
        "kickoff_time": "match_start_time",
        "provisional_start_time": "is_provisional_start_time",
        "started": "is_started",
        "team_h": "home_team_id",
        "team_a": "away_team_id",
        "team_h_score": "home_team_score",
        "team_a_score": "away_team_score",
        "minutes": "minutes_played",
        "stats": "stats",
        "team_h_difficulty": "home_team_difficulty",
        "team_a_difficulty": "away_team_difficulty",
        "pulse_id": "pulse_id",
    }
    fixtures_url = os.path.join(BASE_URL, "fixtures/")
    fixtures_response = requests.get(fixtures_url)
    fixtures_df = pd.DataFrame(fixtures_response.json())
    fixtures_df = fixtures_df.rename(columns=renaming_dict)[
        list(renaming_dict.values())
    ]
    fixtures_df["match_start_time"] = pd.to_datetime(fixtures_df["match_start_time"])
    fixtures_df["match_start_time"] = (
        fixtures_df["match_start_time"]
        .dt.tz_convert("Europe/London")
        .dt.tz_localize(None)
    )
    fixtures_df["match_start_date"] = fixtures_df["match_start_time"].dt.date
    fixtures_df["match_start_time_short"] = (
        fixtures_df["match_start_time"].dt.time.astype(str).str[:5]
    )
    return fixtures_df


def get_teams_df() -> pd.DataFrame:
    renaming_dict = {
        "code": "global_team_id",
        "id": "team_id",
        "name": "team_name",
        "short_name": "team_short_name",
        "position": "league_position",
        "strength": "team_strength",
        "strength_overall_home": "team_strength_overall_home",
        "strength_overall_away": "team_strength_overall_away",
        "strength_attack_home": "team_strength_attack_home",
        "strength_attack_away": "team_strength_attack_away",
        "strength_defence_home": "team_strength_defence_home",
        "strength_defence_away": "team_strength_defence_away",
        "pulse_id": "pulse_id",
    }
    bootstrap_url = os.path.join(BASE_URL, "bootstrap-static/")
    bootstrap_response = requests.get(bootstrap_url)
    teams_df = pd.DataFrame(bootstrap_response.json()["teams"])
    return teams_df.rename(columns=renaming_dict)[list(renaming_dict.values())]


def get_entries() -> Dict[str, pd.DataFrame]:
    directory = os.path.join(DATA_DIRECTORY_PATH, "entries/")
    entries = {}
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith(".csv"):
            new_entry_df = pd.read_csv(os.path.join(directory, filename))
            new_entry_name = "_".join(filename[:-4].split("_")[1:])
            entries[new_entry_name] = new_entry_df
    return dict(entries.items())
