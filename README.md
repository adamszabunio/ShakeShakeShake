# ShakeShakeShake
GalvanizeU Data Engineering Final Project
------

This project makes daily API calls to query data from USGS.gov Earthquake Catalog: [API Call](https://earthquake.usgs.gov/fdsnws/event/1/)

The raw data was sent to an AWS s3 bucket using boto (to make a connection to s3) and requests (to make the API call). 

To gather more data, a script was written to collect all earthquake events from the latest upgrade to the USGS.gov feed (May 22, 2013). All data collected up to this point (May 08, 2017) was cleaned and then transformed into 3rd Normal Form using pyspark and zepplin on an AWS EMR cluster (bootstraped with pyscopg2). This cluster used pyscopg2 to insert selected data to an AWS RDS table. 

A daily cron job continues to collect earthquakes at 00:01 UTC '1 0 * * *' (5:00 PM PST) and write them to an s3 bucket. 

Another daily cron job is set to connect to the most recent s3 file. It then uses pyscopg2 to insert select data into the RDS table with all of the previous day's earthquakes.

To create the website [Most Recent Earthquake Data](http://ec2-34-200-221-198.compute-1.amazonaws.com/), the data is then queried with sqlalchemy and pandas to create dataframes. matplotlib uses the dataframes to create graphs. The dataframes are stored as html and along with the graphs are uploaded to a website using a flask webserver. 

A DAG (directed acyclical graph) visualizing this framework can be found here: [DAG](https://s3.amazonaws.com/nobucketforyou/dag.pdf)


API Call Scripts:
------

1. quakes.py
- Initial script created to access the API.

2. earthquakes.py 
- Queries earthquake reports from the current date using crontab. Sends the raw data to a public s3 bucket: 'bucketshakesforyoudaily'     

3. retroactive_month.py 
- Was written to collect data from the beginning of the current API version, May 22nd, 2013. The query was limited to 30 days due to a limit: "Error 400: Bad Request matching events exceeds search limit of 20000." Sends the raw data to a public s3 bucket: 'bucketshakesforyou'     

4. retroactive_day.py
- Due to a failure of the EC2 instance, this script can pass any number of days as an argument to retroactively pull missing days


Database scripts:
------

1. daily_rds.py 
- Connects to the most recent s3 file using boto. It then uses pyscopg2 to update the RDS table with the s3 file's data.


Flask scripts:
------

1. flasksql.py
- Uses sqlalchemy to query an RDS table and pandas to create dataframes. matplotlib uses the dataframes to create graphs. The dataframes are stored as html and along with the graphs are uploaded to a website using a flask webserver.


Room for improvement
----
