from shiny import ui

from .fixtures_and_results_ui import fixtures_and_resuts_ui
from .league_overview_ui import league_overview_ui

meta_ui = ui.page_fluid(
    ui.navset_pill(
        league_overview_ui,
        fixtures_and_resuts_ui,
        selected="League Overview",
    ),
    ui.input_action_button("logout_button", "Log Out"),
)
