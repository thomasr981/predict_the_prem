def create_game_week_title_html(game_week: int, min_date: str, max_date: str):
    diplay_dates = (
        min_date if min_date == max_date else " - ".join((min_date, max_date))
    )
    return f"""<div style="text-align: center; font-family: Arial, sans-serif;">
    <div style="font-weight: bold; font-size: 24px; color: #37003c;">Game Week {game_week}</div>
    <div style="font-size: 18px; color: #b9a4ba;">{diplay_dates}/div>
    </div>
    """
