import sys
import os
csv_flag = 0
if len(sys.argv) > 1:
	if sys.argv[1] == "-csv":
		csv_flag = 1

import json
if os.path.exists("data/latestData.json"):
	f = open("data/latestData.json", "r")
	latest = json.loads(f.read())
else:
	sys.exit("Nu există fișierul latestData.json!")

import datetime
latest_timestamp = datetime.datetime.fromtimestamp(latest['lasUpdatedOn'])
start_date = datetime.date.fromtimestamp(latest['lasUpdatedOn'])
day = datetime.timedelta(days = 1)

delta = datetime.datetime.now() - latest_timestamp
if delta.seconds > 24*60*60:
	os.rename("data/latestData.json", "data/latestData.json.old.{}".format(latest['lasUpdatedOn']))
	import urllib.request
	urllib.request.urlretrieve("https://datelazi.ro/latestData.json", "./latestData.json")
	print("Fișierul JSON vechi a fost redenumit, iar cel nou a fost descărcat! Rulați programul din nou!")
else:
	print("Fișierul JSON este în regulă!")

currentDayStats = latest['currentDayStats']
print("Datele au fost actualizate ultima oară: {}".format(latest['lasUpdatedOnString']))
print("Numărul total de confirmați: {}".format(currentDayStats['numberInfected']))
print("Numărul total de decese: {}".format(currentDayStats['numberDeceased']))
print("Numărul total de vindecați: {}".format(currentDayStats['numberCured']))
print()
print("Analiza datelor istorice")
print()

# Historical data analysis block

yesterday_string = (start_date - day).strftime("%Y-%m-%d")
infected_last = currentDayStats['numberInfected'] - latest['historicalData'][yesterday_string]['numberInfected']
cured_last = currentDayStats['numberCured'] - latest['historicalData'][yesterday_string]['numberCured']
deceased_last = currentDayStats['numberDeceased'] - latest['historicalData'][yesterday_string]['numberDeceased']
print("{} \tconfirmați \t{} \tdecedați \t{} \tvindecați \t{}".format(start_date.strftime("%Y-%m-%d"), infected_last, deceased_last, cured_last))

# This iterates day by day through historicalData
# and generates the numbers for each day except for
# the latest day (currentDayStats)
date_a = datetime.date.fromtimestamp(latest['lasUpdatedOn']) - day
date_b = date_a - day
end_date = datetime.date(2020, 3, 17)

while date_a > end_date:
	date_a_string = date_a.strftime("%Y-%m-%d")
	date_b_string = date_b.strftime("%Y-%m-%d")
	infected = latest['historicalData'][date_a_string]['numberInfected'] - latest['historicalData'][date_b_string]['numberInfected']
	deceased = latest['historicalData'][date_a_string]['numberDeceased'] - latest['historicalData'][date_b_string]['numberDeceased']
	cured = latest['historicalData'][date_a_string]['numberCured'] - latest['historicalData'][date_b_string]['numberCured']
	print("{} \tconfirmați \t{} \tdecedați \t{} \tvindecați \t{}".format(date_a_string, infected, deceased, cured))
	date_a = date_a - day
	date_b = date_b - day

