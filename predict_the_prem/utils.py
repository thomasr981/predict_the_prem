import pandas as pd


def get_current_game_week(fixtures_df: pd.DataFrame) -> int:
    remaining_fixtures_df = fixtures_df[
        fixtures_df["match_start_time"]
        >= pd.Timestamp.now(tz="Europe/London").strftime("%Y-%m-%d")
    ].copy()
    if remaining_fixtures_df.empty:
        return int(fixtures_df["game_week"].max())
    return int(remaining_fixtures_df["game_week"].min())
