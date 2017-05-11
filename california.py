#!/usr/bin/env python3
"""Does just enough for California."""
import os
import yaml
import pandas as pd
from sqlalchemy import create_engine
import datetime
import numpy as np
import psycopg2
from boto.s3.connection import S3Connection
from magnitude import mag_category
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


def state_stats(state, long_min, long_max, lat_min, lat_max):
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

    california_recent = pd.read_sql("SELECT isotime, magnitude FROM quakes WHERE (longitude >= {} and longitude <= {}) and (latitude >= {} and latitude <= {}) ORDER BY isotime DESC LIMIT 100".format(long_min, long_max, lat_min, lat_max), engine)
    ca_recent = california_recent.head(10).to_html()

    tbl = california_recent.dropna()

    tbl['magnitude'] = tbl['magnitude'].apply(lambda x: mag_category(x))
    tbl.isotime = tbl.isotime.dt.date
    tbl = tbl.groupby(['isotime', 'magnitude'])['isotime'].count().unstack('magnitude').fillna(0)

    ax = tbl.plot(kind='bar', stacked=True, figsize=(12, 8))
    ax.set_title("100 most recent instances for {}".format(state), fontsize=25)
    ax.legend(fontsize=20)
    ax.legend_.set_title("Magnitude Range", prop={'size': 20})
    ax.set_ylabel("Count", fontsize=20)
    ax.xaxis_date()
    ax.set_xlabel("Counts per day (if occured)", fontsize=20)
    ax.grid(True)
    fig = ax.get_figure()
    fig.tight_layout()
    state_fig_name_stacked = '{}_recent_quakes_stacked.png'.format(state)
    fig.savefig(state_fig_name_stacked)


    tbl2 = pd.read_sql("SELECT isotime FROM quakes WHERE (longitude >= {} and longitude <= {}) and (latitude >= {} and latitude <= {})".format(long_min, long_max, lat_min, lat_max), engine)
    locator = mdates.AutoDateLocator()
    years = mdates.YearLocator()

    fig, ax = plt.subplots(figsize=(12, 8))
    data = tbl2.isotime.dt.date
    mpl_data = mdates.date2num(data)
    ax.hist(mpl_data, bins=len(data.unique()))
    ax.set_title("{} Earthquake counts per day (if occurred)".format(state), fontsize=25)
    ax.set_ylabel("Count", fontsize=15)
    ax.set_xlabel("Time", fontsize=15)
    ax.xaxis.set_major_locator(years)
    ax.xaxis.set_major_formatter(mdates.AutoDateFormatter(locator))
    datemin = datetime.date(tbl2.isotime.min().year, 1, 1)
    datemax = datetime.date(tbl2.isotime.max().year + 1, 1, 1)
    ax.set_xlim(datemin, datemax)
    ax.set_ylim(0, 45)
    ax.grid(True)
    fig.tight_layout()
    state_quakes = "{}_quakes.png".format(state)
    fig.savefig(state_quakes)

    aws_cred = credentials['aws']
    conn = S3Connection(aws_access_key_id=aws_cred['access_key_id'],
                        aws_secret_access_key=aws_cred['secret_access_key'])

    bucket = conn.get_bucket("nobucketforyou")
    stacked_plot_key = bucket.new_key(state_fig_name_stacked)
    stacked_plot_key.content_type = 'image/png'
    stacked_plot_key.set_contents_from_filename(state_fig_name_stacked,
                                                policy='public-read')

    ok_all_key = bucket.new_key(state_quakes)
    ok_all_key.content_type = 'image/png'
    ok_all_key.set_contents_from_filename(state_quakes,
                                            policy='public-read')

    return(ca_recent)
