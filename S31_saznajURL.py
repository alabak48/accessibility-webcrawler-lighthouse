# https://www.digitalocean.com/community/tutorials/python-http-client-request-get-post
import concurrent.futures
from dns_resolver import resolve
import http.client
import ssl
import requests
from urllib.parse import urlparse
from urllib.request import urlopen
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import time
import json
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def statusi_tip(https,www,d):
        w=''
        if https:
            h='https://'
            if www:
                w = 'www.'
                try:
                    connection = http.client.HTTPSConnection(w+d,context = ssl._create_unverified_context(),timeout=10)
                except Exception as e:
                    return {'d': d, 'url': h + w + d, 's': str(0), 'cl': str(0), 'p': str(e)}
            else:
                try:
                    connection = http.client.HTTPSConnection(d, context=ssl._create_unverified_context(),timeout=10)
                except Exception as e:
                    return {'d': d, 'url': h + w + d, 's': str(0), 'cl': str(0), 'p': str(e)}
        else:
            h = 'http://'
            if www:
                w = 'www.'
                try:
                    connection = http.client.HTTPConnection(w+d,timeout=10)
                except Exception as e:
                    return {'d': d, 'url': h + w + d, 's': str(0), 'cl': str(0), 'p': str(e)}
            else:
                try:
                    connection = http.client.HTTPConnection(d,timeout=10)
                except Exception as e:
                    return {'d': d, 'url': h + w + d, 's': str(0), 'cl': str(0), 'p': str(e)}
        try:
            connection.request("GET", "/")
            response = connection.getresponse()
            return {'d':d, 'url': h + w + d, 's': str(response.status), 'cl': str(0),'p':response.reason}
        except Exception as e:
            return {'d':d,'url': h + w + d, 's': str(0), 'cl': str(0),'p':str(e)}

def saznaj_url(podaci):
    ip = ''
    try:
        up = urlparse(podaci['url']).netloc
        if ':' in up:
            up=up.split(':')[0]
        dns = resolve(up)
        if len(dns)>0:
            ip=str(dns[0])
    except Exception as e:
        ip=str(e)

    try:
        reqs = requests.get(podaci['url'], verify=False)
        return {'ip':ip,'orr_url': podaci['url'] ,'url': reqs.url, 's': podaci['s'], 'cl': str(len(reqs.content)),'p':podaci['p']}
    except Exception as e:
        return {'ip':ip,'orr_url': podaci['url'], 'url': podaci['url'], 's': podaci['s'], 'cl': str(0), 'p': str(e)}


def posao_statusi(d):
    return {'httpswww': statusi_tip(True,True,d),
            'https': statusi_tip(True, False, d),
            'httpwww': statusi_tip(False, True, d),
            'http': statusi_tip(False, False, d)}

def posao(d):
    statusi = posao_statusi(d)
    if statusi['httpswww']['s']=='200':
        return saznaj_url(statusi['httpswww'])
    elif statusi['https']['s']=='200':
        return saznaj_url(statusi['https'])
    elif statusi['httpwww']['s']=='200':
        return saznaj_url(statusi['httpwww'])
    elif statusi['http']['s']=='200':
        return saznaj_url(statusi['http'])
    else:
        return saznaj_url(statusi['httpswww']) # ako nema ništa idi s https://www.



def process_website_API(index):
    while (True):
        response = urlopen('https://ozizprivremeno.xyz/S31_saznajURL.php')
        niz = json.loads(response.read())
        for data_json in niz:
            id = data_json.get('id')
            url = posao(data_json.get('naziv'))
            domena = urlparse(url['url']).netloc
            #print('domena', data_json.get('naziv') ,domena)
            if domena.lower().endswith('.hr'):
                if domena.endswith(data_json.get('naziv').lower()):
                    # idi na server s statusom 2
                    status='2'
                else:
                    # idi na server s statusom 10 - Domena pokazuje na drugu .hr domenu
                    status='10'
            else:
                # idi na server s statusom 11 - Domena izlazi iz .hr
                status='11'
            if url['s']=='0':
                # idi na server s statusom 12 - Domena nije aktivna
                status='12'
            # pošalji na API
            data = {'id': id, 'status': status, 'url':url['url'], 'ip': url['ip'], 'httpstatus': url['s'], 'contentlength': url['cl'],
                    'poruka': url['p']}
            r=requests.post(url='https://ozizprivremeno.xyz/S32_pohraniURL.php', data=data)
            print(index,'Vratio API:',r.text, 'podaci:',data)




max_threads = 1000
with concurrent.futures.ThreadPoolExecutor(max_threads) as executor:
    futures = [executor.submit(process_website_API, index) for index in range(max_threads)]
    concurrent.futures.wait(futures)

#process_website_API(1)