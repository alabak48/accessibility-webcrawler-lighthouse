# Ovdje će se na svakoj stranici tražiti poveznice kako bi se našle poddomene na identificiranim stranicama na razini 1

import requests
from bs4 import BeautifulSoup

url = 'http://www.unios.hr/o-sveucilistu/sastavnice/'
reqs = requests.get(url)
soup = BeautifulSoup(reqs.text, 'html.parser')

urls = []
for link in soup.find_all('a'):
    print(link.get('href'))