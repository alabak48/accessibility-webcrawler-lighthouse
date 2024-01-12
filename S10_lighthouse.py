import concurrent.futures
import os
import json
import subprocess
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
    id = command[3]
    #print('gotov, može file na API',id + '.json')
    ime_datoteke = command[3] + '.json'
    file_path = os.path.join(os.getcwd(), ime_datoteke)
    #print('Datoteka',file_path)
    audits=[]
    accessibility = []
    accessibility_score=0
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
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
                                   if 'group' in k:
                                       accessibility.append({'g':k['group'],'s':k['id'],'v':k['weight']})
                                   else:
                                       accessibility.append({'g':'no-group','s':k['id'],'v':k['weight']})
           if d =='audits':
                #print('Našao audits')
                obj = data.get('audits')
                for key in obj:
                    audits.append({'s': key, 'v': obj.get(key)['score']})
    #return result.stdout.strip()
    # šalji na API
    #print('Komada',len(accessibility))
    #print(json.dumps(accessibility))
    print('id:',id)
    print('accessibility_score:',accessibility_score)
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
    os.remove(file_path)


def process_website(index):
    print('krenuo ', index)
    while True:
        response = urlopen('https://ozizprivremeno.xyz/S20_poberiLighthouse.php')
        #print(response.status)
        if response.status == 200:
            niz = json.loads(response.read())
        else:
            return
        #print(len(niz))
        if len(niz) == 0:
            print('Završio ', index)
            return
        for data_json in niz:
            print('krećem',data_json.get('url'))
            parameters = [data_json.get('url'), str(data_json.get('id'))]
            run_node_script(js_module_path, *parameters)
            #print(f"Output for {url}: {output}")
            #print('gotov', url,'sada poslati datotetu na api')


js_module_path =  os.path.join(os.getcwd(), 'app.mjs')

max_threads = 10
with concurrent.futures.ThreadPoolExecutor(max_threads) as executor:
    futures = [executor.submit(process_website, index) for index in range(max_threads)]
    concurrent.futures.wait(futures)

