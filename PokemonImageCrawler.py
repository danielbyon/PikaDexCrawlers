#!/usr/bin/env python3 -tt
# coding=utf8

import requests
from bs4 import BeautifulSoup
import os
import pprint
import sys
import json
import shutil
import CrawlerUtils as crawler

def process_file(name, contents):
    soup = BeautifulSoup(contents, 'lxml')
    
    body = soup.html.body
    
    sprite_link = body.find('div', class_='fullMedia').a['href'].strip()
    if sprite_link is None:
        print("Failed to get sprite link, skipping")

    print("Found sprite link: " + sprite_link)

    filename = "Artwork/RawImages/" + name[:3] + "-image.png"
    if os.path.isfile(filename):
        print("Already downloaded image, skipping")
        return

    full_link = "https:" + sprite_link
    response = requests.get(full_link, stream=True)
    with open(filename, 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)
    del response

def main():
    print("This is the Pokepedia Pokemon Crawler")

    with open("PageNames.txt", "r") as f:
        for line in f:
            page_name = line.strip().replace('♀', '').replace('♂', '').replace(' ', '_')
            if page_name.startswith("487"):
                page_name = page_name + "-Altered"
            elif page_name.startswith("492"):
                page_name = page_name + "-Land"
            elif page_name.startswith("585") or page_name.startswith("586"):
                page_name = page_name + "-Spring"
            elif page_name.startswith("741"):
                page_name = page_name + "-Baile"
            elif page_name.startswith("746"):
                page_name = page_name + "-Solo"
            
            print(u"====================")
            print(u"Processing " + page_name)

            filename = u"Cached/PokemonImages/" + page_name.rstrip('.') + ".html"

            url = u"http://bulbapedia.bulbagarden.net/wiki/File:" + page_name.rstrip('.') + ".png"
            contents = crawler.fetch_or_download(filename, url)
            if contents is None:
                continue

            process_file(page_name, contents)

    pass

if __name__ == '__main__':
    main()
