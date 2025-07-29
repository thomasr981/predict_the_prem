import pandas as pd

from .league_table import get_league_table_df


def get_team_position_vs_game_week(team_fixtures_df: pd.DataFrame) -> pd.DataFrame:
    team_position_vs_game_week_df = []
    for game_week in range(1, 39):
        week_league_table_df = get_league_table_df(
            team_fixtures_df=team_fixtures_df[
                team_fixtures_df["game_week"] <= game_week
            ].copy()
        )
        week_league_table_df = week_league_table_df.set_index("team_name")[
            ["position"]
        ].rename(columns={"position": f"game_week_{game_week}"})
        team_position_vs_game_week_df.append(week_league_table_df)
    team_position_vs_game_week_df = pd.concat(team_position_vs_game_week_df, axis=1)
    return team_position_vs_game_week_df
