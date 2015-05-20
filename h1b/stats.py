import json
from collections import Counter

ads = json.load(open('data/parsed.json'))

def stats(arr,key,keygetter=lambda el, key:el[key]):
    def flat(arr):
        for x in arr:
            if type(x) == type([]):
                yield from flat(x)
            else:
                x = str(x)
                yield x.strip()

    c = Counter(flat([keygetter(el,key) for el in arr]))

    count_all = len(arr)
    count_distinct = len(c)
    print()
    print(key,"   -   ",count_all,"values,",count_distinct,"distincts")
    print('----')

    for el,n in c.most_common(10):
        p = n/count_all*100
        print("{:.1f}% ({}) {}".format(p,n,el))
    print()

stats(ads,"case_status")
stats(ads,"title")
stats(ads,"location")
stats(ads,"salary")
stats(ads,"submit_month",lambda el,key:el["submit_date"].split('/')[0])
stats(ads,"start_month",lambda el,key:el["start_date"].split('/')[0])

