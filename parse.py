import sys
import os
import json
import csv
import datetime
import urllib.request

if os.path.exists("data/latestData.json"):
	f = open("data/latestData.json", "r")
	latest = json.loads(f.read())
	f.close()
else:
	sys.exit("Nu există fișierul latestData.json!")

latest_timestamp = datetime.datetime.fromtimestamp(latest['lasUpdatedOn'])
start_date = datetime.date.fromtimestamp(latest['lasUpdatedOn'])
day = datetime.timedelta(days = 1)

delta = datetime.datetime.now() - latest_timestamp
if delta > day:
	os.rename("data/latestData.json", "data/latestData.json.old.{}".format(start_date.strftime("%Y-%m-%d")))
	urllib.request.urlretrieve("https://datelazi.ro/latestData.json", "data/latestData.json")
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

print("Situația pe județe")
for key in latest['historicalData'][yesterday_string]['countyInfectionsNumbers'].keys():
	value = currentDayStats['countyInfectionsNumbers'][key] - latest['historicalData'][yesterday_string]['countyInfectionsNumbers'][key]
	print("Județul {} confirmați {}".format(key, value))


import csv
csvfile = open('data/latestData.csv', 'w', newline='')
writer = csv.writer(csvfile)

# This is the header for the exported CSV file (serves as header when importing the CSV into other programs)
# This is NOT the optimal place/way to do it - will fix this later
writer.writerow(['date', 'confirmed', 'deceased', 'cured'])

# Write today's data into the CSV file (it is stored separately in the JSON as currentDayStats
writer.writerow([start_date.strftime("%Y-%m-%d"), infected_last, deceased_last, cured_last])

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
	
	writer.writerow([date_a_string, infected, deceased, cured])	
	
	date_a = date_a - day
	date_b = date_b - day

infected = latest['historicalData'][date_b_string]['numberInfected']
deceased = latest['historicalData'][date_b_string]['numberDeceased']
cured = latest['historicalData'][date_b_string]['numberCured']
print("{} \tconfirmați \t{} \tdecedați \t{} \tvindecați \t{}".format(date_b_string, infected, deceased, cured))
writer.writerow([date_b_string, infected, deceased, cured])

print()
print("Gata!")

