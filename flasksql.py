#!/usr/bin/env python3
"""Spins up server for HTML for top 10 current global tweets."""
from flask import Flask
import os
import yaml
import pandas as pd
from sqlalchemy import create_engine
import psycopg2
from boto.s3.connection import S3Connection
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


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

    recent_mag = pd.read_sql("SELECT isotime, magnitude, longitude, latitude, altitude FROM quakes WHERE magnitude > 5.5 ORDER BY isotime DESC LIMIT 10", engine)
    top_recent_mag = recent_mag.to_html()

    oklahoma_recent = pd.read_sql("SELECT isotime, magnitude FROM quakes WHERE (longitude >= -103.029785 and longitude <= -94.416504) and (latitude >= 33.642063 and  latitude <= 37.02887) ORDER BY isotime DESC LIMIT 10", engine)
    ok_recent = oklahoma_recent.to_html()

    fig1 = plt.gcf()
    plt.hist(x="magnitude", data=oklahoma_recent)
    fig1.savefig("ok_quakes.png")

    aws_cred = credentials['aws']
    conn = S3Connection(aws_access_key_id=aws_cred['access_key_id'],
                        aws_secret_access_key=aws_cred['secret_access_key'])

    bucket = conn.get_bucket("nobucketforyou")
    plot_key = bucket.new_key('ok_quakes.png')
    plot_key.content_type = 'image/png'
    plot_key.set_contents_from_filename("ok_quakes.png",
                                        policy='public-read')

    index_html = '''<!DOCTYPE html>
    <html>
      <body>
        <p>10 Most recent Earthquakes with Magnitude > 5.5</p>
        {}
        <p>Most recent Earthquakes in Oklahoma</p>
        {}
        <img src="https://s3.amazonaws.com/nobucketforyou/ok_quakes.png">
      </body>
    </html>
    '''.format(top_recent_mag, ok_recent)

    return index_html


if __name__ == '__main__':
    app.run("0.0.0.0", port=80)
