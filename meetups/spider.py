import urldb, json
from bs4 import BeautifulSoup

bootstrap = "http://google.meetup.com/all/"
html = urldb.get(bootstrap)
soup = BeautifulSoup(html)

DATA = []

def save():
    with open("data/raw.live.json",'w') as f:
        json.dump(DATA, f, indent=2)

for meetup in soup.find_all('li',{'class':'vcard'}):
    meetup_infos = {}
    DATA.append(meetup_infos)
    a = meetup.find('a')
    name = a.text
    url_group = a.attrs['href']
    print(name,url_group)
    meetup_infos['name'] = name
    meetup_infos['url'] = url_group
    urldb.get(url_group)
    all_members = []
    offset = 0
    while  True:
        url = "members/?offset={offset}&sort=join_date&desc=0"
        html = urldb.get(url_group+url.format(offset=offset))
        soup = BeautifulSoup(html)
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

        save()

        if len(members) < 20:
            break
    save()
save()