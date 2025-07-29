from typing import Literal

import pandas as pd


def get_league_table_df(
    team_fixtures_df: pd.DataFrame,
    started_or_finished: Literal["started", "finished"] = "started",
) -> pd.DataFrame:
    team_fixtures_df = team_fixtures_df.sort_values(
        by=["match_id", "home_away"], ascending=[True, False], ignore_index=True
    )
    league_table_df = team_fixtures_df.groupby(by=["team_name"], as_index=False).agg(
        matches_played=(f"is_{started_or_finished}", "sum"),
        won=("result", lambda x: sum(x == "W")),
        drawn=("result", lambda x: sum(x == "D")),
        lost=("result", lambda x: sum(x == "L")),
        points=("points", "sum"),
        goals_for=("goals_for", "sum"),
        goals_against=("goals_against", "sum"),
        form=(
            "result",
            lambda x: x[team_fixtures_df[f"is_{started_or_finished}"]].tail(5).tolist(),
        ),
    )
    league_table_df["goal_difference"] = (
        league_table_df["goals_for"] - league_table_df["goals_against"]
    )
    league_table_df = league_table_df.sort_values(
        by=["points", "goal_difference", "goals_for"],
        ascending=False,
        ignore_index=True,
    )
    league_table_df["position"] = range(1, 21)
    return league_table_df
