from typing import Dict

import pandas as pd

from .league_table import get_league_table_df


def get_entries_position_df(
    teams_df: pd.DataFrame, entries: Dict[str, pd.DataFrame]
) -> pd.DataFrame:
    entries_position_df = teams_df[["team_id", "team_name", "team_short_name"]].copy()
    for entry_name, entry_df in entries.items():
        entry_to_merge = (
            entry_df[["Team", "Position"]]
            .rename(columns={"Team": "team_name", "Position": entry_name})
            .copy()
        )
        entries_position_df = entries_position_df.merge(
            entry_to_merge, how="left", on=["team_name"]
        )
    entries_position_df = (
        entries_position_df.set_index(["team_id", "team_name", "team_short_name"])
        .sort_index(axis="columns")
        .reset_index()
    )
    return entries_position_df


def get_entry_score_vs_game_week(
    team_fixtures_df: pd.DataFrame, entries_position_df: pd.DataFrame
) -> pd.DataFrame:
    prediction_cols = entries_position_df.columns[3:]
    entry_score_vs_game_week_df = pd.DataFrame({"entry_name": prediction_cols})

    max_game_week = team_fixtures_df["game_week"].max()
    for game_week in range(1, max_game_week + 1):
        game_week_league_table_df = get_league_table_df(
            team_fixtures_df=team_fixtures_df[
                team_fixtures_df["game_week"] <= game_week
            ].copy(),
            started_or_finished="started",
        )
        if game_week_league_table_df["matches_played"].max() < game_week:
            break  # This game week not started yet so break out of loop

        game_week_league_table_df = game_week_league_table_df[
            ["team_name", "position"]
        ].merge(entries_position_df, how="left", on="team_name")
        stacked_game_week_pos_and_pred_df = game_week_league_table_df.melt(
            id_vars=["team_name", "position"],
            value_vars=prediction_cols,
            var_name="entry_name",
            value_name="prediction",
        )
        stacked_game_week_pos_and_pred_df[f"GW{game_week}"] = abs(
            stacked_game_week_pos_and_pred_df["position"]
            - stacked_game_week_pos_and_pred_df["prediction"]
        )
        stacked_game_week_pos_and_pred_df = stacked_game_week_pos_and_pred_df.groupby(
            by=["entry_name"], as_index=False
        )[f"GW{game_week}"].sum()
        entry_score_vs_game_week_df = entry_score_vs_game_week_df.merge(
            stacked_game_week_pos_and_pred_df, how="left", on=["entry_name"]
        )
    return entry_score_vs_game_week_df.sort_values(
        by=entry_score_vs_game_week_df.columns[-1]
    )
