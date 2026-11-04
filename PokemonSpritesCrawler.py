#!/usr/bin/env python3 -tt
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import os
import pprint
import sys
import json
import shutil
import codecs
import CrawlerUtils as crawler

def process_file(name, contents):
    soup = BeautifulSoup(contents, 'lxml')

    body = soup.html.body

    tds = body.find_all("td", class_="pkmn")
    for td in tds:
        img = td.img
        if img is None:
            continue
        
        path = img["src"]
        if path is None or not path.endswith(".png"):
            print("Not an image")
            continue

        sprite_link = "http://www.serebii.net" + path
        print("Found sprite link: " + sprite_link)

        filename = "Artwork/RawSprites/" + name + "-sprite.png"
        if os.path.isfile(filename):
            print("Already downloaded image, skipping")
            return

        response = requests.get(sprite_link, stream=True)
        with open(filename, 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)
        del response

        break

    return

def process_sprite(page_name, filename, url):
    contents = crawler.fetch_or_download(filename, url)
    if contents is None:
        return

    process_file(page_name, contents)

def main():
    print("This is the Pokepedia Pokemon Crawler")

    page_names = []
    for i in range(1, 810):
        page_names.append('{:0>3}'.format(str(i)))
    
    swsh_page_names = []
    for i in range(810, 891):
        swsh_page_names.append('{:0>3}'.format(str(i)))
    
    for page_name in page_names:
        filename = "Cached/Serebii/{0}.html".format(page_name)
        url = "http://www.serebii.net/pokedex-sm/{0}.shtml".format(page_name)
        process_sprite(page_name, filename, url)
    
    for page_name in swsh_page_names:
        filename = "Cached/Serebii/{0}.html".format(page_name)
        url = "http://www.serebii.net/pokedex-swsh/{0}.shtml".format(page_name)
        process_sprite(page_name, filename, url)
        
if __name__ == '__main__':
    main()
