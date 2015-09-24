import urldb, json
from bs4 import BeautifulSoup

from pprint import pprint as pp

def parse_group_infos(html):
    h = BeautifulSoup(html[0], 'html.parser')
    interresting_keys = ('description','locality','country-name', \
        'region','title','postal-code','latitude','longitude','image', 'placename')
    meetup_infos = {}
    soup = BeautifulSoup(html, "html.parser")
    metas = soup.find_all('meta')
    for meta in metas:
        keyname = 'name' if 'name' in meta.attrs else 'property'
        if keyname in meta.attrs:
            key = meta.attrs[keyname]
            key = key.replace('og:','').replace('geo.','')
            if key in interresting_keys:
                value = meta.attrs['content']
                if 'itude' in key:
                    value = float(value)
                meetup_infos[key] = value
    return meetup_infos

def fetch_group_members(url_group):
    all_members = set()
    offset = 0
    while  True:
        url = "members/?offset={offset}&sort=join_date&desc=0"
        html = urldb.get(url_group+url.format(offset=offset))
        soup = BeautifulSoup(html, "html.parser")
        members = soup.find_all(class_="memberInfo")
        prev_uniq_url = len(all_members)
        for member in members:
            infos = {}
            name = member.find(class_="memName")
            #infos['name'] = name.text.strip()
            all_members.add(name.attrs['href'])
        offset += 20
        print(len(all_members),'=>',len(all_members))
        if len(all_members) <= prev_uniq_url:
            break
    return list(all_members)

def fetch_event_list(url_group):
    url = "{group_url}events/past/?page={page}&__fragment=centerColMeetupList"
    page = 0
    events = set()
    while True:
        r = urldb.get(url.format(page=page, group_url=url_group))
        j = json.loads(r)
        h = BeautifulSoup(j[0], 'html.parser')
        a = h.find_all(class_='event-title')
        print(len(a))
        if len(a) == 0:
            break
        for el in a:
            events.add(el.attrs['href'])
        page += 1
    return list(events)

def parse_group(html, url):
    infos = parse_group_infos(html)
    infos['members'] = fetch_group_members(url)
    infos['private'] = len(infos['members']) == 0
    if not infos['private']:
        infos['events'] = fetch_event_list(url)
    infos['url'] = url
    return infos

if __name__ == '__main__':
    html = open('examples/group.html').read()
    url = 'http://www.meetup.com/fr/DC-French/'
    group = parse_group(html, url)
    pp(group)