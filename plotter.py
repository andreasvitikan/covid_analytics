import csv

dates = []
positives = []

with open('latestData.csv', 'r', newline='') as csvfile:
	reader = csv.DictReader(csvfile)
	for row in reader:
		dates.append(row['date'])
		positives.append(row['numberInfected'])


import matplotlib.pyplot as plt
plt.plot(dates, positives)
plt.show()