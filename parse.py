import json
f = open("data/latestData.json", "r")
latest = json.loads(f.read())

import datetime
latest_timestamp = datetime.datetime.fromtimestamp(latest['lasUpdatedOn'])
delta = datetime.datetime.now() - latest_timestamp
if delta.seconds > 24*60*60:
	import urllib.request
	urllib.request.urlretrieve("https://datelazi.ro/latestData.json", "./latestData.json")
else:
	print("Fișierul JSON este în regulă!")

currentDayStats = latest['currentDayStats']
print("Datele au fost actualizate ultima oară: {}".format(latest['lasUpdatedOnString']))
print("Numărul total de infectați: {}".format(currentDayStats['numberInfected']))
print("Numărul total de decese: {}".format(currentDayStats['numberDeceased']))
print("Numărul total de vindecați: {}".format(currentDayStats['numberCured']))

