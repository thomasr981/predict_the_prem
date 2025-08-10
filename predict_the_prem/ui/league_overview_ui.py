from shiny import ui
from shinywidgets import output_widget

league_overview_ui = ui.nav_panel(
    "League Overview",
    ui.div(
        ui.card(
            ui.card_header("League Table"),
            ui.card_body(ui.output_ui("league_table")),
            full_screen=True,
            style="width: 600px; margin-right: 10px; flex-shrink: 0;",
        ),
        ui.card(
            output_widget("team_position_vs_game_week_plot"),
            full_screen=True,
            style=("width: 1200px; " "height: 800px; " "flex-shrink: 0; "),
        ),
        style="display: flex; overflow-x: auto; width: 100%; margin-top: 20px;",
    ),
    ui.div(
        ui.card(
            ui.output_ui("player_top_10_goals_scored"),
            style="display: flex; flex-direction: column; align-items: center; width: 33%; min-width: 500px;",
        ),
        ui.card(
            ui.output_ui("player_top_10_assists"),
            style="display: flex; flex-direction: column; align-items: center; width: 33%; min-width: 500px;",
        ),
        ui.card(
            ui.output_ui("player_top_10_clean_sheets"),
            style="display: flex; flex-direction: column; align-items: center; width: 33%; min-width: 500px;",
        ),
        style="display: flex; justify-content: space-between; gap: 20px; margin-top: 20px; max-width: 1800px",
    ),
)
