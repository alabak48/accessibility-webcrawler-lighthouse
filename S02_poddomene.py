# Ovdje će se na svakoj identificiranoj početnoj stranici tražiti poveznice kako bi se našle poddomene
import concurrent.futures
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from urllib.parse import urlparse
from urllib.request import urlopen
import json
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import time
import socket

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def datoteka(poveznica):
    return ( poveznica.endswith('.pdf')
            or poveznica.endswith('.jpg')
            or poveznica.endswith('.png')
            or poveznica.endswith('.docx')
            or poveznica.endswith('.doc')
            or poveznica.endswith('.xlsx')
            or poveznica.endswith('.xls')
            or poveznica.endswith('.zip')
            or poveznica.endswith('.gz')
            or poveznica.endswith('.rtf')
            or poveznica.endswith('.mp3')
            or poveznica.endswith('.mov'))

def istapoveznica(prvi,drugi):
    if prvi.endswith('/'):
        prvi = prvi[:-1]
    if drugi.endswith('/'):
        drugi = drugi[:-1]
    prvi=prvi.replace('www.','')
    prvi = prvi.replace('https:', 'http:')
    drugi = drugi.replace('www.', '')
    drugi = drugi.replace('https:', 'http:')
    return prvi==drugi
def pripremi_za_api_jedinstveno(set_podaci,domena):
    niz = []
    domena = domena.replace('www.', '')
    domena = domena.replace('https://', '')
    domena = domena.replace('http://', '')
    for d in set_podaci:
        #print(type(d), ' -> ', str(d), '==', domena)
        try:
            d = d.replace('www.', '')
            if d.endswith('.' + domena) and d != domena:
                niz.append(d)
                # print(d) # ovo ide na api
        except:
            pass
    return json.dumps(niz)

def pripremi_za_api(set_podaci):
    niz = []
    for d in set_podaci:
        # print(type(d), ' -> ', str(d), '==', domena)
        try:
            d = d.replace('www.', '')
            niz.append(d)
            # print(d) # ovo ide na api
        except:
            pass
    return json.dumps(niz)

def process_website_API(index):
    while True:
        response = urlopen('https://ozizprivremeno.xyz/S03_poberiPD.php')
        if response.status == 200:
            niz = json.loads(response.read())
        else:
            return
        for data_json in niz:
            id = data_json.get('id')
            url = data_json.get('naziv')
            start_time = time.time()
            #id=85565
            #url = 'https://www.unisb.hr/'
            if url.endswith('/'):
                url=url[:-1]

            #print(url)
            domena = urlparse(url).netloc
            domena=domena.replace('www.','')
            print('Krećem: ',domena)
            posjecenepoveznice = set()
            jedinstvenedomene = set()
            poveznice = set()
            try:
                reqs = requests.get(url, verify=False)
                #print(reqs.text)
                soup = BeautifulSoup(reqs.text, 'html.parser')
                for link in soup.find_all('a'):
                    poveznica=urljoin(url, link.get('href'))
                    d = urlparse(poveznica).netloc
                    if (d == 'www.' + domena or d == domena) and not datoteka(poveznica) and not istapoveznica(poveznica,url):
                       if not poveznica in posjecenepoveznice:
                           posjecenepoveznice.add(poveznica)
                           poveznice.add(poveznica)
                    try:
                        jedinstvenedomene.add(d)
                    except:
                        pass
                #print('Ukupno posjecenepoveznice 1: ', len(posjecenepoveznice))

                # 2. razina
                poveznice2 = set()
                b=0
                for p in poveznice:
                    b=b+1
                    try:
                        #print('R1 ', b, '/', len(poveznice), ' -> ', len(jedinstvenedomene), ', ', p)
                        reqs = requests.get(p, verify=False)
                        soup = BeautifulSoup(reqs.text, 'html.parser')
                        for link in soup.find_all('a'):
                            poveznica = urljoin(url, link.get('href'))
                            d = urlparse(poveznica).netloc
                            if (d == 'www.' + domena or d == domena) and not datoteka(poveznica) and not istapoveznica(poveznica,url):
                                if not poveznica in posjecenepoveznice:
                                    posjecenepoveznice.add(poveznica)
                                    poveznice2.add(poveznica)
                            try:
                                jedinstvenedomene.add(d)
                            except:
                                #print('Greska jedinstvenedomene.add level 2')
                                pass
                    except:
                        #print('Greška level 2: ', p)
                        pass
                #print('Ukupno posjecenepoveznice 2: ', domena ,' - ', len(posjecenepoveznice),' - ', b, '/', len(poveznice))
                # 3. razina - zbog adresara na skole.hr
                #print('Ukupno poveznice2  za 3. razinu: ', len(poveznice2))
                b=0
                for p in poveznice2:
                    b=b+1
                    try:
                        #print('R2 ', b, '/', len(poveznice2), ' -> ', len(jedinstvenedomene), ', ', p)
                        reqs = requests.get(p, verify=False)
                        soup = BeautifulSoup(reqs.text, 'html.parser')
                        for link in soup.find_all('a'):
                            poveznica = urljoin(url, link.get('href'))
                            d = urlparse(poveznica).netloc
                            try:
                                jedinstvenedomene.add(d)
                            except:
                                #print('Greska jedinstvenedomene.add level 2')
                                pass
                    except:
                        pass
                        #print('Greška level 3: ', p)
            except Exception as error:
                #pass
                print('Greška level 1: ', url, ' -> ', error)
            #print('Šaljem na api ',domena)

            json_jedinstvene_poddomene = pripremi_za_api_jedinstveno(jedinstvenedomene, domena)
            json_sve_domene=pripremi_za_api(jedinstvenedomene)
            json_jedinstvene_poveznice=pripremi_za_api(posjecenepoveznice)
            #print('Poddomene na API:  -> ', json_jedinstvene_poddomene)
            #print('Poveznice na API:  -> ', json_jedinstvene_poveznice)
            #print('Domene na API:  -> ', json_sve_domene)
            sekundi = str((time.time() - start_time))
            sekundi=sekundi.split('.')[0]
            racunalo=socket.gethostname()
            data = {'id': id,
                    'poddomene': json_jedinstvene_poddomene,
                    'poveznice': json_jedinstvene_poveznice,
                    'domene': json_sve_domene,
                    'sekundi': sekundi,
                    'racunalo': racunalo}
            rez = requests.post(url='https://ozizprivremeno.xyz/S04_pohraniPD.php', data=data)
            #print(rez.status_code)
            print(f"Odradio({index}) {id}: {domena} -> ", sekundi, 's')


# izvođenje
max_threads = 100
with concurrent.futures.ThreadPoolExecutor(max_threads) as executor:
    futures = [executor.submit(process_website_API, index) for index in range(max_threads)]
    concurrent.futures.wait(futures)
