from typing import List, Literal, Union

import pandas as pd

from predict_the_prem.constants import TEAM_BADGES
from predict_the_prem.javascripts import SORT_TABLE_BY_COLUMN_JAVASCRIPT

WDL_SVG_DICT = {
    "regular": {
        "W": """<svg width="18" height="18" aria-hidden="true" viewBox="0 0 22 22" style="display: inline-block; vertical-align: center;  margin:0px;">  <path d="M11 3a8 8 0 1 1 0 16 8 8 0 0 1 0-16" fill="#34A853"></path> <path d="M9.2 12.28 7.12 10.2 6 11.32l3.2 3.2 6.4-6.4L14.48 7z" fill="#fff"></path>  </svg>""",
        "D": """<svg width="18" height="18" aria-hidden="true" viewBox="0 0 22 22" style="display: inline-block; vertical-align: center;  margin:0px;">  <path clip-rule="evenodd" d="M11 19a8 8 0 1 0 0-16 8 8 0 0 0 0 16" fill="#9D9BA7" fill-rule="evenodd"></path> <path clip-rule="evenodd" d="M8 10h6v2H8z" fill="#fff" fill-rule="evenodd"></path>  </svg>""",
        "L": """<svg width="18" height="18" aria-hidden="true" viewBox="0 0 22 22" style="display: inline-block; vertical-align: center;  margin:0px;">  <path clip-rule="evenodd" d="M11 19a8 8 0 1 0 0-16 8 8 0 0 0 0 16" fill="#EA4335" fill-rule="evenodd"></path> <path clip-rule="evenodd" d="M13.263 14.394 11 12.131l-2.263 2.263-1.131-1.131L9.869 11 7.606 8.737l1.131-1.131L11 9.869l2.263-2.263 1.131 1.131L12.131 11l2.263 2.263z" fill="#fff" fill-rule="evenodd"></path>  </svg>""",
    },
    "final": {
        "W": """<svg width="18" height="18" aria-hidden="true" viewBox="0 0 22 22" style="display: inline-block; vertical-align: center;  margin:0px;">  <path d="M11 0C4.925 0 0 4.925 0 11s4.925 11 11 11 11-4.925 11-11S17.075 0 11 0" fill="#34A853"></path> <path d="M11 2a9 9 0 1 0 0 18 9 9 0 0 0 0-18" fill="#fff"></path> <path d="M11 3a8 8 0 1 1 0 16 8 8 0 0 1 0-16" fill="#34A853"></path> <path d="M9.2 12.28 7.12 10.2 6 11.32l3.2 3.2 6.4-6.4L14.48 7z" fill="#fff"></path>  </svg>""",
        "D": """<svg width="18" height="18" aria-hidden="true" viewBox="0 0 22 22" style="display: inline-block; vertical-align: center;  margin:0px;">  <path d="M11 0C4.925 0 0 4.925 0 11s4.925 11 11 11 11-4.925 11-11S17.075 0 11 0" fill="#9D9BA7"></path> <path d="M11 2a9 9 0 1 0 0 18 9 9 0 0 0 0-18" fill="#fff"></path> <path clip-rule="evenodd" d="M11 19a8 8 0 1 0 0-16 8 8 0 0 0 0 16" fill="#9D9BA7" fill-rule="evenodd"></path> <path clip-rule="evenodd" d="M8 10h6v2H8z" fill="#fff" fill-rule="evenodd"></path>  </svg>""",
        "L": """<svg width="18" height="18" aria-hidden="true" viewBox="0 0 22 22" style="display: inline-block; vertical-align: center;  margin:0px;">  <path d="M11 0C4.925 0 0 4.925 0 11s4.925 11 11 11 11-4.925 11-11S17.075 0 11 0" fill="#EA4335"></path> <path d="M11 2a9 9 0 1 0 0 18 9 9 0 0 0 0-18" fill="#fff"></path> <path clip-rule="evenodd" d="M11 19a8 8 0 1 0 0-16 8 8 0 0 0 0 16" fill="#EA4335" fill-rule="evenodd"></path> <path clip-rule="evenodd" d="M13.263 14.394 11 12.131l-2.263 2.263-1.131-1.131L9.869 11 7.606 8.737l1.131-1.131L11 9.869l2.263-2.263 1.131 1.131L12.131 11l2.263 2.263z" fill="#fff" fill-rule="evenodd"></path>  </svg>""",
    },
}


def map_form_to_svg(
    form: Union[List[str], str], dict_to_use: Literal["regular", "final"] = "regular"
) -> Union[List[str], str]:
    if isinstance(form, str):
        return WDL_SVG_DICT[dict_to_use][form]
    return [WDL_SVG_DICT[dict_to_use][form_] for form_ in form]


def get_form_svg(form: List[str]) -> str:
    return "".join(
        map_form_to_svg(form[:-1], "regular") + map_form_to_svg(form[-1:], "final")
    )


def create_league_table_html(league_table_df: pd.DataFrame) -> str:
    league_table_df = league_table_df.sort_values(by=["position"], ascending=[True])
    team_records = league_table_df.to_dict(orient="records")
    html = ""
    html += """
    <style>
    #leagueTable {
        width: auto;
        border-collapse: collapse;
        font-family: Helvetica, sans-serif;
    }

    #leagueTable th {
        cursor: pointer;
        font-size: 16px;
        background-color: #f9f9f9;
        color: #37003c;
        position: relative;
        user-select: none;
        transition: background-color 0.3s ease;
    }

    #leagueTable th:hover {
        background-color: #f1f1f1;
    }

    #leagueTable td {
        font-size: 14px;
        background-color: #ffffff;
        color: #37003c;
    }

    #leagueTable tr:hover td {
        background-color: #f5f5f5 !important;
    }

    #leagueTable th.league-table-col-general,
    #leagueTable td.league-table-col-general {
        width: 30px;
        border-top: 1px solid black;
        border-bottom: 1px solid black;
    }

    #leagueTable th.league-table-col-badge,
    #leagueTable td.league-table-col-badge {
        width: 40px;
        border-top: 1px solid black;
        border-bottom: 1px solid black;
    }

    #leagueTable th.league-table-col-name,
    #leagueTable td.league-table-col-name {
        width: 100px;
        border-top: 1px solid black;
        border-bottom: 1px solid black;
    }

    #leagueTable th.league-table-col-form,
    #leagueTable td.league-table-col-form {
        width: 90px;
        border-top: 1px solid black;
        border-bottom: 1px solid black;
    }

    </style>
    """
    html += SORT_TABLE_BY_COLUMN_JAVASCRIPT
    html += """
    <table id="leagueTable">
        <thead>
            <tr>
                <th onclick="sortTableByColumn('leagueTable', 0)" class="league-table-col-general" style="text-align: center">Pos</th>
                <th onclick="sortTableByColumn('leagueTable', 2)" class="league-table-col-badge"  style="text-align: center">Club</th>
                <th onclick="sortTableByColumn('leagueTable', 2)" class="league-table-col-name"></th>
                <th onclick="sortTableByColumn('leagueTable', 3)" class="league-table-col-general" style="text-align: center">MP</th>
                <th onclick="sortTableByColumn('leagueTable', 4)" class="league-table-col-general" style="text-align: center">W</th>
                <th onclick="sortTableByColumn('leagueTable', 5)" class="league-table-col-general" style="text-align: center">D</th>
                <th onclick="sortTableByColumn('leagueTable', 6)" class="league-table-col-general" style="text-align: center">L</th>
                <th onclick="sortTableByColumn('leagueTable', 7)" class="league-table-col-general" style="text-align: center">GF</th>
                <th onclick="sortTableByColumn('leagueTable', 8)" class="league-table-col-general" style="text-align: center">GA</th>
                <th onclick="sortTableByColumn('leagueTable', 9)" class="league-table-col-general" style="text-align: center">GD</th>
                <th onclick="sortTableByColumn('leagueTable', 10)" class="league-table-col-general" style="text-align: center">Pts</th>
                <th onclick="sortTableByColumn('leagueTable', 11)" class="league-table-col-form" style="text-align: center">Form</th>
            <tr>
        </thead>
        <tbody>
    """
    for team in team_records:
        html += f"""
            <tr>
                <td class="league-table-col-general" style="text-align: center">{int(team['position'])}</td>
                <td class="league-table-col-badge" style="text-align: center"><img src="{TEAM_BADGES[team['team_name']]}" width="30px"></td>
                <td class="league-table-col-name" style="text-align: left">{team['team_name']}</td>
                <td class="league-table-col-general" style="text-align: center">{team['matches_played']}</td>
                <td class="league-table-col-general" style="text-align: center">{team['won']}</td>
                <td class="league-table-col-general" style="text-align: center">{team['drawn']}</td>
                <td class="league-table-col-general" style="text-align: center">{team['lost']}</td>
                <td class="league-table-col-general" style="text-align: center">{team['goals_for']}</td>
                <td class="league-table-col-general" style="text-align: center">{team['goals_against']}</td>
                <td class="league-table-col-general" style="text-align: center">{team['goal_difference']}</td>
                <td class="league-table-col-general" style="text-align: center">{int(team['points'])}</td>
                <td class="league-table-col-form" style="text-align: center">{get_form_svg(team['form'])}</td>
            </tr>
        """
    html += """
        </tbody>
    </table>
    """
    return html
