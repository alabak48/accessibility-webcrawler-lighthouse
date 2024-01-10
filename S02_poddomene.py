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
    poveznica=poveznica.lower()
    return ( poveznica.endswith('.pdf')
            or poveznica.endswith('.jpg')
            or poveznica.endswith('.jpeg')
            or poveznica.endswith('.png')
            or poveznica.endswith('.webp')
            or poveznica.endswith('.docx')
            or poveznica.endswith('.doc')
            or poveznica.endswith('.xlsx')
            or poveznica.endswith('.pptx')
            or poveznica.endswith('.ppt')
            or poveznica.endswith('.xls')
            or poveznica.endswith('.zip')
            or poveznica.endswith('.rar')
            or poveznica.endswith('.gz')
            or poveznica.endswith('.rtf')
            or poveznica.endswith('.mp3')
            or poveznica.endswith('.mp4')
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

def poberi(index,id, url):
    start_time = time.time()
    # id=85565
    # url = 'https://www.unisb.hr/'
    if url.endswith('/'):
        url = url[:-1]
    if not url.endswith('.hr'):
        return
    # print(url)
    domena = urlparse(url).netloc
    domena = domena.replace('www.', '')
    print('Krećem (', index, '): ', domena)
    posjecenepoveznice = set()
    jedinstvenedomene = set()
    poveznice = set()
    try:
        reqs = requests.get(url, verify=False)
        if reqs.status_code!=200:
            print('Greška status ', reqs.status_code, ' na ', id , domena)
            return
        # print(reqs.text)

        soup = BeautifulSoup(reqs.text, 'html.parser')
        for link in soup.find_all('a'):
            poveznica = urljoin(url, link.get('href'))
            #print('R0 ', poveznica)
            d = urlparse(poveznica).netloc
            if (d == 'www.' + domena or d == domena) and not datoteka(poveznica) and not istapoveznica(poveznica, url):
                if not poveznica in posjecenepoveznice:
                    posjecenepoveznice.add(poveznica)
                    poveznice.add(poveznica)
            try:
                jedinstvenedomene.add(d)
            except Exception as error:
                #print('Greška level 0: ', error)
                pass
        # print('Ukupno posjecenepoveznice 1: ', len(posjecenepoveznice))
        #if len(poveznice)>100: # makni kasnije
        #    return
        # 2. razina
        poveznice2 = set()
        b = 0
        for p in poveznice:
            b = b + 1
            try:
                if b % 50 ==0:
                    print('R1 ', b, '/', len(poveznice), ' -> ', len(jedinstvenedomene), ', ', p)
                reqs = requests.get(p, verify=False)
                soup = BeautifulSoup(reqs.text, 'html.parser')
                for link in soup.find_all('a'):
                    poveznica = urljoin(url, link.get('href'))
                    d = urlparse(poveznica).netloc
                    if (d == 'www.' + domena or d == domena) and not datoteka(poveznica) and not istapoveznica(
                            poveznica, url):
                        if not poveznica in posjecenepoveznice:
                            posjecenepoveznice.add(poveznica)
                            poveznice2.add(poveznica)
                    try:
                        jedinstvenedomene.add(d)
                    except Exception as error:
                        #print('Greška level 0: ', error)
                        pass
            except Exception as error:
                #print('Greška level 1: ', error)
                pass
        # print('Ukupno posjecenepoveznice 2: ', domena ,' - ', len(posjecenepoveznice),' - ', b, '/', len(poveznice))
        # 3. razina - zbog adresara na skole.hr
        # print('Ukupno poveznice2  za 3. razinu: ', len(poveznice2))
        #privremeno - makni
        #if len(poveznice2)>1000:
        #    return
        b = 0
        for p in poveznice2:
            b = b + 1
            try:
                if b % 50 == 0:
                    print('R2 ', b, '/', len(poveznice2), ' -> ', len(jedinstvenedomene), ', ', p)
                reqs = requests.get(p, verify=False)
                soup = BeautifulSoup(reqs.text, 'html.parser')
                for link in soup.find_all('a'):
                    poveznica = urljoin(url, link.get('href'))
                    d = urlparse(poveznica).netloc
                    try:
                        jedinstvenedomene.add(d)
                    except:
                        # print('Greska jedinstvenedomene.add level 2')
                        pass
            except Exception as error:
                #print('Greška level 2: ', error)
                pass
                # print('Greška level 3: ', p)
    except Exception as error:
        #print('Greška level 1: ', url, ' -> ', error)
        pass
    # print('Šaljem na api ',domena)

    json_jedinstvene_poddomene = pripremi_za_api_jedinstveno(jedinstvenedomene, domena)
    json_sve_domene = pripremi_za_api(jedinstvenedomene)
    json_jedinstvene_poveznice = pripremi_za_api(posjecenepoveznice)
    # print('Poddomene na API:  -> ', json_jedinstvene_poddomene)
    # print('Poveznice na API:  -> ', json_jedinstvene_poveznice)
    # print('Domene na API:  -> ', json_sve_domene)
    sekundi = str((time.time() - start_time))
    sekundi = sekundi.split('.')[0]
    racunalo = socket.gethostname()
    data = {'id': id,
            'poddomene': json_jedinstvene_poddomene,
            'poveznice': json_jedinstvene_poveznice,
            'domene': json_sve_domene,
            'sekundi': sekundi,
            'racunalo': racunalo}
    uk = 0
    for p in posjecenepoveznice:
        uk = uk + 1
    rez = requests.post(url='https://ozizprivremeno.xyz/S04_pohraniPD.php', data=data)
    # print(rez.status_code)
    print(f"Odradio({index}) {id}: {domena} -> ", sekundi, 's, poveznica: ', uk)

def process_website_API(index):
    while True:
        response = urlopen('https://ozizprivremeno.xyz/S03_poberiPD.php')
        if response.status == 200:
            niz = json.loads(response.read())
        else:
            return
        if len(niz)==0:
            print('Završio ', index)
            return
        for data_json in niz:
            poberi(index,data_json.get('id'),data_json.get('naziv'))


# izvođenje
max_threads = 100
with concurrent.futures.ThreadPoolExecutor(max_threads) as executor:
    futures = [executor.submit(process_website_API, index) for index in range(max_threads)]
    concurrent.futures.wait(futures)

#poberi(1,31152,'https://gov.hr/')