# This is a temporary working file
# This is NOT meant to executed!
# This file will contain code snippets removed from the parse.py file

# Historical data analysis block

yesterday_string = (start_date - day).strftime("%Y-%m-%d")
infected_last = currentDayStats['numberInfected'] - latest['historicalData'][yesterday_string]['numberInfected']
cured_last = currentDayStats['numberCured'] - latest['historicalData'][yesterday_string]['numberCured']
deceased_last = currentDayStats['numberDeceased'] - latest['historicalData'][yesterday_string]['numberDeceased']
print("{} \tconfirmați \t{} \tdecedați \t{} \tvindecați \t{}".format(start_date.strftime("%Y-%m-%d"), infected_last, deceased_last, cured_last))

for key in latest['historicalData'][yesterday_string]['countyInfectionsNumbers'].keys():
	value = currentDayStats['countyInfectionsNumbers'][key] - latest['historicalData'][yesterday_string]['countyInfectionsNumbers'][key]
	print("Județul {} confirmați {}".format(key, value))


import csv
csvfile = open('data/latestData.csv', 'w', newline='')
writer = csv.writer(csvfile)

# This is the header for the exported CSV file (serves as header when importing the CSV into other programs)
# This is NOT the optimal place/way to do it - will fix this later
csvfile_header = ['date', 'confirmed', 'deceased', 'cured']

for key in latest['historicalData'][yesterday_string]['countyInfectionsNumbers'].keys():
	csvfile_header.append(key)

writer.writerow(csvfile_header)

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
