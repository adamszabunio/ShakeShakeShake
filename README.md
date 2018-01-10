# GalvanizeU Data Engineering Final Project
------
Current Website displaying the [Most Recent Earthquake Data](http://ec2-34-237-176-236.compute-1.amazonaws.com/)

## Introduction: 

This project is an end to end data engineering pipeline making API calls to query data from USGS.gov Earthquake Catalog: [API Call](https://earthquake.usgs.gov/fdsnws/event/1/). Historical earthquake data is updated daily, plotted using matplotlib and then deployed using a Flask app web server. Libraries used via the Amazon Web Services (EC2, RDS, EMR, and s3) platform include: requests, cron, boto, pyscopg2, and sqlalchemy.

The overarching goal of the project is to compare daily earthquakes in two locations, California and Oklahoma. 

Below are two basic plots that are created daily from querying the relational database. The first is a plot of daily earthquake counts in Oklahoma (since May 22, 2013). 

![](images/ok_quakes.png?raw=true)

![](images/recent_quakes_stacked.png?raw=true)

------

## Workflow

![](images/fiveSs.png?raw=true)
NOTE arrows in this image were only used to connect the columns

The raw data was sent to an AWS s3 bucket using boto (to make a connection to s3) and requests (to make the API call). 

To gather more data, a script was written to collect all earthquake events from the latest upgrade to the USGS.gov feed (May 22, 2013). All data collected up to this point (May 08, 2017) was cleaned and then transformed into 3rd Normal Form using pyspark and zepplin on an AWS EMR cluster (bootstraped with pyscopg2). This cluster used pyscopg2 to insert selected data to an AWS RDS table. 

A daily cron job continues to collect earthquakes at 00:01 UTC '1 0 * * *' (5:00 PM PST) and writes the records to an s3 bucket. 

Another daily cron job is set to connect to the most recent s3 file. It then uses pyscopg2 to insert select data into the RDS table with all of the previous day's earthquakes.

To create a [website displaying recent data](http://ec2-34-237-176-236.compute-1.amazonaws.com/), the data is queried with sqlalchemy and pandas to create dataframes and store them as html. Graphs are created from these dataframes with the matplotlib library and stored in a public s3 bucket. The html version of the dataframes and the graphs are uploaded to a website using a flask webserver. 


A DAG (directed acyclical graph) visualizing this framework can be found here: [DAG](images/dag.pdf)
------

## API Call:
------
Query data based on date from USGS.gov Earthquake Catalog: [API Call](https://earthquake.usgs.gov/fdsnws/event/1/)
 
Scripts used:

1. quakes.py
- Initial script created to access the API.

2. earthquakes.py 
- Queries earthquake reports from the current date using crontab job daily at 00:01 UTC '1 0 * * *'.
- Sends the raw data to a public s3 bucket: 'bucketshakesforyoudaily'     

3. retroactive_month.py 
- Was written to collect data from the beginning of the current API version, May 22nd, 2013.
- The query was limited to 30 days due to a limit: "Error 400: Bad Request matching events exceeds search limit of 20000."
- Raw data is stored in a public s3 bucket: 'bucketshakesforyou'     

4. retroactive_day.py
- Due to a failure of the EC2 instance, this script can pass any number of days as an argument to retroactively pull missing days

------

## Database:
------
Transform the raw data to 3rd Normal Form and place 

1. daily_rds.py 
- Connects to the most recent s3 file using boto. It then uses pyscopg2 to update the RDS table with the s3 file's data.

------

## Flask app:
------

1. flasksql.py
- Uses sqlalchemy to query an RDS table and pandas to create dataframes and store them as html. Graphs are created from these dataframes with the matplotlib library and stored in a public s3 bucket. The html version of the dataframes and the graphs are uploaded to a website using a flask webserver. 

----

## Room for improvement (Version 2.0)
------

1. At the moment, using a script to determine the max/min latitude and longitude (rectangular) coordinates per state.
  - Dictionaries of state/city/country polygon coordinates could be created and used to query more precise boundaries. 
  - Currently experimenting with geopandas and shapely. 

2. Currently the first cron job is schedulded to run at 00:05:00 UTC. A subsequent cron job runs five minutes later, but relies on the proper execution of the first cron job to produce accurate results.
  - A Directed Acyclic Graph scheduling technology, such as Airflow, could be used in place of cron.
  - Error messages could be put in place to send alerts via email. 
  

3. flasksql.py could be abstracted into a set of functions stored in another python module
  - these functions could be generalized to preform queries and computations based on a set of coordinates (e.g. states or cities). 
