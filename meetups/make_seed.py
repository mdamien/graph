import json

import explode

comming = json.load(open('data/events_coming.json'))
seed = {x['url'] for x in comming}
seed = seed - explode.explored_urls()
groups = explode.explored_groups()
for group in groups:
	seed |= set(group.get('events',{})
	seed |= set(group.get('members',{})
events = explode.explored_events()
for event in events:
	seed.add(event['url'].split('events/')[0])
	seed |= set(group.get('attendees',{})
	seed |= set(group.get('nogo',{})
for x in seed:print(x)