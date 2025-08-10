from typing import List

import pandas as pd


def create_player_stat_rank_table_html(
    players_df: pd.DataFrame,
    title: str,
    table_id: str,
    stat_col: str,
    sort_cols: List[str],
    ascending: List[bool],
    number_of_rows: int = 10,
) -> str:
    df = (
        players_df.sort_values(by=sort_cols, ascending=ascending)
        .head(number_of_rows)
        .reset_index(drop=True)
        .copy()
    )

    html = f"""
    <style>
    #{table_id}_title {{
        font-family: Helvetica, sans-serif;
        color: #37003c;
        font-size: 30px;
        text-align: left;
        font-weight: bold;
    }}

    #{table_id} {{
        border-collapse: collapse;
        font-family: Helvetica, sans-serif;
        text-align: center;
        border-radius: 12px; /* round corners */
        overflow: hidden; /* ensures background colors follow rounded edges */
    }}

    #{table_id} td {{
        background-color: #ffffff;
        color: #37003c;
        font-size: 20px;
        vertical-align: middle;
        text-align: center;
    }}

    #{table_id} td.reg_stat {{
        font-size: 20px;
    }}

    #{table_id} td.reg_name {{
        font-size: 16px;
    }}

    #{table_id} img {{
        display: block;
        margin: auto;
    }}

    #{table_id} td.top1_stat {{
        font-size: 28px !important;
        font-weight: bold;
    }}

    #{table_id} td.top1_name {{
        font-size: 24px !important;
        font-weight: bold;
    }}


    #{table_id} td.top2_stat {{
        font-size: 24px !important;
        font-weight: bold;
    }}

    #{table_id} td.top2_name {{
        font-size: 20px !important;
        font-weight: bold;
    }}


    #{table_id} td.top3_stat {{
        font-size: 20px !important;
        font-weight: bold;
    }}

    #{table_id} td.top3_name {{
        font-size: 16px !important;
        font-weight: bold;
    }}

    #{table_id} tr:nth-child(1) td {{ background-color: #fff8dc; }} /* soft gold */
    #{table_id} tr:nth-child(2) td {{ background-color: #f0f0f5; }} /* soft silver */
    #{table_id} tr:nth-child(3) td {{ background-color: #fdf5e6; }} /* soft bronze */

    #{table_id} tr:nth-child(even) td {{
        background-color: #fafafa;
    }}

    </style>

    <h2 id="{table_id}_title">{title}</h2>
    <table id="{table_id}">
    """

    row_heights = {1: 160, 2: 120, 3: 80}

    html += "<tbody>"
    for index, row in df.iterrows():
        row_num = index + 1
        td_stat_class = f"top{row_num}_stat" if row_num <= 3 else "reg_stat"
        td_name_class = f"top{row_num}_name" if row_num <= 3 else "reg_name"
        img_height = row_heights.get(row_num, 80)

        html += f"""
        <tr style="height: {img_height}px;">
            <td style="width: 140px;"><img src="{row['player_png']}" style="height: {img_height}px;"></td>
            <td class="{td_name_class}" style='width: 100px;'>{row["player_name"]}</td>
            <td class="{td_stat_class}" style='width: 50px;'>{row[stat_col]}</td>
        </tr>
        """
    html += """
        </tbody>
    </table>
    """
    return html
