import json
f = open("date_21_iulie_la_13_00.json", "r")
latest = json.loads(f.read())
print(latest['lasUpdatedOn'])

