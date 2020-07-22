import sys
import os
import json
import csv
import datetime
import urllib.request

date_format = "%Y-%m-%d"
root_values = ['numberInfected', 'numberCured', 'numberDeceased']
last_date = datetime.datetime(2020, 4, 3)

# Note: the first day recorded is 17-03-2020
# Note: the first day with county information is 02-04-2020
# Note: the countyInfectionsNumbers did NOT include the - key from the beginning

if os.path.exists("data/latestData.json"):
	f = open("data/latestData.json", "r")
	latest = json.loads(f.read())
	f.close()
else:
	sys.exit("Nu există fișierul latestData.json!")

# latest is the json structure read from the latestData.json
# latest_timestamp is a datetime object representing when the imported JSON was last updated
# latest_timestamp_string is a string that contains the POSIX epoch time when the JSON was last updated
# day is a datetime interval representing 1 day (24 hours) that is frequently used

latest_timestamp_string = latest['lasUpdatedOn']
latest_timestamp = datetime.datetime.fromtimestamp(latest['lasUpdatedOn'])
day = datetime.timedelta(days = 1)


# if the timestamp associated with the JSON file is older than 1 day - redownload the JSON file and exit
# ToDo: do a head request at datelazi.ro/latestData.json and check the Last-Modified header

delta = datetime.datetime.now() - latest_timestamp
if delta > day:
	os.rename("data/latestData.json", "data/latestData.json.old.{}".format(start_date.strftime("%Y-%m-%d")))
	urllib.request.urlretrieve("https://datelazi.ro/latestData.json", "data/latestData.json")
	sys.exit("Fișierul JSON vechi a fost redenumit, iar cel nou a fost descărcat! Rulați programul din nou!")
else:
	print("Fișierul JSON este în regulă!")

# Generating the file header with all of the column names
# The first 4 columns are hard-coded, the date is the key for the historicalData in the JSON file
# And the numberInfected, numberCured and numberDeceased fields share the same name with the JSON file

csvfile_header = ['date']
for key in root_values:
	csvfile_header.append(key)

for key in latest['currentDayStats']['distributionByAge'].keys():
	if key.find("procesare") == -1:
		csvfile_header.append("age{}".format(key))

for key in latest['currentDayStats']['countyInfectionsNumbers'].keys():
	if key.find("-") == -1:
		csvfile_header.append("county{}".format(key))

csvfile = open("data/latestData.csv", 'w', newline='')
writer = csv.writer(csvfile)
writer.writerow(csvfile_header)

# Time to generate the actual values to be written in the CSV file
# These will be generated in 3 blocks:
# Block 1: the data for the present day which is based on currentDayStats ("today")
# and the last day recorded in historicalData ("yesterday")
# Block 2: The historicalData which is done integrally based on consecutive entries
# in historicalData
# Block 3: The numbers for the first day on record (2020-03-17) which are NOT correct
# but are written in such a way that the totals obtained are correct

# !-------!
# |Block 1|
# !-------!
csvfile_row = []

# Add the date for the last day on record
csvfile_row.append(latest_timestamp.strftime(date_format))

# Compute the 3 root values for the last day on record and add them
previous_day = latest_timestamp - day
previous_day_string = previous_day.strftime(date_format)
for key in root_values:
	csvfile_row.append(latest['currentDayStats'][key] - latest['historicalData'][previous_day_string][key])

# Compute the distributionByAge values
for key in latest['currentDayStats']['distributionByAge'].keys():
	if key.find("procesare") == -1:
		csvfile_row.append(latest['currentDayStats']['distributionByAge'][key] - latest['historicalData'][previous_day_string]['distributionByAge'][key])

# Compute the countyInfectionsNumbers values
for key in latest['currentDayStats']['countyInfectionsNumbers'].keys():
	if key.find("-") == -1:
		csvfile_row.append(latest['currentDayStats']['countyInfectionsNumbers'][key] - latest['historicalData'][previous_day_string]['countyInfectionsNumbers'][key])

# Write the first row of values (second real row) to csv file
writer.writerow(csvfile_row)

# !-------!
# |Block 2|
# !-------!
csvfile_row = []

# This iterates through all the days in historicalData
current_day = latest_timestamp - day
while current_day > last_date:
	csvfile_row = []
	current_day_string = current_day.strftime(date_format)
	previous_day_string = (current_day - day).strftime(date_format)
	# This while loop steps through all of the day keys in historicalData
	# There will be 3 subsections in this while loop, keeping the structure of Block 1
	# First, writing the current date
	csvfile_row.append(current_day.strftime(date_format))
	
	# Then, write the root values (3 keys)
	for key in root_values:
		csvfile_row.append(latest['historicalData'][current_day_string][key] - latest['historicalData'][previous_day_string][key])
	
	# Compute the distributionByAge values
	for key in latest['historicalData'][current_day_string]['distributionByAge'].keys():
		if key.find("procesare") == -1:
			csvfile_row.append(latest['historicalData'][current_day_string]['distributionByAge'][key] - latest['historicalData'][previous_day_string]['distributionByAge'][key])
	
	# Compute the countyInfectionsNumbers values
	for key in latest['historicalData'][current_day_string]['countyInfectionsNumbers'].keys():
		if key.find("-") == -1:
			csvfile_row.append(latest['historicalData'][current_day_string]['countyInfectionsNumbers'][key] - latest['historicalData'][previous_day_string]['countyInfectionsNumbers'][key])
	
	writer.writerow(csvfile_row)
	
	current_day = current_day - day

csvfile.close()