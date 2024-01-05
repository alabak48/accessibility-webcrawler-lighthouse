# Ovdje će se na svakoj identificiranoj početnoj stranici tražiti poveznice kako bi se našle poddomene
import concurrent.futures
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from urllib.parse import urlparse
from urllib.request import urlopen
import json

def process_website_API(index):
    while (True):
        response = urlopen('https://ozizprivremeno.xyz/S03_poberiPD.php')
        if response.status==200:
            niz = json.loads(response.read())
        else:
            return
        for data_json in niz:
            id=data_json.get('id')
            url = data_json.get('naziv')
            domena = urlparse(url).netloc
            print('Krećem: ',domena)
            posjecenepoveznice = set()
            jedinstvenedomene = set()
            poveznice = set()
            try:
                reqs = requests.get(url)
                soup = BeautifulSoup(reqs.text, 'html.parser')
                for link in soup.find_all('a'):
                    poveznica=urljoin(url, link.get('href'))
                    d = urlparse(link.get('href')).netloc
                    if d == 'www.' + domena or d == domena:
                       if not poveznica in posjecenepoveznice:
                           posjecenepoveznice.add(poveznica)
                           poveznice.add(poveznica)
                    try:
                        jedinstvenedomene.add(d.replace('www.',''))
                    except:
                        pass
                #print('Ukupno posjecenepoveznice 1: ', len(posjecenepoveznice))
                # print(jedinstvenedomene)
                # 2. razina
                poveznice2 = set()
                b=0
                for p in poveznice:
                    b=b+1
                    try:
                        reqs = requests.get(p)
                        soup = BeautifulSoup(reqs.text, 'html.parser')
                        for link in soup.find_all('a'):
                            poveznica = urljoin(url, link.get('href'))
                            d = urlparse(link.get('href')).netloc
                            if d == 'www.' + domena or d == domena:
                                if not poveznica in posjecenepoveznice:
                                    posjecenepoveznice.add(poveznica)
                                    poveznice2.add(poveznica)
                            try:
                                jedinstvenedomene.add(d.replace('www.',''))
                            except:
                                pass
                    except:
                        print('Greška level 2: ', p)
                #print('Ukupno posjecenepoveznice 2: ', domena ,' - ', len(posjecenepoveznice),' - ', b, '/', len(poveznice))
                # 3. razina - zbog adresara na skole.hr
                #print('Ukupno poveznice2  za 3. razinu: ', len(poveznice2))
                b=0
                for p in poveznice2:
                    b=b+1
                    try:
                        #print(b,'/',len(poveznice2))
                        reqs = requests.get(p)
                        soup = BeautifulSoup(reqs.text, 'html.parser')
                        for link in soup.find_all('a'):
                            d = urlparse(link.get('href')).netloc
                            try:
                                jedinstvenedomene.add(d.replace('www.',''))
                            except:
                                pass
                    except:
                        pass
                        #print('Greška level 3: ', p)
            except Exception as error:
                pass
                #print('Greška level 1: ', url, ' -> ', error)
            #print('Šaljem na api ',domena)
            zaAPI=[]
            for d in jedinstvenedomene:
                try:
                    if d.endswith('.'+domena) and d!=domena:
                        zaAPI.append(d)
                        #print(d) # ovo ide na api
                except:
                    pass
            jsonpd = json.dumps(zaAPI)
            #print('Poddomene na API: ' + jsonpd)
            data = {'id': id,'poddomene': jsonpd, 'analiziranopoveznica': len(posjecenepoveznice)}
            requests.post(url='https://ozizprivremeno.xyz/S04_pohraniPD.php', data=data)
            print(f"Odradio({index}) {id}: {domena} -> {len(posjecenepoveznice)}")


max_threads = 100
with concurrent.futures.ThreadPoolExecutor(max_threads) as executor:
    futures = [executor.submit(process_website_API, index) for index in range(max_threads)]
    concurrent.futures.wait(futures)
