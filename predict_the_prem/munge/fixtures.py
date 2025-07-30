import numpy as np
import pandas as pd

from predict_the_prem.constants import TEAM_BADGES


def merge_fixtures_and_teams(
    fixtures_df: pd.DataFrame, teams_df: pd.DataFrame
) -> pd.DataFrame:
    for home_away in ["home", "away"]:
        renaming_dict = {
            "team_id": f"{home_away}_team_id",
            "team_short_name": f"{home_away}_team_short_name",
            "team_name": f"{home_away}_team_name",
        }
        home_away_teams_df = teams_df.rename(columns=renaming_dict)[
            list(renaming_dict.values())
        ].copy()
        fixtures_df = fixtures_df.merge(
            home_away_teams_df, how="left", on=[f"{home_away}_team_id"]
        )
    fixtures_df["home_team_badge"] = fixtures_df["home_team_name"].map(TEAM_BADGES)
    fixtures_df["away_team_badge"] = fixtures_df["away_team_name"].map(TEAM_BADGES)
    return fixtures_df


def get_team_fixtures_df(fixtures_df: pd.DataFrame) -> pd.DataFrame:
    team_fixtures_dfs = []
    for home_away, away_home in [("home", "away"), ("away", "home")]:
        team_fixtures_df = (
            fixtures_df[
                [
                    "match_id",
                    "game_week",
                    "is_finished",
                    "is_started",
                    "match_start_time",
                    f"{home_away}_team_id",
                    f"{home_away}_team_name",
                    f"{home_away}_team_short_name",
                    f"{home_away}_team_score",
                    f"{away_home}_team_score",
                ]
            ]
            .rename(
                columns={
                    f"{home_away}_team_id": "team_id",
                    f"{home_away}_team_name": "team_name",
                    f"{home_away}_team_short_name": "team_short_name",
                    f"{home_away}_team_score": "goals_for",
                    f"{away_home}_team_score": "goals_against",
                }
            )
            .copy()
        )
        team_fixtures_df["home_away"] = home_away
        condlist = [
            team_fixtures_df["goals_for"] > team_fixtures_df["goals_against"],
            team_fixtures_df["goals_for"] == team_fixtures_df["goals_against"],
            team_fixtures_df["goals_for"] < team_fixtures_df["goals_against"],
        ]
        team_fixtures_df["result"] = np.select(
            condlist=condlist,
            choicelist=["W", "D", "L"],
            default=None,
        )
        team_fixtures_df["points"] = np.select(
            condlist=condlist,
            choicelist=[3, 1, 0],
            default=np.nan,
        )
        team_fixtures_dfs.append(team_fixtures_df)
    return pd.concat(team_fixtures_dfs).sort_values(
        by=["match_id", "home_away"], ascending=[True, False], ignore_index=True
    )
