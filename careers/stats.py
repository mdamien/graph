import json
from collections import Counter

ads = json.load(open('data/parsed.json'))

def stats(arr,key):
    print()
    print("stats",key)
    print('----')

    def flat(arr):
        for x in arr:
            if type(x) == type([]):
                for y in x:
                    yield y
            else:
                yield x

    c = Counter(flat([el[key] for el in arr]))
    for el,n in c.most_common(10):
        print(n,el)
    print()

stats(ads,"team")
stats(ads,"title")
stats(ads,"type")
stats(ads,"locations")