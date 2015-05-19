import json, urldb
from bs4 import BeautifulSoup

PREFIX = "https://github.com"
OUT_FILE = 'data/raw.json'

def load_graph():
    graph = []
    try:
        with open(OUT_FILE) as f:
            graph = json.load(f)
    except:
        print(OUT_FILE,"not found")
    return graph

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

def orgs(graph):
    return set([x['orgname'] for x in graph
            if x['type'] == "org"])

def users(graph):
    return set([x['username'] for x in graph
            if x['type'] == "user"])

def users_orgs(graph):
    orgs = [x['orgs'] for x in graph if x['type'] == "user"]
    return set(sum(orgs,[]))

def orgs_users(graph):
    users = [x['members'] for x in graph if x['type'] == "org"]
    return set(sum(users,[]))


def save_graph(graph):
    with open(OUT_FILE,'w') as f:
        json.dump(graph,f,indent=2)
    with open(OUT_FILE+".cold",'w') as f:
        json.dump(graph,f,indent=2)

def bootstrap():
    graph = []
    org = scrape_org("google")
    graph.append(org)
    for username in org['members']:
        user = scrape_user(username)
        graph.append(user)
    
    with open(OUT_FILE,'w') as f:
        json.dump(graph,f,indent=2)

def main():
    graph = load_graph()
    print(users_orgs(graph))
    orgs_to_scrape = users_orgs(graph)-orgs(graph)
    for orgname in orgs_to_scrape:
        try:
            org = scrape_org(orgname)
            graph.append(org)
            save_graph(graph)
            print(len(graph))
        except Exception as e:
            print('skip',orgname,e)

    user_to_scrape = orgs_users(graph)-users(graph)
    for username in user_to_scrape:
        try:
            user = scrape_user(username)
            graph.append(user)
            save_graph(graph)
            print(len(graph))
        except Exception as e:
            print('skip',orgname,e)

if __name__ == "__main__":
    main()
