from flask import Flask, request, render_template
from bokeh.plotting import figure, output_notebook, show
from bokeh import embed
from bokeh.models import HoverTool
import pandas as pd
import numpy as np
from monthly_line_plot import cumulative_amounts_chart
from choropleth import make_value_plot, make_detail_plot
import sys
import getopt
from utils import *

app = Flask('sef_web_app')
donations = pd.read_pickle('.data/donations.pkl')


# home page
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/yearly_donations')
def yearly_donations():
    year = tryget_int(request.args.get('year'), 2015)
    chart = cumulative_amounts_chart(donations, year)
    script, div = embed.components(chart)
    return render_template('index.html', script=script, div=div, title='Dashboard')


@app.route('/donations_by_region')
def donations_by_region():
    year = tryget_int(request.args.get('year'), 2015)
    region_name = request.args.get('region')
    chart = make_value_plot(donations, year=int(year), region_name=region_name)
    script, div = embed.components(chart)
    return render_template('index.html', script=script, div=div, title='')


@app.route('/donors_by_region')
def donors_by_region():
    year = tryget_int(request.args.get('year'), 2015)
    region_name = request.args.get('region')
    chart = make_detail_plot(year=year, region_name=region_name)
    script, div = embed.components(chart)
    return render_template('index.html', script=script, div=div, title='')


def process_input_args(argv):
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hm:", ["help", "mode="])
    except getopt.GetoptError:
        print sys.argv[0] + ' -m <dev|prod>'
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print sys.argv[0] + ' -m <dev|prod>'
            sys.exit()
        elif opt in ("-m", "--mode"):
            mode = arg
    if mode == 'dev':
        port = 8080
        host = '0.0.0.0'
    elif mode == 'prod':
        port = 80
        host = '0.0.0.0'
    return host, port

if __name__ == '__main__':
    app_host, app_port = process_input_args(sys.argv[1:])
    app.run(host=app_host, port=app_port, debug=True)
