#!/usr/bin/python3
"""
In case of an EC2 failure, this script can pass any number of days as an
argument to retroactively pull missing days
"""
import yaml
import os
import requests
import datetime
from boto.s3.connection import S3Connection
from boto.s3.key import Key


def main(days):
    """
    Take in one argument, days: int
    This pulls all earthquakes recored daily.
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

    for day in range(0, days):
        bucket = conn.get_bucket('bucketshakesforyou')
        num_day_start = datetime.timedelta(days=day+1)
        num_day_end = datetime.timedelta(days=day)
        today = datetime.date.today()
        end_day = today - num_day_end
        start_day = today - num_day_start
        start = start_day.strftime('%Y-%m-%d')
        end = end_day.strftime('%Y-%m-%d')
        url_str = "https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&"\
                    + "starttime=" + start + "&endtime=" + end
        r = requests.get(url_str)

        k = Key(bucket)
        k.key = start
        k.set_contents_from_string(r.text)


if __name__ == '__main__':
    main()
