#!/usr/bin/python3
import yaml
import os
from boto.s3.connection import S3Connection

def main():
    """
    Creates bucket policy
    1. Import credentials
    2. Connect to S3
    3. Create bucket: 'bucketshakesforyoudaily'
    """
    credentials = yaml.load(open(os.path.expanduser
                            ('/vagrant/credentials.yml')))

    aws_cred = credentials['aws']
    conn = S3Connection(aws_access_key_id=aws_cred['access_key_id'],
                        aws_secret_access_key=aws_cred['secret_access_key'])

    website_bucket = conn.create_bucket('bucketshakesforyoudaily')
    website_bucket.set_policy('''{
      "Version":"2012-10-17",
      "Statement": [{
        "Sid": "Allow Public Access to All Objects",
        "Effect": "Allow",
        "Principal": "*",
        "Action": "s3:GetObject",
        "Resource": "arn:aws:s3:::%s/*"
      }
     ]
    }''' % website_bucket.name)


if __name__ == '__main__':
    main()
