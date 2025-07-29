import pandas as pd

from predict_the_prem.constants import TEAM_BADGES
from predict_the_prem.javascripts import SORT_TABLE_BY_COLUMN_JAVASCRIPT


def create_league_table_html(league_table_df: pd.DataFrame) -> str:
    league_table_df = league_table_df.sort_values(by=["position"], ascending=[True])
    team_records = league_table_df.to_dict(orient="records")
    html = ""
    html += """
    <style>
    table {
        width: auto;
        border-collapse: collapse;
        font-family: Arial, sans-serif;
    }

    th {
        cursor: pointer;
        font-size: 16px;
        background-color: #f9f9f9;
        position: relative;
        user-select: none;
        transition: background-color 0.3s ease;
    }

    th:hover {
        background-color: #f1f1f1;
    }

    td {
        font-size: 16px;
        background-color: #ffffff;
    }

    tr:hover td {
        background-color: #f5f5f5 !important;
    }

    th.col-general,
    td.col-general {
        width: 30px;
        border: 1px solid black;
    }

    th.col-badge,
    td.col-badge {
        width: 40px;
        border-left: 1px solid black;
        border-top: 1px solid black;
        border-bottom: 1px solid black;
    }

    th.col-name,
    td.col-name {
        width: 100px;
        border-right: 1px solid black;
        border-top: 1px solid black;
        border-bottom: 1px solid black;
    }

    th.col-form,
    td.col-form {
        width: 80px;
        border: 1px solid black;
    }

    </style>
    """
    html += SORT_TABLE_BY_COLUMN_JAVASCRIPT
    html += """
    <table id="leagueTable">
        <thead>
            <tr>
                <th onclick="sortTableByColumn('leagueTable', 0)" class="col-general" style="text-align: center">Pos</th>
                <th onclick="sortTableByColumn('leagueTable', 2)" class="col-badge"  style="text-align: center">Club</th>
                <th onclick="sortTableByColumn('leagueTable', 2)" class="col-name"></th>
                <th onclick="sortTableByColumn('leagueTable', 3)" class="col-general" style="text-align: center">MP</th>
                <th onclick="sortTableByColumn('leagueTable', 4)" class="col-general" style="text-align: center">W</th>
                <th onclick="sortTableByColumn('leagueTable', 5)" class="col-general" style="text-align: center">D</th>
                <th onclick="sortTableByColumn('leagueTable', 6)" class="col-general" style="text-align: center">L</th>
                <th onclick="sortTableByColumn('leagueTable', 7)" class="col-general" style="text-align: center">GF</th>
                <th onclick="sortTableByColumn('leagueTable', 8)" class="col-general" style="text-align: center">GA</th>
                <th onclick="sortTableByColumn('leagueTable', 9)" class="col-general" style="text-align: center">GD</th>
                <th onclick="sortTableByColumn('leagueTable', 10)" class="col-general" style="text-align: center">Pts</th>
                <th onclick="sortTableByColumn('leagueTable', 11)" class="col-form" style="text-align: center">Form</th>
            <tr>
        </thead>
        <tbody>
    """
    for team in team_records:
        html += f"""
            <tr>
                <td class="col-general" style="text-align: center">{int(team['position'])}</td>
                <td class="col-badge" style="text-align: center"><img src="{TEAM_BADGES[team['team_name']]}" width="30px"></td>
                <td class="col-name" style="text-align: left">{team['team_name']}</td>
                <td class="col-general" style="text-align: center">{team['matches_played']}</td>
                <td class="col-general" style="text-align: center">{team['won']}</td>
                <td class="col-general" style="text-align: center">{team['drawn']}</td>
                <td class="col-general" style="text-align: center">{team['lost']}</td>
                <td class="col-general" style="text-align: center">{team['goals_for']}</td>
                <td class="col-general" style="text-align: center">{team['goals_against']}</td>
                <td class="col-general" style="text-align: center">{team['goal_difference']}</td>
                <td class="col-general" style="text-align: center">{int(team['points'])}</td>
                <td class="col-form" style="text-align: center">{team['form']}</td>
            </tr>
        """
    html += """
        </tbody>
    </table>
    """
    return html
