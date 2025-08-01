import pandas as pd


def get_current_game_week(fixtures_df: pd.DataFrame) -> int:
    return fixtures_df[
        fixtures_df["match_start_time"]
        >= pd.Timestamp.now(tz="Europe/London").strftime("%Y-%m-%d")
    ]["game_week"].min()
