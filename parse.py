import json
f = open("data/latestData.json", "r")
latest = json.loads(f.read())

import datetime
latest_timestamp = datetime.datetime.fromtimestamp(latest['lasUpdatedOn'])
delta = datetime.datetime.now() - latest_timestamp
if delta.seconds > 24*60*60:
	import os
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

# iterating through the last 7 days
interval = datetime.timedelta(days = 1)
date_a = datetime.date.today() - interval
date_b = date_a - interval
end_date = datetime.date(2020, 3, 17)

while date_a > end_date:
	date_a_string = date_a.strftime("%Y-%m-%d")
	date_b_string = date_b.strftime("%Y-%m-%d")
	infected = latest['historicalData'][date_a_string]['numberInfected'] - latest['historicalData'][date_b_string]['numberInfected']
	deceased = latest['historicalData'][date_a_string]['numberDeceased'] - latest['historicalData'][date_b_string]['numberDeceased']
	cured = latest['historicalData'][date_a_string]['numberCured'] - latest['historicalData'][date_b_string]['numberCured']
	print("{} \tconfirmați \t{} \tdecedați \t{} \tvindecați \t{}".format(date_a_string, infected, deceased, cured))
	date_a = date_a - interval
	date_b = date_b - interval

