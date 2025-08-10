from typing import Dict

import pandas as pd


def svg_football(color: str = "black") -> str:
    return f"""
    <svg width="18" height="18" viewBox="0 0 60 60"
         style="display:inline-block; vertical-align:bottom;  margin:0px;">
        <path fill="{color}" fill-opacity="1" stroke-width="0.2" stroke-linejoin="round"
        d="M 43.5,21.0285L 48.6842,25.394L 50.3689,24.9228C 48.4338,23.092 46.0926,21.6859 43.4946,20.854L 43.5,21.0285 Z
        M 53.6014,39.3315L 52.5714,45.5285L 53.8558,46.5275C 55.221,43.9944 55.9969,41.0968 56,38.0182L 53.6014,39.3315 Z
        M 43.8214,48.7596L 38.3871,44.894L 32.1728,47.2255L 30.6427,53.6725L 32.5593,55.1631C 34.2758,55.7068 36.1036,56 38,56C
        39.7036,56 41.3519,55.7633 42.9138,55.3211L 43.8214,48.7596 Z
        M 29.5413,53.4566L 31.0714,47.0096L 25.3871,42.644L 21.0897,44.182C 22.5587,48.1994 25.4186,51.5469 29.0863,53.6415L 29.5413,53.4566 Z
        M 25.5413,41.5626L 26.3214,34.1156L 21.5554,30.6696C 20.5557,32.9087 20,35.3894 20,38C 20,39.8384 20.2756,41.6124 20.7877,43.2829L 25.5413,41.5626 Z
        M 27.0056,33.644L 33.22,31.0625L 34.5,24.3656L 30.7276,21.5296C 26.8969,23.2235 23.768,26.2146 21.898,29.946L 27.0056,33.644 Z
        M 51.7199,45.2066L 52.7499,39.0096L 46.8157,34.394L 40.3514,36.7255L 39.3214,44.1725L 44.7556,48.038L 51.7199,45.2066 Z
        M 46.4699,33.4566L 47.4999,26.0096L 42.3157,21.6441L 35.3514,24.4755L 34.0714,31.1725L 40.0056,35.788L 46.4699,33.4566 Z
        M 38,18C 49.0457,18 58,26.9543 58,38C 58,49.0457 49.0457,58 38,58C 26.9543,58 18,49.0457 18,38C 18,26.9543 26.9543,18 38,18 Z" />
    </svg>
    """


def format_goals(goals_dict: Dict) -> str:
    if not goals_dict["black"] and not goals_dict["red"]:
        return "—"
    return "<br>".join(
        f"{player_goals['player_name']} {''.join(svg_football(ball_color) for _ in range(player_goals['value']))}"
        for ball_color, players_goals in goals_dict.items()
        for player_goals in players_goals
    )


def create_fixture_table_html(fixtures_df: pd.DataFrame, game_week: int) -> str:
    game_week_fixtures = fixtures_df[fixtures_df["game_week"] == game_week].copy()
    game_week_fixtures_records = {
        pd.to_datetime(date).strftime("%a %d %b"): group.to_dict(orient="records")
        for date, group in game_week_fixtures.groupby("match_start_date")
    }

    html = """
    <style>
    #fixtureTable {
        width: 100%;
        border-collapse: collapse;
        font-family: Helvetica, sans-serif;
        margin: auto; /* Center table horizontally */
    }
    #fixtureTable td {
        font-size: 12px;
        font-weight: 575;
        color: #37003c;
        background-color: #ffffff;
    }
    #fixtureTable tr:hover td {
        background-color: #f5f5f5 !important;
    }
    #fixtureTable td.fixture-and-results-table-col-date {
        width: 200px;
        font-size: 16px;
        font-weight: bold;
        text-align: left;
    }
    #fixtureTable td.fixture-and-results-table-col-name {
        width: 150px;
    }
    #fixtureTable td.fixture-and-results-table-col-badge {
        width: 24px;
    }
    #fixtureTable td.fixture-and-results-table-col-time {
        width: 50px;
        font-size: 16px;
        font-weight: bold;
        text-align: center;
    }
    #fixtureTable td.fixture-and-results-table-col-events {
        width: 150px;
        font-size: 10px;
    }

    #fixtureTable .goal-details-content {
        overflow: hidden;
        max-height: 0;
        transition: max-height 0.3s ease;
    }
    #fixtureTable .goal-details.open .goal-details-content {
        max-height: 50px; /* adjust for scorer row height */
    }
    #fixtureTable .toggle-row {
        cursor: pointer;
    }
    </style>
    <table id="fixtureTable">
        <tbody>
    """

    for date, fixtures in game_week_fixtures_records.items():
        # Date row - with original date class on the first and last td to match your original format
        html += f"""
            <tr>
                <td class="fixture-and-results-table-col-date" style="text-align: left;">{date}</td>
                <td class="fixture-and-results-table-col-name"></td>
                <td class="fixture-and-results-table-col-badge"></td>
                <td class="fixture-and-results-table-col-time"></td>
                <td class="fixture-and-results-table-col-badge"></td>
                <td class="fixture-and-results-table-col-name"></td>
                <td class="fixture-and-results-table-col-date"></td>
            </tr>
        """
        for fixture in fixtures:
            middle_col = (
                f"""<td class="fixture-and-results-table-col-time" style="text-align: center;">{fixture['match_score']}</td>"""
                if fixture["is_started"]
                else f"""<td class="fixture-and-results-table-col-time" style="text-align: center;">{fixture['match_start_time_short']}</td>"""
            )

            # Fixture row
            html += f"""
                <tr class="toggle-row" data-fixture-id="{fixture['match_id']}">
                    <td class="fixture-and-results-table-col-date"></td>
                    <td class="fixture-and-results-table-col-name" style="text-align: right;">{fixture['home_team_name']}</td>
                    <td class="fixture-and-results-table-col-badge" style="text-align: center;"><img src="{fixture['home_team_badge']}" width="24px"></td>
                    {middle_col}
                    <td class="fixture-and-results-table-col-badge" style="text-align: center;"><img src="{fixture['away_team_badge']}" width="24px"></td>
                    <td class="fixture-and-results-table-col-name" style="text-align: left;">{fixture['away_team_name']}</td>
                    <td class="fixture-and-results-table-col-date"></td>
                </tr>
            """

            # Goal scorers/details row
            if fixture["is_started"]:
                home_goals_dict = {
                    "black": fixture["home_team_goals_scored_stats"],
                    "red": fixture["away_team_own_goals_stats"],
                }
                away_goals_dict = {
                    "black": fixture["away_team_goals_scored_stats"],
                    "red": fixture["home_team_own_goals_stats"],
                }
                html += f"""
                    <tr class="goal-details" data-fixture-id="{fixture['match_id']}">
                        <td class="fixture-and-results-table-col-date"></td>
                        <td class="fixture-and-results-table-col-events" style="text-align: right;">
                            <div class="goal-details-content">{format_goals(home_goals_dict)}</div>
                        </td>
                        <td class="fixture-and-results-table-col-badge"></td>
                        <td class="fixture-and-results-table-col-time"></td>
                        <td class="fixture-and-results-table-col-badge"></td>
                        <td class="fixture-and-results-table-col-events" style="text-align: left;">
                            <div class="goal-details-content">{format_goals(away_goals_dict)}</div>
                        </td>
                        <td class="fixture-and-results-table-col-date"></td>
                    </tr>
                """

    html += """
        </tbody>
    </table>
    <script>
    document.querySelectorAll('.toggle-row').forEach(row => {
        row.addEventListener('click', () => {
            const fixtureId = row.getAttribute('data-fixture-id');
            const detailsRow = document.querySelector(`.goal-details[data-fixture-id="${fixtureId}"]`);

            // Close all other open details rows
            document.querySelectorAll('.goal-details.open').forEach(openRow => {
                if (openRow !== detailsRow) {
                    openRow.classList.remove('open');
                    openRow.querySelectorAll('.goal-details-content').forEach(content => {
                        content.style.maxHeight = '0';
                    });
                }
            });

            // Toggle the clicked details row
            if (detailsRow) {
                const isOpen = detailsRow.classList.contains('open');
                if (isOpen) {
                    detailsRow.classList.remove('open');
                    detailsRow.querySelectorAll('.goal-details-content').forEach(content => {
                        content.style.maxHeight = '0';
                    });
                } else {
                    detailsRow.classList.add('open');
                    detailsRow.querySelectorAll('.goal-details-content').forEach(content => {
                        content.style.maxHeight = content.scrollHeight + 'px';
                    });
                }
            }
        });
    });
    </script>
    """

    return html
