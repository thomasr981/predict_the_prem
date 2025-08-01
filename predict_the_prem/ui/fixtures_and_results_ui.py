from shiny import ui

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
                width: 40px;
                height: 40px;
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

            .circle-arrow-btn:disabled {
                background-color: #f4f1f4;
            }

            .circle-arrow-btn svg {
                width: 30px;
                height: 30px;
                stroke: #4f1d52;
                stroke-width: 1;
                fill: none;
            }

            .circle-arrow-btn:disabled svg {
                stroke: #987a99;
            }
        """
        )
    ),
    ui.card(
        ui.card_body(
            ui.tags.div(
                ui.input_action_button(
                    "prev_game_week_button",
                    ui.HTML(
                        """<svg viewBox="0 0 24 24"><polyline points="14,6 8,12 14,18" /></svg>"""
                    ),
                    class_="circle-arrow-btn",
                    style="margin-right: 20px;",
                    disabled=False,
                ),
                ui.output_ui("fixtures_and_results_table_title"),
                ui.input_action_button(
                    "next_game_week_button",
                    ui.HTML(
                        """<svg viewBox="0 0 24 24"><polyline points="10,6 16,12 10,18" /></svg>"""
                    ),
                    class_="circle-arrow-btn",
                    disabled=False,
                ),
                style="display: flex; justify-content: center; align-items: center;",
            ),
            ui.output_ui("fixtures_and_results_table"),
        ),
        full_screen=True,
        style="min-width: 600px; flex-shrink: 0; flex-grow: 1;",
    ),
)
