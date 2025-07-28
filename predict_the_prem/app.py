from ui import login_ui, meta_ui
from shiny import App, ui, reactive, render

app_ui = ui.page_fluid(
    ui.output_ui("login_page"),
    ui.output_ui("main_content"),
    title="Predict The Prem 2025/26",
)

def server(input, output, session):
    logged_in = reactive.Value(False)
    login_message_text = reactive.Value("")

    @output
    @render.ui
    def login_page():
        if not logged_in():
            return login_ui
        else:
            ui.div()

    @output
    @render.ui
    def main_content():
        if logged_in():
            return meta_ui
        else:
            return ui.div()
        
    @output
    @render.text
    def login_message():
        return login_message_text()


    @reactive.Effect
    @reactive.event(input.login_button)
    def check_login():
        if input.username() == "username" and input.password() == "password":
            logged_in.set(True)
            login_message_text.set("")
        else:
            login_message_text.set("Invalid username or password.")

    @reactive.Effect
    @reactive.event(input.logout_button)
    def logout():
        logged_in.set(False)
        login_message_text.set("You have been logged out.")

    
app = App(ui=app_ui, server=server)