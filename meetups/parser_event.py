from pprint import pprint as pp
from itertools import chain
import urldb, json
from bs4 import BeautifulSoup

def parse_infos(html):
    h = BeautifulSoup(html[0], 'html.parser')
    interresting_keys = ('description','locality','country-name', 'name', \
        'region','title','postal-code','latitude','longitude','image', 'placename')
    infos = {}
    soup = BeautifulSoup(html, "html.parser")
    els = chain(soup.find_all('meta'), soup.find_all('div'), soup.find_all('h1'))
    for el in els:
        keyname = 'name'
        keyname = keyname if keyname in el.attrs else 'property'
        keyname = keyname if keyname in el.attrs else 'itemprop'
        if keyname in el.attrs:
            key = el.attrs[keyname]
            #print('*  found', keyname, key)
            key = key.replace('og:','').replace('geo.','')
            if key in interresting_keys:
                if 'content' in el.attrs:
                    value = el.attrs['content']
                    if 'itude' in key:
                        value = float(value)
                else:
                    value = el.text.strip()
                #print('     add', key, value)
                infos[key] = value

    attendees = soup.find('ul',{'id':'rsvp-list'})
    if attendees:
        attendees = attendees.find_all(class_='member-name')
        infos['attendees'] = [x.find('a').attrs['href'] for x in attendees]

    nogo = soup.find('div',{'id':'no-list'})
    if nogo:
        nogo = nogo.find_all(class_='member-name')
        infos['nogo'] = [x.find('a').attrs['href'] for x in nogo]

    return infos

def parse_event(html, url):
    infos = parse_infos(html)
    infos['url'] = url
    return infos

if __name__ == '__main__':
    html = open('examples/event.html').read()
    url = 'http://www.meetup.com/fr/Arizona-Backpacking/events/225427943/'
    event = parse_event(html, url)
    pp(event)