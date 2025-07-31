from shiny import ui

from .fixtures_and_results_ui import fixtures_and_resuts_ui
from .league_overview_ui import league_overview_ui

meta_ui = ui.page_fluid(
    ui.tags.head(
        ui.tags.style(
            """
            .ptp-navset .nav-pills .nav-link {
                background-color: #f0e6f7;
                color: #4f1d52;
            }

            .ptp-navset .nav-pills .nav-link.active {
                background-color: #37003c !important;
                color: white !important;
            }

            .ptp-navset .nav-pills .nav-link:hover {
                background-color: #a07bb0;
                color: white;
            }
        """
        )
    ),
    ui.tags.div(
        ui.navset_pill(
            league_overview_ui,
            fixtures_and_resuts_ui,
            selected="League Overview",
        ),
        class_="ptp-navset",
    ),
    ui.input_action_button("logout_button", "Log Out"),
)
