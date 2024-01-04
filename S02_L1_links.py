# Ovdje će se na svakoj identificiranoj početnoj stranici tražiti poveznice kako bi se našle poddomene

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from urllib.parse import urlparse

domena = 'skole.hr' # ovo ćemo dobiti od CARNET
# 1. razina
url = 'https://skole.hr'
reqs = requests.get(url)
soup = BeautifulSoup(reqs.text, 'html.parser')

jedinstvenedomene=set()
poveznice=set()
br=0
for link in soup.find_all('a'):
    br=br+1
    poveznica=urljoin(url, link.get('href'))
    d = urlparse(link.get('href')).netloc
    if d == 'www.' + domena or d == domena:
       poveznice.add(poveznica)
    #print(poveznica)
    jedinstvenedomene.add(d)
#print('Ukupno poveznica',br)
# print(jedinstvenedomene)
# 2. razina
poveznice2 = set()
for p in poveznice:
    reqs = requests.get(p)
    soup = BeautifulSoup(reqs.text, 'html.parser')
    for link in soup.find_all('a'):
        poveznica = urljoin(url, link.get('href'))
        d = urlparse(link.get('href')).netloc
        if d == 'www.' + domena or d == domena:
            poveznice2.add(poveznica)
        d = urlparse(link.get('href')).netloc
        jedinstvenedomene.add(d)

# 3. razina - zbog adresara na skole.hr
for p in poveznice2:
    reqs = requests.get(p)
    soup = BeautifulSoup(reqs.text, 'html.parser')
    for link in soup.find_all('a'):
        d = urlparse(link.get('href')).netloc
        jedinstvenedomene.add(d)

for d in jedinstvenedomene:
    try:
        if d.endswith(domena) and d!='www.' + domena and d!=domena:
            print(d) # ovo ide na api
    except:
        pass