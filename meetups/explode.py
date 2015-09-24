import random
from pprint import pprint as pp
import json
from itertools import chain

import urldb
from parser import parse_event, parse_group

EVENT_PAGE, GROUP_PAGE, MEMBER_PAGE = range(3)

def to_explore():
	return {x.strip() for x in open('data/to_explore') if len(x.strip()) > 0}

def all_left_to_explore():
	return to_explore()-explored_urls()

def explored_urls():
	return {x['url'] for x in chain(explored_groups(), explored_events())}

def explored_groups():
	return json.load(open('data/done/groups.json'))

def explored_events():
	return json.load(open('data/done/events.json'))

def add_event_explored(event):
	new = explored_events() + [event]
	json.dump(new, open('data/done/events.json','w'), indent=2)
	json.dump(new, open('data/done/events.bkp.json','w'), indent=2)

def add_group_explored(group):
	new = explored_groups() + [group]
	json.dump(new, open('data/done/groups.json','w'), indent=2)
	json.dump(new, open('data/done/groups.bkp.json','w'), indent=2)

def something_to_explore():
	to_explore = all_left_to_explore()
	if len(to_explore) == 0: return
	return random.choice(list(to_explore))

def detect_type(url):
	if '/events/' in url:
		return EVENT_PAGE
	if '/members/' in url:
		return MEMBER_PAGE
	return GROUP_PAGE


if __name__ == "__main__":
	while True:
		url = something_to_explore()
		if url == None: break
		try:
			html = urldb.get(url)
		except Exception as e:
			print('error:',e)
			continue
		page_type = detect_type(url)
		if page_type == EVENT_PAGE:
			event = parse_event(html, url)
			add_event_explored(event)
		if page_type == GROUP_PAGE:
			group = parse_group(html, url)
			add_group_explored(group)

		print()
		print()
		print(len(explored_groups()),'groups',len(explored_events()),'events')
		print()