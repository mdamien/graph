import json
comming = json.load(open('data/events_coming.json'))
seed = [x['url'] for x in comming]
for x in seed:print(x)