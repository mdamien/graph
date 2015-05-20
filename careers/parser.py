from bs4 import BeautifulSoup 
import os, json
from pprint import pprint as pp

data = []

ids = set()

for root, dirs, files in os.walk("PAGES/"):
    files = list(files)
    for i, name in enumerate(files):
        ad = {}
        filename = os.path.join(root, name)
        ad['filename'] = filename
        with open(filename) as f:
            soup = BeautifulSoup(f)
            ad['title'] = soup.title.text
            container = soup.find(class_="detail-a")
            if container == None:
                print('bad file',filename)
                continue
            title = container.find("a")
            ad['id'] = int(container.attrs['id'])
            if ad['id'] in ids:
                continue
            ids.add(ad['id'])

            for div in soup.find_all(class_='detail-content'):
                info = div.find(class_='info-text')
                if info:
                    divs = list(div.find_all('div', recursive=False))

                    get = lambda x:x.find(class_='info-text').text.strip()

                    ad['teams'] = get(divs[0]).split(';')
                    ad['type'] = get(divs[1])
                    ad['level'] = get(divs[2])
                    #ad['salary'] = get(divs[3])
                    ad['last_updated'] = get(divs[4])
                    ad['locations'] = get(divs[5]).split(';')
            ad['text'] = container.find_all(class_='detail-item')[2].text
        data.append(ad)
        if i % 10 == 0:
            print(i,"/",len(files))

with open('data/parsed.json','w') as f:
    json.dump(data,f,indent=2)