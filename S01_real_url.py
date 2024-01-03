# dobivena domena je u formi npr unios.hr

import requests
from bs4 import BeautifulSoup

file = open('domene.txt', 'r')
Lines = file.readlines()

count = 0
# Strips the newline character


for line in Lines:
    count += 1
    print("Line{}: {}".format(count, line.strip()))
    domena = line.strip()
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




