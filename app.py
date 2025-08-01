import pandas as pd
from shiny import App, reactive, render, ui
from shinywidgets import render_plotly

from predict_the_prem.data.data_loading import get_fixtures_df, get_teams_df
from predict_the_prem.display.misc import create_fixture_table_title_html
from predict_the_prem.display.plotting import plot_team_position_vs_game_week
from predict_the_prem.display.tables import (
    create_fixture_table_html,
    create_league_table_html,
)
from predict_the_prem.munge import (
    get_league_table_df,
    get_team_fixtures_df,
    get_team_position_vs_game_week,
    merge_fixtures_and_teams,
)
from predict_the_prem.ui import login_ui, meta_ui
from predict_the_prem.utils import get_current_game_week

app_ui = ui.page_fluid(
    ui.output_ui("login_page"),
    ui.output_ui("main_content"),
    title="Predict The Prem 2025/26",
)


def server(input, output, session):
    logged_in = reactive.Value(True)
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

    min_game_week = fixtures_df["game_week"].min()
    max_game_week = fixtures_df["game_week"].max()
    fixtures_and_results_game_week = reactive.Value(
        get_current_game_week(fixtures_df=fixtures_df)
    )

    @reactive.Effect
    def game_week_buttons():
        ui.update_action_button(
            "prev_game_week_button",
            disabled=fixtures_and_results_game_week() == min_game_week,
        )
        ui.update_action_button(
            "next_game_week_button",
            disabled=fixtures_and_results_game_week() == max_game_week,
        )

    @reactive.Effect
    @reactive.event(input.prev_game_week_button, ignore_init=True)
    def prev_game_week_button_click():
        if fixtures_and_results_game_week() > min_game_week:
            fixtures_and_results_game_week.set(fixtures_and_results_game_week() - 1)

    @reactive.Effect
    @reactive.event(input.next_game_week_button, ignore_init=True)
    def next_game_week_button_click():
        if fixtures_and_results_game_week() < max_game_week:
            fixtures_and_results_game_week.set(fixtures_and_results_game_week() + 1)

    @output
    @render.ui
    def fixtures_and_results_table_title():
        min_game_week_date = pd.to_datetime(
            fixtures_df[fixtures_df["game_week"] == fixtures_and_results_game_week()][
                "match_start_date"
            ].min()
        ).strftime("%a %d %b")
        max_game_week_date = pd.to_datetime(
            fixtures_df[fixtures_df["game_week"] == fixtures_and_results_game_week()][
                "match_start_date"
            ].max()
        ).strftime("%a %d %b")
        return ui.HTML(
            create_fixture_table_title_html(
                game_week=fixtures_and_results_game_week(),
                min_date=min_game_week_date,
                max_date=max_game_week_date,
            )
        )

    @output
    @render.ui
    def fixtures_and_results_table():
        return ui.HTML(
            create_fixture_table_html(
                fixtures_df=fixtures_df, game_week=fixtures_and_results_game_week()
            )
        )


app = App(ui=app_ui, server=server)
