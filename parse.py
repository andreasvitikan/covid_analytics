#ToDo add additional functionality to check if the
#JSON file for today has been issued (13:00), and if so
#check if it exists in the data directory, and if not
#download it and use that

import json
#from time import time, strftime
import time
from datetime import date
import locale

#set the locale to romanian
locale.setlocale(locale.LC_ALL, "ro_RO.utf8")

json_file_name = "date_21_iulie_la_13_00.json"
f = open("data/" + json_file_name, "r")
latest = json.loads(f.read())
print("The JSON file imported for analysis was last updated on: ")
print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(latest['lasUpdatedOn'])))

currentDayStats = latest['currentDayStats']
print("The total number of infected today is: ")
print(currentDayStats['numberInfected'])
print("The total number of deceased today is: ")
print(currentDayStats['numberDeceased'])


