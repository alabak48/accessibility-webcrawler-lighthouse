# dobivena domena je u formi npr unios.hr

import requests
from bs4 import BeautifulSoup

domena = 'uniosik.hr';

url = 'https://unios.hr'
postoji=True
try:
    reqs = requests.get('https://' + domena)
except:
    try:
        reqs = requests.get('http://' + domena)
    except:
        try:
            reqs = requests.get('https://www.' + domena)
        except:
            try:
                reqs = requests.get('http://www.' + domena)
            except:
                print('Domena ne postoji - ručno provjeriti takve')
                postoji=False

if (postoji):
    try:
        print('dentificirana početna stranica: ' + reqs.url)
        soup = BeautifulSoup(reqs.text, 'html.parser')
        urls = []
        for link in soup.find_all('a'):
            print(link.get('href'))
    except:
        print('Neki problem - ručno provjeriti takve')