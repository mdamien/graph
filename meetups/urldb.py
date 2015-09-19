"""
Cache GET requests in the file system
"""
import requests, unicodedata, re, os.path

DIR = "HTML"

headers = """
Connection: keep-alive
Cache-Control: max-age=0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36
Accept-Encoding: gzip, deflate, sdch
Accept-Language: en-US,en;q=0.8,fr;q=0.6
Cookie: __cfduid=d70b96ee51d4e17a8348c17d33cf6c7cb1442376062; MEETUP_AFFIL="affil=meetup"; MEETUP_CSRF=33f76b8b-b712-4047-994f-ceb83d209b2f; MEETUP_MEMBER="id=192793723&status=1&timestamp=1442377403&bs=0&tz=US%2FPacific&zip=94303&country=us&city=Palo+Alto&state=CA&lat=37.45&lon=-122.13&s=59e3f571e239e7145113e7298ac8ae0c0f93f7da&rem=1"; MEETUP_TRACK="id=44347692-f2c1-4873-bd2e-e2a21d8abefa&l=1&s=0a734162726a85c22f6b70efdc99bc08da4f95ad"; MEETUP_SEGMENT=member; trax_universal_reg="uuid=43d23478-cb61-4c58-84b0-825bf6a026ed&v=track&p=group_join&s=70&_=cc5cae"; click-track=%7B%22history%22%3A%5B%7B%22lineage%22%3A%22button.reg-next-button.primary.j-next.j-get-topics.margin-bottom.full-width%3C%23j-submit-loader%3Cdiv%3Cdiv%3C%23interests-categories-reg-view%3C%23main-view-wrapper%22%2C%22linkText%22%3A%22Next%22%2C%22coords%22%3A%5B384%2C1030%5D%2C%22data%22%3A%7B%7D%7D%2C%7B%22lineage%22%3A%22button.reg-next-button.primary.j-next.j-subscribe-topics.margin-bottom.full-width%3C%23j-submit-loader%3Cdiv%3Cdiv%3C%23interests-topics-reg-view%3C%23main-view-wrapper%22%2C%22linkText%22%3A%22Next%22%2C%22coords%22%3A%5B-295%2C5073%5D%2C%22data%22%3A%7B%7D%7D%2C%7B%22lineage%22%3A%22a.navBar-action.ffbox-fix.j-action.j-follow-next%3Cnav%3Cdiv%3C%23header%3C%23top-nav-wrapper%3C%23main-view-wrapper%22%2C%22linkText%22%3A%22Next%22%2C%22coords%22%3A%5B783%2C0%5D%2C%22data%22%3A%7B%7D%7D%5D%7D; MUP_jqueryEn=on; trax_event_groupage_model=uuid=7b7c9e7d-e0c4-40f5-8af2-77e58f2e4b5b&v=group_age&p=start&s=0&_=d456a4; trax_event_groupage_model_withage=uuid=27690ac1-63f7-4493-8cea-8c2a6316b742&v=group_age&p=start&s=0&_=fddb28; MEETUP_GA=rg%3Dsignup%252Csignup%26id%3Dnull
"""

headers = headers.split('\n')
headers = [x.strip() for x in headers]
headers = [x for x in headers if x]

def split(l):
    return l.split(':',1)
headers = {k:v for k,v in map(split,headers)}

def slugify(value):
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub('[^\w\s-]', '', value).strip().lower()
    return re.sub('[-\s]+', '-', value)

def retrieve_cached(slug):
    filename = DIR+"/"+slug
    if os.path.isfile(filename):
        with open(filename) as f:
            return f.read()

def store(slug, html):
    filename = DIR+"/"+slug
    with open(filename,'w') as f:
        f.write(html)

def get(url):
    global headers
    print("GET",url)

    slug = slugify(url)
    html = retrieve_cached(slug)
    if html:
        print("got cached GET")
        return html

    r = requests.get(url, headers=headers)
    if r.status_code != 200:
        raise Exception("Bad status code for %s : %s" \
            % (url, r.status_code))
    store(slug, r.text)
    return r.text