import json
from collections import Counter

ads = json.load(open('data/parsed.json'))

def stats(arr,key):
    def flat(arr):
        for x in arr:
            if type(x) == type([]):
                for y in x:
                    yield y
            else:
                yield x

    c = Counter(flat([el[key] for el in arr]))

    count_all = len(arr)
    count_distinct = len(c)
    print()
    print("stats",key,"   -   ",count_all,"values,",count_distinct,"distincts")
    print('----')

    for el,n in c.most_common(10):
        p = n/count_all*100
        ps = "({:.1f}%)".format(p)
        print(n,ps,el)
    print()

stats(ads,"team")
stats(ads,"title")
stats(ads,"type")
stats(ads,"locations")