from shiny import ui

meta_ui = ui.page_fluid(
    ui.input_action_button("logout_button", "Log Out")
)