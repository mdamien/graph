import urldb, json
from bs4 import BeautifulSoup
from pprint import pprint as pp

url = "http://www.meetup.com/find/events/?pageToken=225320454%7C2015-09-19T04%3A00%3A00.000-04%3A00%7C{offset}%7CFORWARD&allMeetups=true&keywords=&radius=Infinity&userFreeform=Palo+Alto%2C+CA&mcId=z94303&mcName=Palo+Alto%2C+CA&sort=recommended&eventFilter=all&__fragment=simple_search&op=&on_home=true"

DATA = []

def save():
    with open("data/events_coming.json",'w') as f:
        json.dump(DATA, f, indent=2)

offset = 0
while True:
	html = json.loads(urldb.get(url.format(offset=offset)))[0]
	soup = BeautifulSoup(html,'html.parser')
	events = soup.find_all(class_='event-listing')
	print(offset,':',len(events))
	for e in events:
		infos = {}
		event_link = e.find(class_='event-title')
		infos['title'] = event_link.text.strip()
		infos['url'] = event_link.attrs['href']
		infos['attendees_count'] = int(e.find(class_='attendee-count').text.strip().split()[0])
		group_link = e.find(class_='chapter-name')
		infos['group_name'] = group_link.text.strip()
		infos['group_url'] = group_link.attrs['href']
		infos['start'] = e.find('time').attrs['datetime']
		DATA.append(infos)
	if len(events) == 0:
		break
	offset += 100
	save()
