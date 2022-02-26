from typing import Sequence
import pandas as pd
import datetime
from hela._utils.date_utils import get_date_range_from_set
from hela.plots.html_displays import HTMLDisplay


def plot_date_availability_calendar(dates: Sequence[datetime.date]) -> HTMLDisplay:
    colors = {
        'exists': '#77DD77',
        'missing': '#FF6961',
        'NA': 'white'
    }

    def color_df(val):
        try:
            day, exists = val
        except TypeError:
            day, exists = '', None
        color = colors['NA'] if exists is None else colors['exists'] if exists else colors['missing']
        return f'c:{color}{day}'

    possible_dates = list(get_date_range_from_set(dates))
    date_check_list = list(zip(possible_dates, [True if d in dates else False for d in possible_dates]))
    df = pd.DataFrame([
        {'year-month': (d.year, d.month), 'date': d.day, 'day_exists': (d.day, exists)}
        for d, exists in date_check_list
    ])
    df = df.pivot(index='year-month', columns='date')
    df = df.applymap(color_df)
    html_str = df.to_html(escape=False, header=False)
    replacements = [(f'<td>c:{c}', f'<td style="background-color:{c}">') for c in colors.values()]
    for fs, ns in replacements:
        html_str = html_str.replace(fs, ns)
    return HTMLDisplay(html_str)
