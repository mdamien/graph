import json, spider,random

graph = spider.load_graph()

nodes_added = set()
nodes = []
edges_added = set()
edges = []

def add_edge(orgname, username):
    if orgname not in nodes_added:
        node = {
            'label':orgname,
            'id':orgname,
            'color':'rgb(200,20,20)',
            'x':random.random()*40-20,
            'y':random.random()*40-20,
            'size':3,
        }
        nodes.append(node)
        nodes_added.add(orgname)

    if username not in nodes_added:
        node = {
            'label':username,
            'id':username,
            'color':'rgb(20,20,200)',
            'x':random.random()*100-50,
            'y':random.random()*100-50,
            'size':1,
        }
        nodes.append(node)
        nodes_added.add(username)

    edgename = username+"-"+orgname
    if edgename not in edges_added:
        edge = {
            "id": edgename,
            "source": username,
            "target": orgname,
        }
        edges.append(edge)
        edges_added.add(edgename)


for i, el in enumerate(graph):
    if el['type'] == 'org':
        for member in el['members']:
            add_edge(el['orgname'], member)
    if el['type'] == 'user':
        for org in el['orgs']:
            add_edge(org, el['username'])

    if i > 100:
        break

print(len(edges),"edges")
print(len(nodes),"nodes")

with open('data/graph.json','w') as f:
    json.dump({
            'nodes':nodes,
            'edges':edges
        }, f, indent=2)