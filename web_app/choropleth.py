from bokeh.plotting import figure, show, output_file, ColumnDataSource
from bokeh.models import HoverTool
import numpy as np
import pandas as pd
from utils import *

us_states = pd.read_pickle('.data/states_gps.pkl')
us_counties = pd.read_pickle('.data/counties_gps.pkl')
mainland_states = us_states[~us_states.state.isin(['AK', 'HI'])]
mainland_counties = us_counties[~us_counties.state.isin(['AK', 'HI'])].sort_values(by='county_norm')
yearly_actual_donors = pd.read_pickle('.data/yearly_actual_donors.pkl')
yearly_expected_donors = pd.read_pickle('.data/yearly_expected_donors.pkl')
indian_population = pd.read_pickle('.data/indian_population.pkl')


def get_gps_coordinates(statesfilter):
    states = mainland_states.copy()
    counties = mainland_counties.copy()
    states = states[(states.state.isin(statesfilter))]
    counties = counties[(counties.state.isin(statesfilter))]
    state_xs = states.lons.tolist()
    state_ys = states.lats.tolist()
    county_xs = counties.lons.tolist()
    county_ys = counties.lats.tolist()
    county_names = counties.county.values.tolist()
    return county_names, state_xs, state_ys, county_xs, county_ys


def make_value_plot(donations, year, region_name):
    states_filter = get_states_for_region(region_name)
    county_names, state_xs, state_ys, county_xs, county_ys = get_gps_coordinates(states_filter)
    data = donations[(donations.activity_year == year) & (donations.state.isin(states_filter))]\
      .groupby(['state', 'county_norm', 'activity_ym'])['amount', ]\
      .sum()\
      .unstack()\
      .fillna(0)\
      .sum(axis=1)\
      .to_frame()

    # Get colors for data
    ncat, bidi = 7, False
    palette = get_palette(ncat, bidi)
    labels = pd.qcut(data.values.flatten(), ncat, labels=range(ncat))
    color_values = [palette[b] for b in labels.get_values()]

    title = 'Donations in {0} for {1}'.format(year, region_name)
    p = figure(title=title, toolbar_location="left",
               tools='hover, wheel_zoom, resize, reset, help')
    hover = p.select(dict(type=HoverTool))
    hover.point_policy = "follow_mouse"
    hover.tooltips = """
            <div>
                @counties: @data
            </div>
            """
    source = ColumnDataSource(
            data = dict(
                xs=county_xs,
                ys=county_ys,
                counties=county_names,
                colors=color_values,
                data=data.values
            )
    )
    p.plot_width = 800

    plot_usa_choropleth(p, source, state_xs, state_ys)

    return p


def make_detail_plot(year, region_name):
    states_filter = get_states_for_region(region_name)
    county_names, state_xs, state_ys, county_xs, county_ys = get_gps_coordinates(states_filter)

    actual = yearly_actual_donors.query('state in @states_filter')[year]
    expected = yearly_expected_donors.query('state in @states_filter')[year]
    population = indian_population.query('state in @states_filter')[year]

    # Compute the difference between the actual and expected number of donors
    difference = actual - expected

    title = 'Unique number of donors in {0} for {1}'.format(year, region_name)
    p = figure(title=title, toolbar_location="left",
               tools='hover, wheel_zoom, resize, reset, help')

    # Get colors for data
    ncat, bidi = 7, False
    palette = get_palette(ncat, bidi)
    labels = pd.cut(difference.values.flatten(), ncat, labels=range(ncat))
    color_values = [palette[b] for b in labels.get_values()]

    hover = p.select(dict(type=HoverTool))
    hover.point_policy = "follow_mouse"
    hover.tooltips = """
            <div>
                <div>
                    <span style="font-size: 15px;">@counties</span>
                </div>
                <div>
                    <span style="font-size: 12px; color: #696;">Projected: @expected</span>
                </div>
                <div>
                    <span style="font-size: 12px; color: #696;">Actual: @actual</span>
                </div>
                <div>
                    <span style="font-size: 12px; color: #696;">Indian Population (Census): @population</span>
                </div>
            </div>
            """
    source = ColumnDataSource(
            data=dict(
                xs=county_xs,
                ys=county_ys,
                counties=county_names,
                colors=color_values,
                data=difference.values,
                expected=expected.values.tolist(),
                actual=actual.values.tolist(),
                population=population.values.tolist(),
            )
    )

    p.plot_width = 800
    plot_usa_choropleth(p, source, state_xs, state_ys)
    return p


def plot_usa_choropleth(p, source, state_xs, state_ys):
    '''
    input: bokeh figure
    input: ColumnDataSource object for bokeh figure
    input: State gps x-coordinates
    input: State gps y-coordinates

    Desc: Adds the choropleth plot to the given bokeh figure object
    '''

    # Turn off all axis and grid lines
    p.grid.grid_line_color = None
    p.axis.axis_line_color = None
    p.axis.major_label_text_font_size = '0pt'
    p.axis.major_tick_line_color = None
    p.axis[0].ticker.num_minor_ticks = 0
    p.axis[1].ticker.num_minor_ticks = 0

    # Determine optimal height based on p.width
    flat_xs = flatten(state_xs)
    flat_ys = flatten(state_ys)
    diff_x, diff_y = max(flat_xs) - min(flat_xs), max(flat_ys) - min(flat_ys)
    p.plot_height = int(p.plot_width*(diff_y/diff_x))

    p.patches(state_xs, state_ys, fill_alpha=0.0, line_color="#696969", line_width=1.5)
    # The following must be the last glyph for the hover to function properly
    p.patches(xs='xs', ys='ys', fill_color='colors', fill_alpha=0.7,
              line_color="#e77575", line_width=0.5, source=source)
