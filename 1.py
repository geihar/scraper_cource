import urllib.request
from bs4 import BeautifulSoup
import requests, shutil
import threading


print('Please wait, collecting urls')

html = urllib.request.urlopen('https://te.legra.ph/Sliv-kursa-PlastikCash-04-22')
soup = BeautifulSoup(html, 'html.parser').find_all('a')
urls = []

for i in soup[2:]:
    html = urllib.request.urlopen(i['href'])
    script = str(BeautifulSoup(html, 'html.parser').find_all('script')[-1])
    clean_script = script[script.find("var serverVm") + 24: script.find(";") + 1].split(',')
    counter = 0
    for i in clean_script:
        if "Url" in i:
            counter = counter + 1
            if counter == 4:
                counter = 0
                urls.append(i[i.find("h"): -1])
                break


def download(i, url):
    print(f"Thread № {i} started")
    filename = f'(PlastikCash) Lesson {i}.mp4'
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        with open(filename, "wb") as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)
    if len(threading.enumerate()) != 2:
        print(f"Thread № {i} ended, {len(threading.enumerate()) - 2} file(s) left to upload")


for i, url in enumerate(urls):
    threading.Thread(target=download, args=[i+1, url]).start()


