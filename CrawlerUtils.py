#!/usr/bin/env python3 -tt

import requests
import os
import pprint
import sys
import json
import codecs
import csv
import io
import shutil
import time
from pathlib import Path
from urllib.parse import urlparse
from bs4 import BeautifulSoup

USER_AGENT = "PikaDexDataPipeline/1.0 (+offline tooling; contact repository owner)"
REQUEST_TIMEOUT_SECONDS = 30
MINIMUM_HOST_INTERVAL_SECONDS = 1.0
MAX_ATTEMPTS = 3
_last_request_by_host = {}
_session = requests.Session()
_session.headers.update({"User-Agent": USER_AGENT})


def _allowed_hosts():
    value = os.environ.get("PIKADEX_CRAWLER_ALLOWED_HOSTS", "")
    return {host.strip().lower() for host in value.split(",") if host.strip()}


def request(url, stream=False):
    """Fetch a declared crawler URL with bounded retries and host rate limiting."""
    host = (urlparse(url).hostname or "").lower()
    allowed_hosts = _allowed_hosts()
    if not allowed_hosts:
        raise RuntimeError("PIKADEX_CRAWLER_ALLOWED_HOSTS is required")
    if not host or host not in allowed_hosts:
        raise RuntimeError("Crawler URL host is not allowlisted: %s" % host)

    for attempt in range(MAX_ATTEMPTS):
        elapsed = time.monotonic() - _last_request_by_host.get(host, 0.0)
        if elapsed < MINIMUM_HOST_INTERVAL_SECONDS:
            time.sleep(MINIMUM_HOST_INTERVAL_SECONDS - elapsed)
        _last_request_by_host[host] = time.monotonic()

        response = _session.get(url, stream=stream, timeout=REQUEST_TIMEOUT_SECONDS)
        if response.status_code == 429 or response.status_code >= 500:
            if attempt + 1 == MAX_ATTEMPTS:
                response.raise_for_status()
            retry_after = response.headers.get("Retry-After")
            delay = float(retry_after) if retry_after and retry_after.isdigit() else float(2 ** attempt)
            time.sleep(delay)
            continue
        response.raise_for_status()
        return response

    raise RuntimeError("Crawler request exhausted retries: %s" % url)

class DictUnicodeWriter(object):

    def __init__(self, f, fieldnames, dialect=csv.excel_tab, encoding="utf-8", **kwds):
        # Redirect output to a queue
        self.queue = io.StringIO()
        self.writer = csv.DictWriter(self.queue, fieldnames, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, D):
        self.writer.writerow({k:v for k,v in list(D.items())})
#        self.writer.writerow({k:v.encode("utf-8") for k,v in list(D.items())})
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
#        data = data.decode("utf-8")
        
#        if type(data) is bytes:
#            data = data.decode(encoding='utf-8')
        
        # ... and reencode it into the target encoding
#        data = self.encoder.encode(data)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)

    def writerows(self, rows):
        for D in rows:
            self.writerow(D)

    def writeheader(self):
        self.writer.writeheader()

def fetch_file(filename):
    if not os.path.isfile(filename):
        return None

    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return f.read()
    except:
        return None

def fetch_file_lines(filename):
    if not os.path.isfile(filename):
        return None
    
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return f.readlines()
    except:
        return None

def download(url):
    r = request(url)
    return r.text.encode('utf-8')

def ensure_dir(filename):
    Path(filename).parent.mkdir(exist_ok=True, parents=True)
    
def cache_file(contents, filename):
    ensure_dir(filename)
    with codecs.open(filename, 'w', encoding='utf-8') as f:
        f.write(contents)

def write_data_to_file(data, title):
    print("Writing data to %s.json" % title)
    
    filename = title + ".json"
    ensure_dir(filename)
    
    with codecs.open(filename, 'w', encoding='utf8') as f:
        json.dump(data, f, indent=2, sort_keys=True, ensure_ascii=False)
        f.write('\n')

def write_entries_to_tsv(data, fieldnames, title):
    print("Writing data to %s.tsv" % title)

    filename = title + ".tsv"
    ensure_dir(filename)

    with open(filename,'w',encoding='utf-8-sig',newline='') as f:
        writer = csv.DictWriter(f,fieldnames=fieldnames)
        writer.writeheader()
        
        for d in data:
            writer.writerow(d)

#    with codecs.open(filename, 'wb', encoding='utf8') as f:
#        writer = DictUnicodeWriter(f, fieldnames=fieldnames)
#        writer.writeheader()
#
#        for d in data:
#            writer.writerow(d)

#def write_dict_to_csv(data, fieldnames, title):
#    print("Writing data to %s.csv" % title)
#
#    filename = title + ".csv"
#
#    with codecs.open(filename, 'wb', encoding='utf8') as f:
#        writer = DictUnicodeWriter(f, fieldnames=fieldnames)
#        writer.writeheader()
#
#        for d in data:
#            row = d
#            writer.writerow(d)

def fetch_or_download(filename, url):
    contents = fetch_file(filename)
    if contents is None:
        contents = download(url)
        if contents is None:
            print("Failed to download page " + url + ", skipping")
            return None
            
        if type(contents) is bytes:
            contents = contents.decode(encoding='utf-8')
            
        try:
            cache_file(contents, filename)
        except TypeError as e:
            print(e)
    return contents

def download_image(url, filename):
    if os.path.isfile(filename):
        print("Already downloaded image, skipping")
        return
    
    response = request(url, stream=True)
    ensure_dir(filename)
    with open(filename, 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)
    del response

def sanitize_bulbapedia_image_name(name):
    sanitized = name.replace('-Dream', '').replace('Dream ', '').replace(' Sprite', '')
    number_component = sanitized[:3]
    
    try:
        int(number_component)
    except ValueError:
        return sanitized
    
    sanitized = '{}-{}'.format(number_component, sanitized[3:])
    
    return sanitized

def download_images_from_bulbapedia(page_url, page_number, cache_path, image_path):
    filename = cache_path + '_AllItems-{}.html'.format(page_number)
    contents = fetch_or_download(filename, page_url)
    soup = BeautifulSoup(contents, 'lxml').html.body
    
    header = soup.find('div', id='mw-category-media')
    
    for li in header.ul.find_all('li'):
        image_page_url = 'https://archives.bulbagarden.net' + li.a['href']
        cache_name = li.find_all('a')[1].text.strip().replace(' ', '-')
        print('Processing {}'.format(cache_name))
        
        image_page_filename = cache_path + '{}.html'.format(cache_name)
        contents = fetch_or_download(image_page_filename, image_page_url)
        soup = BeautifulSoup(contents, 'lxml').html.body
        
        div = soup.find('div', id='mw-content-text')
        image_url = 'https:' + div.contents[1].a['href']
        
        image_name = sanitize_bulbapedia_image_name(cache_name)
        image_filename = image_path + image_name
        print(image_name)
        download_image(image_url, image_filename)

def main():
    pass

if __name__ == '__main__':
    main()
