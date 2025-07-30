import pandas as pd


def create_fixture_table_html(fixtures_df: pd.DataFrame, game_week: int) -> str:
    game_week_fixtures = fixtures_df[fixtures_df["game_week"] == game_week].copy()
    game_week_fixtures_records = {
        pd.to_datetime(date).strftime("%a %d %b"): group.to_dict(orient="records")
        for date, group in game_week_fixtures.groupby("match_start_date")
    }
    html = ""
    html += """
    <style>
    table {
        width: auto;
        border-collapse: collapse;
        font-family: Arial, sans-serif;
    }

    td {
        font-size: 16px;
        color: #37003c;
        background-color: #ffffff;
    }

    tr:hover td {
        background-color: #f5f5f5 !important;
    }

    td.fixture-and-results-table-col-date {
        width: 300px;
        font-size: 20px;
        font-weight: bold;
    }

    td.fixture-and-results-table-col-name {
        width: 150px;
    }

    td.fixture-and-results-table-col-badge {
        width: 30px;
    }

    td.fixture-and-results-table-col-time {
        width: 60px;
        font-size: 18px;
        font-weight: bold;
    }

    </style>
    """
    html += """
    <table id="fixtureTable">
        <tbody>
    """
    for date, fixtures in game_week_fixtures_records.items():
        html += f"""
            <tr>
                <td class="fixture-and-results-table-col-date" style="text-align: left">{date}</td>
                <td class="fixture-and-results-table-col-name"></td>
                <td class="fixture-and-results-table-col-badge"></td>
                <td class="fixture-and-results-table-col-time"></td>
                <td class="fixture-and-results-table-col-badge"></td>
                <td class="fixture-and-results-table-col-name"></td>
                <td class="fixture-and-results-table-col-date"></td>
            </tr>
        """
        for fixture in fixtures:
            html += f"""
                <tr>
                    <td class="fixture-and-results-table-col-date"></td>
                    <td class="fixture-and-results-table-col-name" style="text-align: right">{fixture['home_team_name']}</td>
                    <td class="fixture-and-results-table-col-badge"><img src="{fixture['home_team_badge']}" width="30px"></td>
                    <td class="fixture-and-results-table-col-time" style="text-align: center">{fixture['match_start_time_short']}</td>
                    <td class="fixture-and-results-table-col-badge"><img src="{fixture['away_team_badge']}" width="30px"></td>
                    <td class="fixture-and-results-table-col-name" style="text-align: left">{fixture['away_team_name']}</td>
                    <td class="fixture-and-results-table-col-date"></td>
                </tr>
            """
    html += """
        </tbody>
    </table>
    """
    return html
