# ShakeShakeShake
------
GalvanizeU Data Engineering Final Project
<<<<<<< HEAD

Current Website displaying the [Most Recent Earthquake Data](http://ec2-34-200-221-198.compute-1.amazonaws.com/)

API Call:
------
Query data based on date from USGS.gov Earthquake Catalog: [API Call](https://earthquake.usgs.gov/fdsnws/event/1/)
 
Scripts used:

1. quakes.py
Initial script created to access the API.

2. earthquakes.py 
Queries earthquake reports from the current date using crontab job daily at 00:01 UTC '1 0 * * *'.
Sends the raw data to a public s3 bucket: 'bucketshakesforyoudaily'     

3. retroactive_month.py 
Was written to collect data from the beginning of the current API version, May 22nd, 2013.
The query was limited to 30 days due to a limit: "Error 400: Bad Request matching events exceeds search limit of 20000."
Also sent the raw data to a public s3 bucket: 'bucketshakesforyou'     

4. retroactive_day.py
Due to a failure of the EC2 instance, this script can pass any number of days as an
argument to retroactively pull missing days

Database:
------
Transform the raw data to 3rd Normal Form and place 
||||||| merged common ancestors
=======

Current Website displaying the [Most Recent Earthquake Data](http://ec2-34-200-221-198.compute-1.amazonaws.com/)


API:
------
Query data based on date from USGS.gov Earthquake Catalog: [API Call](https://earthquake.usgs.gov/fdsnws/event/1/)
 
Scripts used:

1. quakes.py
Initial script created to access the API.

2. earthquakes.py 
Queries earthquake reports from the current date using crontab job daily at 00:01 UTC '1 0 * * *'.
Sends the raw data to a public s3 bucket: 'bucketshakesforyoudaily'     

3. retroactive_month.py 
Was written to collect data from the beginning of the current API version, May 22nd, 2013.
The query was limited to 30 days due to a limit: "Error 400: Bad Request matching events exceeds search limit of 20000."
Also sent the raw data to a public s3 bucket: 'bucketshakesforyou'     

4. retroactive_day.py
Due to a failure of the EC2 instance, this script can pass any number of days as an
argument to retroactively pull missing days


>>>>>>> ddce53fc9bfc371afa33d1a0a1ca4b117d475657
