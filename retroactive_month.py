#!/usr/bin/python3
"""
retroactive_month.py was written to collect data from the beginning of the
current API version, May 22nd, 2013
The month parameter was limited to 30 days due to a "Error 400: Bad Request
matching events exceeds search limit of 20000"
With a little investigation, the average month contained 11,000 events
"""
import yaml
import os
import requests
import datetime
from boto.s3.connection import S3Connection
from boto.s3.key import Key

def main(months):
    """
    Take in one argument, months: int
    This pulls all earthquakes recored monthly (30 days)
    1. Import credentials
    2. Connect to S3, 'bucketshakesforyou'
    3. Create date specific timestamp
    4. Pull from usgs.gov website
    5. Save as json string
    6. Create Key(s) based on relevant day(s) timestamp
    7. Push to S3
    """

    credentials = yaml.load(open(os.path.expanduser
                            ('/vagrant/credentials.yml')))

    aws_cred = credentials['aws']
    conn = S3Connection(aws_access_key_id=aws_cred['access_key_id'],
                        aws_secret_access_key=aws_cred['secret_access_key'])

    production_version = datetime.date(2013,5,22)
    beg_month = production_version
    # for a more robust code:
    # today = datetime.date.today()
    # while end_day < today:
    #   if end_day > today:
    #       end_day = today
    for month in range(1, months):
        bucket = conn.get_bucket('bucketshakesforyou')
        end_month = datetime.timedelta(days=30)
        end_day = beg_month + end_month
        start_day = beg_month
        start = start_day.strftime('%Y-%m-%d')
        end = end_day.strftime('%Y-%m-%d')
        url_str = "https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&"\
                  + "starttime=" + start + "&endtime=" + end

        r = requests.get(url_str)

        k = Key(bucket)
        k.key = start
        k.set_contents_from_string(r.text)
        beg_month += end_month


if __name__ == '__main__':
    # to capture all data from production_version until current date the month
    # parameter was set to 49
    main(49)
