#!/usr/bin/python3
"""
earthquake.py uses API documentation from
"https://earthquake.usgs.gov/fdsnws/event/1/#methods"
to query earthquake reports from the current date
will pair with a crontab job AT 23:59 UTC '59 23 * * *'.
"""

import json
import requests
from datetime import datetime
from pprint import pprint

i = datetime.utcnow()
start = i.strftime('%Y-%m-%d')
# if %h-%m starttime is not specified, will gather reports from UTC 00:00
url_str = "https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&"\
            + "starttime=" + start + "&endtime"
r = requests.get(url_str)
data = json.loads(r.text)
pprint(data)
