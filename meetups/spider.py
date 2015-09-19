import urldb, json
from bs4 import BeautifulSoup

bootstrap = "http://google.meetup.com/all/"
html = urldb.get(bootstrap)
soup = BeautifulSoup(html, "html.parser")

DATA = []

def save():
    with open("data/raw.live.json",'w') as f:
        json.dump(DATA, f, indent=2)

def parse_group(html):
    interresting_keys = ('description','locality','country-name', \
        'region','postal-code','latitude','longitude','image', 'placename')
    meetup_infos = {}
    soup = BeautifulSoup(html, "html.parser")
    metas = soup.find_all('meta')
    print('\n'.join(list(map(str,metas))))

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

groups = soup.find_all('li',{'class':'vcard'})
for i, meetup in enumerate(groups):
    print('group',i,'/',len(groups))
    
    a = meetup.find('a')
    name = a.text
    url_group = a.attrs['href']
    
    group_html = urldb.get(url_group)
    meetup_infos = parse_group(group_html)
    meetup_infos['name'] = name
    meetup_infos['url'] = url_group
    DATA.append(meetup_infos)

    all_members = []
    offset = 0
    while  True:
        url = "members/?offset={offset}&sort=join_date&desc=0"
        html = urldb.get(url_group+url.format(offset=offset))
        soup = BeautifulSoup(html, "html.parser")
        members = soup.find_all(class_="memberInfo")
        members_infos = []
        for member in members:
            infos = {}
            name = member.find(class_="memName")
            infos['name'] = name.text.strip()
            infos['url'] = name.attrs['href']
            print(infos)
            members_infos.append(infos)
        all_members.append(members_infos)
        offset += 20

        meetup_infos['all_members'] = all_members

    
        if len(members) < 20:
            break
    save()
save()