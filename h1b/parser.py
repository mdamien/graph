from bs4 import BeautifulSoup 
import os, json
from pprint import pprint as pp

data = []

with open("data/raw.html") as f:
    soup = BeautifulSoup(f)
    trs = soup.find_all("tr")
    for i,tr in enumerate(trs[1:]):
        tds = tr.find_all('td')
        row = {}
        row['title'] = tds[1].text
        row['salary'] = int(tds[2].text.replace(',',''))
        row['location'] = tds[3].text
        row['submit_date'] = tds[4].text
        row['start_date'] = tds[5].text
        row['case_status'] = tds[6].text
        data.append(row)

with open('data/parsed.json','w') as f:
    json.dump(data,f,indent=2)