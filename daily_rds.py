#!/usr/bin/python3
'''
Schema for:
TABLE quakes has the following columns:
    quake_id - character varying - length < 20 - PRIMARY KEY and NOT NULL
    isotime - timestamp without time zone
    magnitude - real
    longitude - double precision
    latitude - double precision
    altitude - real
'''

import json
from os.path import expanduser
import psycopg2
from psycopg2 import IntegrityError, InternalError
from boto.s3.connection import S3Connection
import yaml
import datetime


def get_quakes(quake):
    '''
    INPUT: dict of quakes
    OUTPUT: list of length 6 w/ the following values:
            quake_id
            isotime
            magnitude
            longitude
            latitude
            altitude
    '''
    try:
        quake_id = quake["id"]
        # isotime = quake.get("properties").get("time")
        properties = quake.get("properties")
        if properties:
            epochtime = properties.get("time")  # machine readable timestamp
            isotime = datetime.datetime.utcfromtimestamp(epochtime/1000).isoformat()  # human readable timestamp
            magnitude = properties.get("mag")

        geometry = quake.get("geometry")
        if geometry:
            longitude = geometry.get("coordinates")[0]
            latitude = geometry.get("coordinates")[1]
            altitude = geometry.get("coordinates")[2]

        return [quake_id, isotime, magnitude, longitude, latitude, altitude]

    except ValueError:
        pass


def main():
    '''
    INPUT: None
    OUTPUT: None
        Inserts all tweets into postgres using `get_quakes`
    '''
    credentials = yaml.load(open(expanduser('/vagrant/credentials.yml')))

    aws_cred = credentials['aws']
    conns3 = S3Connection(aws_access_key_id=aws_cred['access_key_id'],
                          aws_secret_access_key=aws_cred['secret_access_key'])

    bucket = conns3.get_bucket('bucketshakesforyoudaily')

    one_day = datetime.timedelta(days=1)
    today = datetime.date.today()
    yesterday = today - one_day
    quake_key = yesterday.strftime('%Y-%m-%d')

    qkey = bucket.get_key(quake_key).get_contents_as_string().decode('utf-8').replace('\n', '')
    quakes_dict = json.loads(qkey)

    conn = psycopg2.connect(**credentials['rds'])
    cur = conn.cursor()
    # total_count = 0

    for quake in quakes_dict['features']:
        # total_count += 1
        q = get_quakes(quake)

        try:
            cur.execute("INSERT INTO quakes VALUES (%s,%s,%s,%s,%s,%s)", q)
            conn.commit()

        except (IntegrityError, InternalError) as e:  # prevents duplicates
            cur.execute("rollback") # conn.rollback()

    conn.commit()
    conn.close()
    # print('Inserted {} quakes'.format(total_count))

if __name__ == '__main__':
    main()
