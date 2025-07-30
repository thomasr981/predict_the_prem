from shiny import ui

from predict_the_prem.display.misc.buttons import (
    LEFT_ARROW_BUTTON_HTML,
    RIGHT_ARROW_BUTTON_HTML,
)

fixtures_and_resuts_ui = ui.nav_panel(
    "Fixtures & Results",
    ui.tags.head(
        ui.tags.style(
            """
            .circle-arrow-btn {
                background-color: #ebe5eb;
                color: white;
                border: none;
                border-radius: 50%;
                width: 50px;
                height: 50px;
                padding: 0;
                font-size: 24px;
                display: flex;
                align-items: center;
                justify-content: center;
                cursor: pointer;
                transition: background-color 0.3s ease;
            }

            .circle-arrow-btn:hover {
                background-color: #e5dee6;
            }

            .circle-arrow-btn svg {
                width: 28px;
                height: 28px;
                stroke: #4f1d52;
                stroke-width: 2;
                fill: none;
            }
        """
        )
    ),
    ui.card(
        ui.card_body(
            ui.tags.div(
                ui.input_action_button(
                    "prev_game_week_button",
                    ui.HTML(LEFT_ARROW_BUTTON_HTML),
                    class_="circle-arrow-btn",
                    style="margin-right: 20px;",
                ),
                ui.HTML(
                    """
                    <div style="text-align: center; font-family: Arial, sans-serif; margin-right: 20px;">
                    <div style="font-weight: bold; font-size: 24px; color: #37003c;">Matchweek 1</div>
                    <div style="font-size: 18px; color: #b9a4ba;">Fri 15 Aug - Mon 18 Aug</div>
                    </div>
                """
                ),
                ui.input_action_button(
                    "next_game_week_button",
                    ui.HTML(RIGHT_ARROW_BUTTON_HTML),
                    class_="circle-arrow-btn",
                ),
                style="display: flex; justify-content: center; align-items: center;",
            ),
            ui.output_ui("fixtures_and_results_table"),
        ),
        full_screen=True,
        style="min-width: 1000px; flex-shrink: 0; flex-grow: 1;",
    ),
)
