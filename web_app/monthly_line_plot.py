from bokeh.plotting import figure, output_notebook, show, ColumnDataSource
from bokeh.models.formatters import NumeralTickFormatter
import calendar
from bokeh.models import HoverTool
import seaborn as sns
import numpy as np
import pandas as pd
from utils import *


def cumulative_amounts_chart(donations, year):
    tools = "hover,box_select,lasso_select,help"
    p = figure(plot_width=600, plot_height=600, x_range=calendar.month_abbr[1:], tools=[tools])
    year_month_data = donations[donations.activity_year.isin([year, year-1, year-2])]\
        .groupby(['activity_year', 'activity_month'])['amount', ]\
        .sum()\
        .unstack()\
        .fillna(0)

    monthly_line_plot(year_month_data, p, cumulative=True)

    return p


def monthly_line_plot(year_month_data, p, cumulative=True):
    '''
    input: year_month_data (dataframe)
    input: bokeh figure object
    input: cumulative (boolean) - whether cumulative or not
    output: none

    Expects year_month_data to have the following:
    columns: level 0: 'amount', level 1: integer for months (1-12)
    index: level 0: integer for years

    Adds the line plot to the given bokeh figure object
    '''

    hover = p.select(dict(type=HoverTool))
    hover.point_policy = "follow_mouse"
    hover.tooltips = """
            <div>
                @months, @years
            </div>
            """

    y_label = 'Total Amount'
    if cumulative:
        y_label += ' (cumulative)'
        data = np.cumsum(year_month_data, axis=1, dtype='int64')
    else:
        data = year_month_data.copy()

    years = sorted(data.index.get_level_values(0).unique())

    num_years = len(years)
    months = range(1,13)

    palette = sns.color_palette("muted", num_years).as_hex()
    allxs = np.array(months * num_years)

    source = ColumnDataSource(
            data=dict(
                x=allxs,
                y=flatten(data.values),
                months=calendar.month_abbr[1:]*num_years,
                years=np.repeat(years, 12),
            )
    )

    p.circle('x', 'y', size=10, source=source)
    p.xaxis.axis_label = 'Month'
    p.yaxis.axis_label = y_label
    p.yaxis.formatter = NumeralTickFormatter(format='0,0')

    xs = months
    for ix, year in enumerate(years):
        ys = data[data.index==year].values[0]
        p.line(x=xs, y=ys, line_width=2, line_color=palette[ix], legend=str(year))

    p.legend.orientation = "top_left"
    return p
