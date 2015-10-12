from datetime import date, timedelta
from time import strftime, sleep
from random import randint
from urllib import urlencode
from sys import argv
import json
import urllib2
# Local settings
import settings

# A station name must be given
if len(argv) < 2 or not settings.STATIONS.get(argv[1], False):
	# Human readable stations list
	stations = ', '.join( settings.STATIONS.keys() )
	# Print out the available stations
	print 'You must specify the station: %s' % stations
	# End now
	exit()

# Get the station name from command arguments
station_name = argv[1]
# Date we need in format DD.MM.YYYY, defaults is yesterday
for i in range(1,357):
	yesterday = date.today() - timedelta(i)
	# The page we need to scrape
	url = "http://powietrze.katowice.wios.gov.pl/dane-pomiarowe/pobierz"
	# Query parameters
	params = {
		"measType":"Auto",
		"viewType":"Station",
		"dateRange":"Day",
		"date": yesterday.strftime("%d.%m.%Y")
	}
	# Get the station we're looking for
	station = settings.STATIONS[station_name]
	# Update the query parameters with the station
	params.update( station['query'] )
	# The POST data we'll send
	body = urlencode({ 'query': json.dumps(params) })
	# Pause
	sleep(randint(1,3))
	# Sends the request 
	req = urllib2.Request(url, body)
	response = urllib2.urlopen(req)
	# Converts the response to JSON
	response_json = json.loads(response.read())
	# Parse the JSON to a CSV file
	for series in response_json["data"]["series"]:
		series_id = series["paramId"]
		for data in series["data"]:
			# Bear in mind that data[0] is a UNIX epoch timestamp
			print ','.join([ str(station_name), str(series_id), str(data[0]), str(data[1]) ])
