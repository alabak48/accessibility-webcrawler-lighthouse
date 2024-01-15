import concurrent.futures
import os
import json
import subprocess
import threading
import time
from requests_toolbelt.multipart.encoder import MultipartEncoder
import requests
import socket
from urllib.request import urlopen
from urllib.parse import urljoin
from urllib.parse import urlparse


def run_node_script(script_path, *args):
    start_time = time.time()
    command = ['node', script_path, *map(str, args)]
    #print(command[3] + '.json')
    subprocess.run(command)
    ime_datoteke = command[3] + '.json'
    file_path = os.path.join(os.getcwd(), ime_datoteke)

    thread = threading.Thread(target=procitaj_json(command[3], file_path, ime_datoteke, start_time))
    thread.start()
    thread.join()
    try:
        os.remove(file_path)
    except Error as e:
        print(f"PermissionError: {e}")


def procitaj_json(id, file_path, ime_datoteke, start_time):
    # widows mašine u 16. imaju problem da se file koristi. Vjerojatno node nije zapisao do kraja pa malo spavaj
    time.sleep(5)
    #print('gotov, može file na API',id + '.json')
    audits=[]
    accessibility = []
    accessibility_score=0
    with open(file_path, 'r', encoding='utf-8') as f:
        #print('Čitam datoteku')
        data = json.load(f)
        #print(data)
        for d in data:
            if d=='categories':
                obj =data.get('categories')
                for key in obj:
                    if key=='accessibility':
                        obj2 = obj.get('accessibility')
                        accessibility_score=obj2.get('score')
                        for key2 in obj2:
                            if key2=='auditRefs':
                                for k in obj2.get('auditRefs'):
                                    #print('----------',k)
                                    kljucsvojstvo = k['id']  # ovo na API gledati ako nije broje > 0 onda napraviti insert u bazu pa spremiti novi id
                                    #print(kljucsvojstvo, k['id'])
                                    accessibility.append({'s':kljucsvojstvo,'v':k['weight']})
            if d =='audits':
                obj = data.get('audits')
                for key in obj:
                    description=''
                    try:
                        description=obj.get(key)['description']
                    except:
                        pass
                    scoreDisplayMode = ''
                    try:
                        scoreDisplayMode=obj.get(key)['scoreDisplayMode']
                    except:
                        pass
                    kljucsvojstvo=key
                    #print('Ključ svojstvo',kljucsvojstvo,key,description,scoreDisplayMode)
                    audits.append({'s': kljucsvojstvo, 'v': obj.get(key)['score'],'description': description, 'scoreDisplayMode':scoreDisplayMode})
                    #print(json.dumps(audits))
    #return result.stdout.strip()
    # šalji na API
    #print('Gotovo čitanje JSON')
    #print(json.dumps(accessibility))
    #print(json.dumps(audits))
    #print('id:',id)
    #print('accessibility_score:',accessibility_score)
    #print(json.dumps(audits))

    sekundi = str((time.time() - start_time))
    sekundi = sekundi.split('.')[0]
    racunalo = socket.gethostname()
    mp_encoder = MultipartEncoder(
        fields={
            'id': id,
            'accessibility_score': str(accessibility_score),
            'accessibility': json.dumps(accessibility),
            'audits': json.dumps(audits),
            'sekundi':sekundi,
            'racunalo':racunalo,
            'datoteka': (ime_datoteke, open(file_path, 'rb'), 'text/json')
        }
    )
    r = requests.post(
        'https://ozizprivremeno.xyz/S21_pohraniLighthouse.php',
        data=mp_encoder,
        headers={'Content-Type': mp_encoder.content_type}
    )
    print(r.text)



def process_website(index):
    #print('krenuo ', index)
    b=0

    while True:
        b=b+1

        response = urlopen('https://ozizprivremeno.xyz/S20_poberiLighthouse.php')
        #print('status servera kada se traže nove domene za pobiranje:',response.status)
        if response.status == 200:
            niz = json.loads(response.read())
        else:
            return
        #print(b,'prolaz u niti',index, 'server vratio',len(niz),'domena')
        if len(niz) == 0:
            print('Završio ', index)
            return
        for data_json in niz:
            #print('krećem',data_json.get('url'))
            parameters = [data_json.get('url'), str(data_json.get('id'))]
            run_node_script(js_module_path, *parameters)
            #print(f"Output for {url}: {output}")
            #print('gotov', url,'sada poslati datotetu na api')
        #print('Završio',b, 'prolaz u niti', index)
        #break

js_module_path = os.path.join(os.getcwd(), 'app.mjs')

max_threads = 5 # 100 ne može nikako, i na 20 se buni
with concurrent.futures.ThreadPoolExecutor(max_threads) as executor:
    futures = [executor.submit(process_website, index) for index in range(max_threads)]
    concurrent.futures.wait(futures)

#process_website(1);