# Ovdje će se na svakoj identificiranoj početnoj stranici tražiti poveznice kako bi se našle poddomene

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from urllib.parse import urlparse

domena = 'unios.hr' # ovo ćemo dobiti od CARNET

url = 'http://www.' + domena
reqs = requests.get(url)
soup = BeautifulSoup(reqs.text, 'html.parser')

jedinstvenedomene=set()

urls = []
br=0
for link in soup.find_all('a'):
    br=br+1
    print(urljoin(url, link.get('href')))
    jedinstvenedomene.add(urlparse(link.get('href')).netloc)
print('Ukupno poveznica',br)
# print(jedinstvenedomene)

for d in jedinstvenedomene:
    try:
        if d.endswith(domena) and d!='www.' + domena and d!=domena:
            print(d) # ovo ide na api
    except:
        pass