import requests, unicodedata, re, os.path

DIR = "HTML"

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
    print("GET",url)

    slug = slugify(url)
    html = retrieve_cached(slug)
    if html:
        print("got cached GET")
        return html

    r = requests.get(url)
    if r.status_code != 200:
        raise Exception("Bad status code for %s : %s" \
            % (url, r.status_code))
    store(slug, r.text)
    return r.text