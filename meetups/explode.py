import random
from pprint import pprint as pp
import json

import urldb
from parser import parse_event, parse_group

EVENT_PAGE, GROUP_PAGE, MEMBER_PAGE = range(3)

def to_explore():
	return {x.strip() for x in open('data/to_explore') if len(x.strip()) > 0]

def all_left_to_explore():
	return to_explore()-explored()

def explored():
	groups = {x['url'] for x in json.load(open('data/done/groups.json'))
	return groups

def add_group_explored(group):
	pass

def something_to_explore():
	to_explore = all_left_to_explore()
	if len(to_explore) == 0: return
	return random.choice(to_explore)

def detect_type(url):
	if '/events/' in url:
		return EVENT_PAGE
	if '/members/' in url:
		return MEMBER_PAGE
	return GROUP_PAGE

while True:
	url = something_to_explore()
	if url == None: break
	html = urldb.get(url)
	page_type = detect_type(url)
	if page_type == EVENT_PAGE:
		continue
	if page_type == GROUP_PAGE:
		group = parse_group(html, url)

	print()
	print()