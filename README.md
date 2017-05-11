# ShakeShakeShake
------
GalvanizeU Data Engineering Final Project

Visit this: [Website](http://ec2-34-200-221-198.compute-1.amazonaws.com/) fo


Dataset:
------
Tree types found in the Roosevelt National Forest in Colorado.
[Earthquake API Call](https://earthquake.usgs.gov/fdsnws/event/1/)





earthquake.py uses API documentation from
"https://earthquake.usgs.gov/fdsnws/event/1/#methods"
to query earthquake reports from the current date
will pair with a crontab job daily at 00:01 UTC '1 0 * * *'.

retroactive_month.py was written to collect data from the beginning of the
current API version, May 22nd, 2013
The month parameter was limited to 30 days due to a "Error 400: Bad Request
matching events exceeds search limit of 20000"
With a little investigation, the average month contained 11,000 events


