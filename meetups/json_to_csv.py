import json, csv, sys

inputfile = sys.argv[1]
outputfile = sys.argv[2]

data = json.load(open(inputfile))
keys = {}
for el in data:
	keys |= el.keys()
keys = sorted(list(keys))

csv_data = [keys]+[[el.get(k) for k in keys] for el in data]

with open(outputfile, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(csv_data)