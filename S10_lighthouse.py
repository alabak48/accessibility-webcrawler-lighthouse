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
    #print('Datoteka',file_path)
    svojstvo_accessibility = {
        'accesskeys': 1,
        'aria-allowed-attr': 2,
        'aria-allowed-role': 3,
        'aria-command-name': 4,
        'aria-dialog-name': 5,
        'aria-hidden-body': 6,
        'aria-hidden-focus': 7,
        'aria-input-field-name': 8,
        'aria-meter-name': 9,
        'aria-progressbar-name': 10,
        'aria-required-attr': 11,
        'aria-required-children': 12,
        'aria-required-parent': 13,
        'aria-roles': 14,
        'aria-text': 15,
        'aria-toggle-field-name': 16,
        'aria-tooltip-name': 17,
        'aria-treeitem-name': 18,
        'aria-valid-attr-value': 19,
        'aria-valid-attr': 20,
        'button-name': 21,
        'bypass': 22,
        'color-contrast': 23,
        'definition-list': 24,
        'dlitem': 25,
        'document-title': 26,
        'duplicate-id-active': 27,
        'duplicate-id-aria': 28,
        'form-field-multiple-labels': 29,
        'frame-title': 30,
        'heading-order': 31,
        'html-has-lang': 32,
        'html-lang-valid': 33,
        'html-xml-lang-mismatch': 34,
        'image-alt': 35,
        'image-redundant-alt': 36,
        'input-button-name': 37,
        'input-image-alt': 38,
        'label': 39,
        'link-in-text-block': 40,
        'link-name': 41,
        'list': 42,
        'listitem': 43,
        'meta-refresh': 44,
        'meta-viewport': 45,
        'object-alt': 46,
        'select-name': 47,
        'skip-link': 48,
        'tabindex': 49,
        'table-duplicate-name': 50,
        'td-headers-attr': 51,
        'th-has-data-cells': 52,
        'valid-lang': 53,
        'video-caption': 54,
        'focusable-controls': 55,
        'interactive-element-affordance': 56,
        'logical-tab-order': 57,
        'visual-order-follows-dom': 58,
        'focus-traps': 59,
        'managed-focus': 60,
        'use-landmarks': 61,
        'offscreen-content-10': 62,
        'custom-controls-labels': 63,
        'custom-controls-roles': 64,
        'empty-heading': 65,
        'identical-links-same-purpose': 66,
        'landmark-one-main': 67,
        'target-size': 68,
        'label-content-name-mismatch': 69,
        'table-fake-caption': 70,
        'td-has-header': 71
    }
    svojstvo_audit = {
        'accesskeys': 1,
        'aria-allowed-attr': 2,
        'aria-allowed-role': 3,
        'aria-command-name': 4,
        'aria-dialog-name': 5,
        'aria-hidden-body': 6,
        'aria-hidden-focus': 7,
        'aria-input-field-name': 8,
        'aria-meter-name': 9,
        'aria-progressbar-name': 10,
        'aria-required-attr': 11,
        'aria-required-children': 12,
        'aria-required-parent': 13,
        'aria-roles': 14,
        'aria-text': 15,
        'aria-toggle-field-name': 16,
        'aria-tooltip-name': 17,
        'aria-treeitem-name': 18,
        'aria-valid-attr': 19,
        'aria-valid-attr-value': 20,
        'bf-cache': 21,
        'bootup-time': 22,
        'button-name': 23,
        'bypass': 24,
        'canonical': 25,
        'charset': 26,
        'color-contrast': 27,
        'content-width': 28,
        'crawlable-anchors': 29,
        'critical-request-chains': 30,
        'csp-xss': 31,
        'cumulative-layout-shift': 32,
        'custom-controls-labels': 33,
        'custom-controls-roles': 34,
        'definition-list': 35,
        'deprecations': 36,
        'diagnostics': 37,
        'dlitem': 38,
        'doctype': 39,
        'document-title': 40,
        'dom-size': 41,
        'duplicate-id-active': 42,
        'duplicate-id-aria': 43,
        'duplicated-javascript': 44,
        'efficient-animated-content': 45,
        'empty-heading': 46,
        'errors-in-console': 47,
        'final-screenshot': 48,
        'first-contentful-paint': 49,
        'first-meaningful-paint': 50,
        'focus-traps': 51,
        'focusable-controls': 52,
        'font-display': 53,
        'font-size': 54,
        'form-field-multiple-labels': 55,
        'frame-title': 56,
        'geolocation-on-start': 57,
        'heading-order': 58,
        'hreflang': 59,
        'html-has-lang': 60,
        'html-lang-valid': 61,
        'html-xml-lang-mismatch': 62,
        'http-status-code': 63,
        'identical-links-same-purpose': 64,
        'image-alt': 65,
        'image-aspect-ratio': 66,
        'image-redundant-alt': 67,
        'image-size-responsive': 68,
        'input-button-name': 69,
        'input-image-alt': 70,
        'inspector-issues': 71,
        'installable-manifest': 72,
        'interactive': 73,
        'interactive-element-affordance': 74,
        'is-crawlable': 75,
        'is-on-https': 76,
        'js-libraries': 77,
        'label': 78,
        'label-content-name-mismatch': 79,
        'landmark-one-main': 80,
        'largest-contentful-paint': 81,
        'largest-contentful-paint-element': 82,
        'layout-shift-elements': 83,
        'lcp-lazy-loaded': 84,
        'legacy-javascript': 85,
        'link-in-text-block': 86,
        'link-name': 87,
        'link-text': 88,
        'list': 89,
        'listitem': 90,
        'logical-tab-order': 91,
        'long-tasks': 92,
        'main-thread-tasks': 93,
        'mainthread-work-breakdown': 94,
        'managed-focus': 95,
        'maskable-icon': 96,
        'max-potential-fid': 97,
        'meta-description': 98,
        'meta-refresh': 99,
        'meta-viewport': 100,
        'metrics': 101,
        'modern-image-formats': 102,
        'network-requests': 103,
        'network-rtt': 104,
        'network-server-latency': 105,
        'no-document-write': 106,
        'no-unload-listeners': 107,
        'non-composited-animations': 108,
        'notification-on-start': 109,
        'object-alt': 110,
        'offscreen-content-hidden': 111,
        'offscreen-images': 112,
        'paste-preventing-inputs': 113,
        'performance-budget': 114,
        'plugins': 115,
        'preload-fonts': 116,
        'prioritize-lcp-image': 117,
        'pwa-cross-browser': 118,
        'pwa-each-page-has-url': 119,
        'pwa-page-transitions': 120,
        'redirects': 121,
        'render-blocking-resources': 122,
        'robots-txt': 123,
        'screenshot-thumbnails': 124,
        'script-treemap-data': 125,
        'select-name': 126,
        'server-response-time': 127,
        'skip-link': 128,
        'speed-index': 129,
        'splash-screen': 130,
        'structured-data': 131,
        'tabindex': 132,
        'table-duplicate-name': 133,
        'table-fake-caption': 134,
        'tap-targets': 135,
        'target-size': 136,
        'td-has-header': 137,
        'td-headers-attr': 138,
        'th-has-data-cells': 139,
        'themed-omnibox': 140,
        'third-party-facades': 141,
        'third-party-summary': 142,
        'timing-budget': 143,
        'total-blocking-time': 144,
        'total-byte-weight': 145,
        'unminified-css': 146,
        'unminified-javascript': 147,
        'unsized-images': 148,
        'unused-css-rules': 149,
        'unused-javascript': 150,
        'use-landmarks': 151,
        'user-timings': 152,
        'uses-http2': 153,
        'uses-long-cache-ttl': 154,
        'uses-optimized-images': 155,
        'uses-passive-event-listeners': 156,
        'uses-rel-preconnect': 157,
        'uses-rel-preload': 158,
        'uses-responsive-images': 159,
        'uses-text-compression': 160,
        'valid-lang': 161,
        'valid-source-maps': 162,
        'video-caption': 163,
        'viewport': 164,
        'visual-order-follows-dom': 165
    }
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
                                    accessibility.append({'s':svojstvo_accessibility[k['id']],'v':k['weight']})
           if d =='audits':
                #print('Našao audits')
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
                    audits.append({'s': svojstvo_audit[key], 'v': obj.get(key)['score'],'description': description, 'scoreDisplayMode':scoreDisplayMode})
    #return result.stdout.strip()
    # šalji na API
    #print('Komada',len(accessibility))
    #print(json.dumps(accessibility))
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
    #print(r.text)



def process_website(index):
    print('krenuo ', index)
    b=0

    while True:
        b=b+1

        response = urlopen('https://ozizprivremeno.xyz/S20_poberiLighthouse.php')
        print('status servera kada se traže nove domene za pobiranje:',response.status)
        if response.status == 200:
            niz = json.loads(response.read())
        else:
            return
        print(b,'prolaz u niti',index, 'server vratio',len(niz),'domena')
        if len(niz) == 0:
            print('Završio ', index)
            return
        for data_json in niz:
            print('krećem',data_json.get('url'))
            parameters = [data_json.get('url'), str(data_json.get('id'))]
            run_node_script(js_module_path, *parameters)
            #print(f"Output for {url}: {output}")
            #print('gotov', url,'sada poslati datotetu na api')
        print('Završio',b, 'prolaz u niti', index)


js_module_path = os.path.join(os.getcwd(), 'app.mjs')

max_threads = 10 # 100 ne može nikako, i na 20 se buni
with concurrent.futures.ThreadPoolExecutor(max_threads) as executor:
    futures = [executor.submit(process_website, index) for index in range(max_threads)]
    concurrent.futures.wait(futures)

