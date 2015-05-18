import json, urldb
from bs4 import BeautifulSoup

OUT_FILE = "data/github.json"
PREFIX = "https://github.com"

def load_graph():
    graph = {}
    try:
        with open(OUT_FILE) as f:
            json.load(f)
    except:
        print(OUT_FILE,"not found")
    return graph

GRAPH = load_graph()

def scrape_org_people(orgname):
    members = []
    page = 1
    while True:
        url = "/orgs/{orgname}/people?page={page}".format(
            orgname=orgname, page=page)
        html = urldb.get(PREFIX+url)
        soup = BeautifulSoup(html)
        prev_len = len(members)
        for member in soup.find_all('div',{'class':'member-info'}):
            """
            infos = {}
            img = member.find('img')
            infos['img'] = img.attrs['src']
            infos['id'] = img.attrs['data-user']
            infos['username'] = member.find('strong').text.strip()
            full_name = member.find('span').text.strip()
            if full_name != "":
                infos['full_name'] = full_name
            """
            username = member.find('strong').text.strip()
            members.append(username)
        if len(members) == prev_len:
            break
        page += 1
    return members

def scrape_org(orgname):
    org = {
        'type':'org',
        'orgname':orgname,
    }
    org['members'] = scrape_org_people(orgname)
    return org

def scrape_user(username):
    user = {
        'type':'user',
        'username':username,
    }
    url = "/{username}".format(username=username)
    html = urldb.get(PREFIX+url)
    soup = BeautifulSoup(html)

    #user orgs
    orgs = []
    for org in soup.find_all('a',{'itemprop':'follows'}):
        orgs.append(org.attrs['aria-label'])
    user['orgs'] = orgs
    return user

def main():
    graph = []
    org = scrape_org("google")
    graph.append(org)
    for username in org['members']:
        user = scrape_user(username)
        graph.append(user)
    print(graph)

main()