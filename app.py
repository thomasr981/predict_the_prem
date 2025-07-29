from shiny import App, reactive, render, ui
from shinywidgets import render_plotly

from predict_the_prem.data.data_loading import get_fixtures_df, get_teams_df
from predict_the_prem.display.plotting.league_table import create_league_table_html
from predict_the_prem.display.plotting.team_position_vs_game_week import (
    plot_team_position_vs_game_week,
)
from predict_the_prem.munge import (
    get_league_table_df,
    get_team_fixtures_df,
    get_team_position_vs_game_week,
    merge_fixtures_and_teams,
)
from predict_the_prem.ui import login_ui, meta_ui

app_ui = ui.page_fluid(
    ui.output_ui("login_page"),
    ui.output_ui("main_content"),
    title="Predict The Prem 2025/26",
)


def server(input, output, session):
    logged_in = reactive.Value(False)
    login_message_text = reactive.Value("")

    fixtures_df = get_fixtures_df()
    teams_df = get_teams_df()

    fixtures_df = merge_fixtures_and_teams(fixtures_df=fixtures_df, teams_df=teams_df)
    team_fixtures_df = get_team_fixtures_df(fixtures_df=fixtures_df)
    league_table_df = get_league_table_df(
        team_fixtures_df=team_fixtures_df, started_or_finished="started"
    )

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

    @output
    @render.ui
    def league_table():
        return ui.HTML(create_league_table_html(league_table_df=league_table_df))

    @output
    @render_plotly
    def team_position_vs_game_week_plot():
        team_position_vs_game_week_df = get_team_position_vs_game_week(
            team_fixtures_df=team_fixtures_df
        )
        return plot_team_position_vs_game_week(
            team_position_vs_game_week_df=team_position_vs_game_week_df
        )


app = App(ui=app_ui, server=server)
