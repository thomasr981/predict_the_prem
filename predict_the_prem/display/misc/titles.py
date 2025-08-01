def create_fixture_table_title_html(game_week: int, min_date: str, max_date: str):
    diplay_dates = (
        min_date if min_date == max_date else " - ".join((min_date, max_date))
    )
    return f"""<div style="text-align: center; font-family: Arial, sans-serif; margin-right: 20px;">
    <div style="font-weight: bold; font-size: 16px; color: #37003c;">Game Week {game_week}</div>
    <div style="font-weight: light; font-size: 14px; color: #7e5981;">{diplay_dates}</div>
    </div>
    """
