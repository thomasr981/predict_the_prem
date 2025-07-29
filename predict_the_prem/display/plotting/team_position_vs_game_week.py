import pandas as pd
import plotly.graph_objects as go

from predict_the_prem.constants import TEAM_BADGES, TEAM_COLOURS


def plot_team_position_vs_game_week(
    team_position_vs_game_week_df: pd.DataFrame,
) -> go.Figure:
    fig = go.Figure()

    teams = sorted(team_position_vs_game_week_df.index)
    columns = [
        col.replace("game_week_", "GW") for col in team_position_vs_game_week_df.columns
    ]
    n_teams = len(teams)
    n_columns = len(columns)

    # Pre-calculate x-axis range with margin
    x_start = -0.025 * n_columns
    x_end = n_columns - (1 - 0.025 * n_columns)
    x_range = [x_start, x_end]

    # Add traces and badges
    for team in teams:
        y_values = team_position_vs_game_week_df.T[team]
        final_game_week = columns[-1]
        final_position = y_values.iloc[-1]

        fig.add_trace(
            go.Scatter(
                x=columns,
                y=y_values,
                line=dict(color=TEAM_COLOURS[team]),
                name=team,
                mode="lines",
            )
        )

        fig.add_layout_image(
            dict(
                source=TEAM_BADGES[team],
                x=final_game_week,
                y=final_position,
                xref="x",
                yref="y",
                sizex=1.25,
                sizey=1.25,
                xanchor="center",
                yanchor="middle",
            )
        )

    # Vertical grid lines
    vertical_lines = [
        dict(
            type="line",
            x0=i + 0.5,
            x1=i + 0.5,
            y0=0,
            y1=n_teams + 1,
            line=dict(color="LightGrey", width=1),
        )
        for i in range(n_columns - 1)
    ]

    # Horizontal grid lines for positions 1 through 20
    horizontal_lines = [
        dict(
            type="line",
            x0=x_start,
            x1=x_end,
            y0=j + 0.5,
            y1=j + 0.5,
            line=dict(color="LightGrey", width=1),
        )
        for j in range(1, 20)
    ]

    shapes = vertical_lines + horizontal_lines

    fig.update_layout(
        title=dict(
            text="Team Position Over Game Weeks",
            y=0.99,
            x=0.5,
            xanchor="center",
            yanchor="top",
            font=dict(size=20, color="black", family="Arial"),
        ),
        xaxis_title=dict(
            text="Game Week",
            font=dict(size=16, color="black", family="Arial"),
        ),
        yaxis_title=dict(
            text="Position",
            font=dict(size=16, color="black", family="Arial"),
        ),
        xaxis=dict(range=x_range),
        yaxis=dict(
            autorange="reversed",
            tickmode="array",
            tickvals=list(range(1, 21)),
            showgrid=False,
        ),
        shapes=shapes,
        legend_title="Teams",
    )

    return fig
