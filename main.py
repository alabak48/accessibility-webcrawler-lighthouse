import concurrent.futures
import os
import subprocess
import time

start_time = time.time()
def run_node_script(script_path, *args):
    command = ['node', script_path, *map(str, args)]
    result = subprocess.run(command)
    return result.stdout.strip()


def process_website(url, index):
    parameters = [url, str(index)]
    output = run_node_script(js_module_path, *parameters)
    print(f"Output for {url}: {output}")


js_module_path =  os.path.join(os.getcwd(), 'app.mjs')

websites = [
    'https://www.mefos.unios.hr/index.php/hr/',
    'https://www.biologija.unios.hr/',
    'https://www.kemija.unios.hr/',
    'https://www.pravos.unios.hr/',
    'http://www.uaos.unios.hr/',
    'http://www.efos.unios.hr/',
    'https://www.ferit.unios.hr/',
    'https://www.fdmz.hr/index.php/hr/',
    'https://www.foozos.hr/',
    'https://www.ffos.unios.hr/'
]

max_threads = 5

with concurrent.futures.ThreadPoolExecutor(max_threads) as executor:
    futures = [executor.submit(process_website, url, websites.index(url)) for url in websites]

    concurrent.futures.wait(futures)

print("--- %s seconds ---" % (time.time() - start_time))