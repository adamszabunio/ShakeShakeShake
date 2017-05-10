#!/usr/bin/python3
"""
earthquake.py uses API documentation from
"https://earthquake.usgs.gov/fdsnws/event/1/#methods"
to query earthquake reports from the current date
will pair with a crontab job daily at 00:01 UTC '1 0 * * *'.
"""
import yaml
import os
import requests
import datetime
from boto.s3.connection import S3Connection
from boto.s3.key import Key


def main():
    """
    Pulls all earthquakes recored daily.
    1. Import credentials
    2. Connect to S3, 'bucketshakesforyoudaily'
    3. Create date specific timestamps range(yesterday-midnight)
    4. Request from usgs.gov website
    5. Save as json string
    6. Create Key based on relevant day timestamp
    7. Push to S3
    """
    credentials = yaml.load(open(os.path.expanduser
                            ('/vagrant/credentials.yml')))

    aws_cred = credentials['aws']
    conn = S3Connection(aws_access_key_id=aws_cred['access_key_id'],
                        aws_secret_access_key=aws_cred['secret_access_key'])

    bucket = conn.get_bucket('bucketshakesforyoudaily')

    one_day = datetime.timedelta(days=1)
    today = datetime.date.today()
    yesterday = today - one_day
    start = yesterday.strftime('%Y-%m-%d')
    # if %h-%m starttime or endtime are not specified, will gather reports from
    # UTC %Y-%m-%d:00:00
    end = today.strftime('%Y-%m-%d')
    url_str = "https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&"\
              + "starttime=" + start + "&endtime=" + end

    r = requests.get(url_str)

    k = Key(bucket)
    k.key = start
    k.set_contents_from_string(r.text)


if __name__ == '__main__':
    main()
