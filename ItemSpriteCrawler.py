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
import re

def main():
    print('This is the Pokepedia Item Sprite Crawler')

    file_path = 'Cached/Items/Bulbapedia/'
    image_path = 'Artwork/RawItems/Sprites/'
    
    filename = file_path + '_AllItems.html'
    url = 'https://bulbapedia.bulbagarden.net/wiki/List_of_items_by_name'
    contents = crawler.fetch_or_download(filename, url)
    soup = BeautifulSoup(contents, 'lxml').html.body
    
    for h3 in soup.h2.find_next_siblings('h3'):
        table = h3.find_next_sibling('table')
        
        for row in table.find_all('tr'):
            if row.td is None:
                continue
            
            tds = row.find_all('td')
            if len(tds) != 4:
                print('invalid row')
                continue
            
            url = 'http:' + tds[0].img['src']
            cache_name = tds[1].a['title'].replace(' ', '-').lower()
            
            print('Processing {}: {}'.format(cache_name, url))
            
            filename = image_path + '{}.png'.format(cache_name)
            crawler.download_image(url, filename)
        
    print("Done!")

if __name__ == '__main__':
    main()
