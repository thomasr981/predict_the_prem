import os
from pathlib import Path
from typing import Any, Dict, List, Optional

import pandas as pd
import requests

BASE_URL = "https://fantasy.premierleague.com/api/"
DATA_DIRECTORY_PATH = Path(__file__).parent

STATS_COLS = [
    "home_team_goals_scored_stats",
    "away_team_goals_scored_stats",
    "home_team_own_goals_stats",
    "away_team_own_goals_stats",
]


def get_players_df() -> pd.DataFrame:
    renaming_dict = {
        "code": "global_player_id",
        "id": "player_id",
        "web_name": "player_name",
    }
    bootstrap_url = os.path.join(BASE_URL, "bootstrap-static/")
    bootstrap_response = requests.get(bootstrap_url)
    players_df = pd.DataFrame(bootstrap_response.json()["elements"])
    return players_df.rename(columns=renaming_dict)[list(renaming_dict.values())]


def get_fixtures_df(players_df: Optional[pd.DataFrame] = None) -> pd.DataFrame:
    player_mapping_dict = (
        {}
        if players_df is None
        else players_df[["player_id", "player_name"]]
        .set_index("player_id")
        .to_dict()["player_name"]
    )
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
    fixtures_df["match_score"] = (
        fixtures_df["home_team_score"].astype(float).fillna(0).astype(int).astype(str)
        + " - "
        + fixtures_df["away_team_score"].astype(float).fillna(0).astype(int).astype(str)
    )
    stats_df = pd.DataFrame.from_records(
        fixtures_df["stats"].apply(_expand_stats)
    ).reindex(labels=STATS_COLS, axis=1)
    stats_df[
        [
            "home_team_goals_scored_stats",
            "away_team_goals_scored_stats",
            "home_team_own_goals_stats",
            "away_team_own_goals_stats",
        ]
    ] = stats_df[
        [
            "home_team_goals_scored_stats",
            "away_team_goals_scored_stats",
            "home_team_own_goals_stats",
            "away_team_own_goals_stats",
        ]
    ].map(
        _map_player_in_stat, player_mapping_dict=player_mapping_dict
    )
    fixtures_df = pd.concat([fixtures_df, stats_df], axis=1)
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


def _expand_stats(stats: str):
    stats = pd.DataFrame.from_records(stats)
    row_data = {}
    for idx, row in stats.iterrows():
        identifier = row["identifier"]
        if identifier in ["goals_scored", "own_goals"]:
            row_data[f"home_team_{identifier}_stats"] = row.get("h", [])
            row_data[f"away_team_{identifier}_stats"] = row.get("a", [])
    for col in STATS_COLS:
        row_data[col] = row_data.get(col, [])
    return row_data


def _map_player_in_stat(
    stat: List[Dict[str, Any]], player_mapping_dict: Dict[int, str]
):
    stat = [
        x
        if not x.get("element")
        else {**x, **{"player_name": player_mapping_dict.get(x.get("element"))}}
        for x in stat
    ]
    return stat
