import urldb, json
from bs4 import BeautifulSoup

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
    all_members = []
    offset = 0
    while  True:
        url = "members/?offset={offset}&sort=join_date&desc=0"
        html = urldb.get(url_group+url.format(offset=offset), printdot=False)
        soup = BeautifulSoup(html, "html.parser")
        members = soup.find_all(class_="memberInfo")
        for member in members:
            infos = {}
            name = member.find(class_="memName")
            infos['name'] = name.text.strip()
            infos['url'] = name.attrs['href']
            all_members.append(infos)
        offset += 20
        if len(members) < 20:
            break
    return all_members

def parse_group(html, url):
    infos = parse_group_infos(html)
    infos['members'] = fetch_group_members(url)
    infos['private'] = len(infos['members']) == 0
    infos['url'] = url
    return infos