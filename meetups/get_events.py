import urldb, json
from bs4 import BeautifulSoup

groups = json.load(open('data/raw.live.json'))

url = "{group_url}events/past/?page={page}&__fragment=centerColMeetupList"

group_events = {}

def save():
    with open("data/events.live.json",'w') as f:
        json.dump(group_events, f, indent=2)

for group in groups:
	page = 0
	events = []
	while True:
		r = urldb.get(url.format(page=page, group_url=group['url']))
		j = json.loads(r)
		h = BeautifulSoup(j[0], 'html.parser')
		a = h.find_all(class_='event-title')
		print(len(a))
		if len(a) == 0:
			break
		for el in a:
			infos = {
				'url': el.attrs['href'],
				'title': el.text.strip()
			}
			events.append(infos)
		page += 1
	group_events[group['url']] = events
	save()