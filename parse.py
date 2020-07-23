#! python

import sys
import os
import json
import csv
import datetime
import urllib.request
import requests

# Correct setting of the working directory in case the script
# is not called from the directory where it is located
real_path = os.path.realpath(__file__)
os.chdir(real_path[:real_path.index("parse.py")])

# The URL for the datelazi.ro JSON file
url_json = "https://datelazi.ro/latestData.json"

date_format = "%Y-%m-%d"
root_values = ['numberInfected', 'numberCured', 'numberDeceased']
last_date_county = datetime.date(2020, 4, 3)
last_date = datetime.date(2020, 3, 17)
last_modified = ""

http_response = requests.head(url_json)

# Note: the first day recorded is 17-03-2020
# Note: the first day with county information is 03-04-2020
# Note: the countyInfectionsNumbers did NOT include the - key from the beginning
# Note: nor did the distributionByAge contain the wonderful "in procesare" key with the mis-rendering...

# This is in case either the data directory, the data/latestData.json or the data/Last-Modified.head
# files do not exist. This will create the timestamp file, download the latest JSON and create
# the directory if necessary.

if not (os.path.exists("data/latestData.json") and os.path.exists("data/Last-Modified.head")):
	print("Nu există fișierul latestData.json sau fișierul Last-Modified.head !")
	# Thanks https://github.com/mcmarius/
	os.makedirs("data/", exist_ok = True)
	urllib.request.urlretrieve(url_json, "data/latestData.json")
	with open('data/Last-Modified.head', 'w') as f:
		f.write(http_response.headers['Last-Modified'])

# Once we are sure that files exist, it's time to check the timestamp
# if the files stored locally are the right version.
# if the locally stored timestamp of the JSON file does not match the timestamp
# return by the HEAD request via the Last-Modified field, redownload the JSON file

with open('data/Last-Modified.head', 'r') as f:
	last_modified = f.read()

if last_modified == http_response.headers['Last-Modified']:
	print("Fișierul JSON este ultima variantă!")
else:
	os.rename("data/latestData.json", "data/latestData.json.old.{}".format(datetime.date.today().strftime("%Y-%m-%d")))
	urllib.request.urlretrieve(url_json, "data/latestData.json")
	with open('data/Last-Modified.head', 'w') as f:
		f.write(http_response.headers['Last-Modified'])

# At this point, the latestData.json file definitely exists
# and is definitely the right version!
# The Narrator is thankful there are no more restarts...

with open('data/latestData.json', 'r') as f:
	latest = json.loads(f.read())

# latest is the json structure read from the latestData.json
# latest_timestamp is a datetime object representing when the imported JSON was last updated
# day is a datetime interval representing 1 day (24 hours) that is frequently used

latest_timestamp = datetime.date.fromtimestamp(latest['lasUpdatedOn'])
day = datetime.timedelta(days = 1)

# Generating the file header with all of the column names
# The first 4 columns are hard-coded, the date is the key for the historicalData in the JSON file
# And the numberInfected, numberCured and numberDeceased fields share the same name with the JSON file

# Generate the CSV header
csvfile_header = ['dayNumber', 'date']
for key in root_values:
	csvfile_header.append(key)

for key in latest['currentDayStats']['distributionByAge'].keys():
	if key.find("procesare") == -1:
		csvfile_header.append("age{}".format(key))

for key in latest['currentDayStats']['countyInfectionsNumbers'].keys():
	if key.find("-") == -1:
		csvfile_header.append("county{}".format(key))

# Begin writing CSV file
csvfile = open("data/latestData.csv", 'w', newline='')
writer = csv.DictWriter(csvfile, csvfile_header)
writer.writeheader()

# Time to generate the actual values to be written in the CSV file
# These will be generated in 3 blocks:
# Block 1: the data for the present day which is based on currentDayStats ("today")
# and the last day recorded in historicalData ("yesterday")
# Block 2: The historicalData which is done integrally based on consecutive entries
# in historicalData
# Block 3: Padding the last day in historicalData with wrong values so that the totals
# are correct when summed to the present day

# !-------!
# |Block 1|
# !-------!

csvfile_row = {}

# Add the date for the last day on record
csvfile_row['dayNumber'] = (latest_timestamp - last_date).days + 1
csvfile_row['date'] = latest_timestamp.strftime(date_format)

# Compute the 3 root values for the last day on record and add them
previous_day = latest_timestamp - day
previous_day_string = previous_day.strftime(date_format)
for key in root_values:
	csvfile_row[key] = latest['currentDayStats'][key] - latest['historicalData'][previous_day_string][key]

# Compute the distributionByAge values
for key in latest['currentDayStats']['distributionByAge'].keys():
	if key.find("procesare") == -1:
		csvfile_row['age{}'.format(key)] = latest['currentDayStats']['distributionByAge'][key] - latest['historicalData'][previous_day_string]['distributionByAge'][key]

# Compute the countyInfectionsNumbers values
for key in latest['currentDayStats']['countyInfectionsNumbers'].keys():
	if key.find("-") == -1:
		csvfile_row['county{}'.format(key)] = latest['currentDayStats']['countyInfectionsNumbers'][key] - latest['historicalData'][previous_day_string]['countyInfectionsNumbers'][key]

# Write the first row of values (second real row) to csv file
writer.writerow(csvfile_row)

# !-------!
# |Block 2|
# !-------!
csvfile_row = {}

# This iterates through all the days in historicalData
current_day = latest_timestamp - day
while current_day > last_date:
	csvfile_row = {}
	current_day_string = current_day.strftime(date_format)
	previous_day_string = (current_day - day).strftime(date_format)
	
	# This while loop steps through all of the day keys in historicalData
	# There will be 3 subsections in this while loop, keeping the structure of Block 1
	# First, writing the current date
	#csvfile_row.append(current_day.strftime(date_format))
	csvfile_row['dayNumber'] = (current_day - last_date).days + 1
	csvfile_row['date'] = current_day.strftime(date_format)
	
	# Then, write the root values (3 keys)
	for key in root_values:
		csvfile_row[key] = latest['historicalData'][current_day_string][key] - latest['historicalData'][previous_day_string][key]
	
	# Compute the distributionByAge values
	for key in latest['historicalData'][current_day_string]['distributionByAge'].keys():
		if key.find("procesare") == -1:
			csvfile_row["age{}".format(key)] = latest['historicalData'][current_day_string]['distributionByAge'][key] - latest['historicalData'][previous_day_string]['distributionByAge'][key]
	
	# Compute the countyInfectionsNumbers values
	# These values are missing before April 3rd, so just pad the CSV file with 0's
	if current_day > last_date_county:
		for key in latest['historicalData'][current_day_string]['countyInfectionsNumbers'].keys():
			if key.find("-") == -1:
				csvfile_row["county{}".format(key)] = latest['historicalData'][current_day_string]['countyInfectionsNumbers'][key] - latest['historicalData'][previous_day_string]['countyInfectionsNumbers'][key]
	else:
		for key in latest['currentDayStats']['countyInfectionsNumbers'].keys():
			if key.find("-") == -1:
				csvfile_row["county{}".format(key)] = 0
	
	writer.writerow(csvfile_row)
	
	current_day = current_day - day

# !-------!
# |Block 3|
# !-------!

# Block 3 handles exclusively the last day in the historicalData set

csvfile_row = {}

current_day_string = current_day.strftime(date_format)
csvfile_row['dayNumber'] = (current_day - last_date).days + 1
csvfile_row['date'] = current_day_string

for key in root_values:
	csvfile_row[key] = latest['historicalData'][current_day_string][key]

for key in latest['historicalData'][current_day_string]['distributionByAge'].keys():
	if key.find("procesare") == -1:
		csvfile_row["age{}".format(key)] = latest['historicalData'][current_day_string]['distributionByAge'][key]

for key in latest['currentDayStats']['countyInfectionsNumbers'].keys():
	if key.find("-") == -1:
		csvfile_row["county{}".format(key)] = 0

writer.writerow(csvfile_row)

csvfile.close()