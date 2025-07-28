from shiny import ui

login_ui = ui.page_fluid(
    ui.h2("Login"),
    ui.input_text("username", "Username"),
    ui.input_password("password", "Password"),
    ui.input_action_button("login_button", "Log In"),
    ui.output_text_verbatim("login_message"),
)