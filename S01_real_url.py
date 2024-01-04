# dobivena domena je u formi npr unios.hr
import concurrent.futures
import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen
import json

def process_website_API(index):
    while (True):
        url = "https://ozizprivremeno.xyz/poberi.php"
        response = urlopen(url)
        niz = json.loads(response.read())
        for data_json in niz:
            id = data_json.get('id')
            domena = data_json.get('naziv')
            postoji = True
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
                            postoji = False
            stvarnadomena=''
            if (postoji):
                try:
                    stvarnadomena = reqs.url
                except:
                    stvarnadomena = 'null'
            else:
                stvarnadomena = 'null'

            # pošalji na API
            data = {'id': id,'stvarnadomena': stvarnadomena}
            requests.post(url='https://ozizprivremeno.xyz/pohraniSD.php', data=data)
            print(f"Odradio({index}) {id}: {domena} -> {stvarnadomena}")



# Strips the newline character

def process_website(data_json):
    domena = data_json.get('naziv')
    print("Domena {}".format(domena))

    postoji = True
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
                    postoji = False
    file1 = open('domenePobrano.txt', 'a')
    if (postoji):
        try:
            file1.write('(\'' + domena +'\',\'' + reqs.url +'\'),\n')
            print(domena,',', reqs.url)
        except:
            file1.write('(\'' +domena + '\',null),\n')
            print(domena,',null')
    else:
        file1.write('(\'' +domena + '\',null),\n')
        print(domena,',null')
    file1.close()

file = open('domene.txt', 'r')
lines = file.readlines()

max_threads = 100


with concurrent.futures.ThreadPoolExecutor(max_threads) as executor:
    futures = [executor.submit(process_website_API, index) for index in range(max_threads)]
    concurrent.futures.wait(futures)

