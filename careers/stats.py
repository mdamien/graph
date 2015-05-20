import json
from collections import Counter

ads = json.load(open('data/parsed.json'))

def stats(arr,key):
    def flat(arr):
        for x in arr:
            if type(x) == type([]):
                yield from flat(x)
            else:
                yield x.strip()

    c = Counter(flat([el[key] for el in arr]))

    count_all = len(arr)
    count_distinct = len(c)
    print()
    print(key,"   -   ",count_all,"values,",count_distinct,"distincts")
    print('----')

    for el,n in c.most_common(10):
        p = n/count_all*100
        print("{:.1f}% ({}) {}".format(p,n,el))
    print()

stats(ads,"teams")
stats(ads,"title")
stats(ads,"level")
stats(ads,"type")
stats(ads,"locations")
