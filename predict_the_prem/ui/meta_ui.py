from shiny import ui

from .league_overview import league_overview_ui

meta_ui = ui.page_fluid(
    ui.navset_pill(
        league_overview_ui,
        selected="League Overview",
    ),
    ui.input_action_button("logout_button", "Log Out"),
)
