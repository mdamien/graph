import urldb
from bs4 import BeautifulSoup

bootstrap = "http://google.meetup.com/all/"
html = urldb.get(bootstrap)
soup = BeautifulSoup(html)

for meetup in soup.find_all('li',{'class':'vcard'}):
    a = meetup.find('a')
    name = a.text
    url = a.attrs['href']
    print(name,url)
    urldb.get(url)
    urldb.get(url+"members/?offset=0&sort=name&desc=0")