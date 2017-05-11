#!/usr/bin/env python3
"""Does way too much."""
from flask import Flask
import os
import yaml
import pandas as pd
from sqlalchemy import create_engine
import datetime
import numpy as np
import psycopg2
from boto.s3.connection import S3Connection
# from california import state_stats
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


app = Flask(__name__)


@app.route('/')
def create_tables():
    """
    This displays a pandas dataframe.
    1. Import credentials
    2. connect to postgresql API
    3. Create pandas df
    4. Save as html
    """
    credentials = yaml.load(open(os.path.expanduser
                            ('/vagrant/credentials.yml')))

    engine = create_engine(
        'postgresql://{user}:{password}@{host}:{port}/{dbname}'
        .format(**credentials['rds']))


    # recent = pd.read_sql("SELECT isotime, magnitude, longitude, latitude, altitude FROM quakes ORDER BY isotime DESC LIMIT 10", engine)
    # recent_global = recent.to_html()

    # top 10 earthquakes since 5/22/2013
    top_10 = pd.read_sql("SELECT isotime, magnitude, longitude, latitude, altitude FROM quakes ORDER BY magnitude DESC", engine)
    top_10 = top_10.dropna()
    top_10_html = top_10.head(10).to_html()

    # top 10 recent earthquakes with magnitude > 5.5
    recent_mag = pd.read_sql("SELECT isotime, magnitude, longitude, latitude, altitude FROM quakes WHERE magnitude > 5.5 ORDER BY isotime DESC LIMIT 10", engine)
    top_recent_mag = recent_mag.to_html()

    oklahoma_recent = pd.read_sql("SELECT isotime, magnitude FROM quakes WHERE (longitude >= -103.029785 and longitude <= -94.416504) and (latitude >= 33.642063 and  latitude <= 37.02887) ORDER BY isotime DESC LIMIT 100", engine)
    ok_recent = oklahoma_recent.head(10).to_html()

    # fig1 = plt.gcf()
    # plt.hist(x="magnitude", data=oklahoma_recent)
    # fig1.savefig("ok_quakes.png")

    tbl = oklahoma_recent.dropna()

    def mag_category(x):
        if x <= 2.5:
            return("0-2.5, not felt")
        elif x > 2.5 and x < 5.5:
            return("2.5-5.5, felt, minor damage")
        else:
            return("5.5 and above, potential for major damage")

    tbl['magnitude'] = tbl['magnitude'].apply(lambda x: mag_category(x))
    tbl.isotime = tbl.isotime.dt.date
    tbl = tbl.groupby(['isotime', 'magnitude'])['isotime'].count().unstack('magnitude').fillna(0)

    ax = tbl.plot(kind='bar', stacked=True, figsize=(10, 8))
    ax.set_title("Oklahoma 100 Most Recent Earthquakes", fontsize=20)
    ax.legend(fontsize=15)
    ax.legend_.set_title("Magnitude Range", prop={'size': 18})
    ax.set_ylabel("Count", fontsize=18)
    ax.xaxis_date()
    ax.set_xlabel("Date (if missing, no recorded Earthquake)", fontsize=18)
    ax.grid(True)
    fig = ax.get_figure()
    fig.tight_layout()
    fig.savefig('recent_quakes_stacked.png')

    tbl2 = pd.read_sql("SELECT isotime FROM quakes WHERE (longitude >= -103.029785 and longitude <= -94.416504) and (latitude >= 33.642063 and  latitude <= 37.02887)", engine)
    locator = mdates.AutoDateLocator()
    years = mdates.YearLocator()

    fig, ax = plt.subplots(figsize=(10, 8))
    data = tbl2.isotime.dt.date
    mpl_data = mdates.date2num(data)
    ax.hist(mpl_data, bins=len(data.unique()))
    ax.set_title("Oklahoma Earthquake Counts Per Day (if occurred)", fontsize=20)
    ax.set_ylabel("Count", fontsize=18)
    ax.set_xlabel("Time", fontsize=18)
    ax.xaxis.set_major_locator(years)
    ax.xaxis.set_major_formatter(mdates.AutoDateFormatter(locator))
    datemin = datetime.date(tbl2.isotime.min().year, 1, 1)
    datemax = datetime.date(tbl2.isotime.max().year + 1, 1, 1)
    ax.set_xlim(datemin, datemax)
    ax.set_ylim(0, 50)
    ax.grid(True)
    fig.tight_layout()
    fig.savefig("ok_quakes.png")

    aws_cred = credentials['aws']
    conn = S3Connection(aws_access_key_id=aws_cred['access_key_id'],
                        aws_secret_access_key=aws_cred['secret_access_key'])

    bucket = conn.get_bucket("nobucketforyou")
    stacked_plot_key = bucket.new_key('recent_quakes_stacked.png')
    stacked_plot_key.content_type = 'image/png'
    stacked_plot_key.set_contents_from_filename('recent_quakes_stacked.png',
                                                policy='public-read')

    ok_all_key = bucket.new_key('ok_quakes.png')
    ok_all_key.content_type = 'image/png'
    ok_all_key.set_contents_from_filename('ok_quakes.png',
                                            policy='public-read')

    # state_stats(state='California', long_min=-124.40918, long_max=-114.191895, lat_min=32.546814, lat_max=42.016651)

    long_min = -124.40918
    long_max = -114.191895
    lat_min = 32.546814
    lat_max = 42.016651
    # state = "california"

    california_recent = pd.read_sql("SELECT isotime, magnitude FROM quakes WHERE (longitude >= {} and longitude <= {}) and (latitude >= {} and latitude <= {}) ORDER BY isotime DESC LIMIT 100".format(long_min, long_max, lat_min, lat_max), engine)
    ca_recent = california_recent.head(10).to_html()

    # tbl3 = california_recent.dropna()
    #
    # tbl3['magnitude'] = tbl3['magnitude'].apply(lambda x: mag_category(x))
    # tbl3.isotime = tbl3.isotime.dt.date
    # tbl3 = tbl3.groupby(['isotime', 'magnitude'])['isotime'].count().unstack('magnitude').fillna(0)
    #
    # ax = tbl3.plot(kind='bar', stacked=True, figsize=(12, 8))
    # ax.set_title("100 most recent instances for {}".format(state), fontsize=25)
    # ax.legend(fontsize=20)
    # ax.legend_.set_title("Magnitude Range", prop={'size': 20})
    # ax.set_ylabel("Count", fontsize=20)
    # ax.xaxis_date()
    # ax.set_xlabel("Counts per day (if occured)", fontsize=20)
    # ax.grid(True)
    # fig = ax.get_figure()
    # fig.tight_layout()
    # state_fig_name_stacked = '{}_recent_quakes_stacked.png'.format(state)
    # fig.savefig(state_fig_name_stacked)
    #
    # tbl4 = pd.read_sql("SELECT isotime FROM quakes WHERE (longitude >= {} and longitude <= {}) and (latitude >= {} and latitude <= {})".format(long_min, long_max, lat_min, lat_max), engine)
    # locator = mdates.AutoDateLocator()
    # years = mdates.YearLocator()
    #
    # fig, ax = plt.subplots(figsize=(12, 8))
    # data = tbl4.isotime.dt.date
    # mpl_data = mdates.date2num(data)
    # ax.hist(mpl_data, bins=len(data.unique()))
    # ax.set_title("{} Earthquake counts per day (if occurred)".format(state), fontsize=25)
    # ax.set_ylabel("Count", fontsize=15)
    # ax.set_xlabel("Time", fontsize=15)
    # ax.xaxis.set_major_locator(years)
    # ax.xaxis.set_major_formatter(mdates.AutoDateFormatter(locator))
    # datemin = datetime.date(tbl4.isotime.min().year, 1, 1)
    # datemax = datetime.date(tbl4.isotime.max().year + 1, 1, 1)
    # ax.set_xlim(datemin, datemax)
    # ax.set_ylim(0, 45)
    # ax.grid(True)
    # fig.tight_layout()
    # state_quakes = "{}_quakes.png".format(state)
    # fig.savefig(state_quakes)
    #
    # bucket = conn.get_bucket("nobucketforyou")
    # ca_stacked_plot_key = bucket.new_key(state_fig_name_stacked)
    # ca_stacked_plot_key.content_type = 'image/png'
    # ca_stacked_plot_key.set_contents_from_filename(state_fig_name_stacked,
    #                                             policy='public-read')
    #
    # ca_all_key = bucket.new_key(state_quakes)
    # ca_all_key.content_type = 'image/png'
    # ca_all_key.set_contents_from_filename(state_quakes,
    #                                         policy='public-read')

    index_html = '''<!DOCTYPE html>
    <html>
    <head>
        <style>
            * {{
                box-sizing: border-box;
            }}

            .magnitude-table-container {{
                display: inline-block;
                width: 49%;
                padding: 10px;
            }}

            .magnitude-table-container table {{
                width: 100%;
            }}

            .magnitude-table-container th,
            .magnitude-table-container td, h4, h2 {{
                text-align: center;
            }}

            .stack-histogram {{
                margin: 60px 0;
                text-align: center;
                img {{
                    width: 100%;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="magnitude-table-container">
            <h4>10 Most Recent Earthquakes in Oklahoma</h4> {}
        </div>
        <div class="magnitude-table-container">
            <h4>10 Most Recent Earthquakes in California</h4> {}
        </div>
        <div class="stack-histogram">
            <img src="https://s3.amazonaws.com/nobucketforyou/recent_quakes_stacked.png">
        </div>
        <div class="stack-histogram">
            <img src="https://s3.amazonaws.com/nobucketforyou/ok_quakes.png">
        </div>
            <h2>Some fun facts!</h2>
        <div class="magnitude-table-container">
            <h4>10 Most Recent Earthquakes Globally with Magnitude &gt; 5.5</h4> {}
        </div>

        <div class="magnitude-table-container">
            <h4>10 Strongest Earthquakes Since 5/22/2013</h4> {}
        </div>
            <h4>Data updated daily at 00:00 UTC (5:00 PM PST). For more
                information visit:
            <a href="https://github.com/adamszabunio/ShakeShakeShake">
                https://github.com/adamszabunio/ShakeShakeShake</a></h4>
    </body>

    </html>'''.format(ok_recent, ca_recent, top_recent_mag, top_10_html)

    return index_html


if __name__ == '__main__':
    app.run("0.0.0.0", port=80)
