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
    print('This is the Pokepedia Pokemon Sprite Crawler')

    file_path = 'Cached/Pokemon/'
    image_path = 'Artwork/RawSpritesNationalList/'
    
    filename = file_path + '_AllPokemon.html'
    url = 'https://bulbapedia.bulbagarden.net/wiki/List_of_Pok%C3%A9mon_by_National_Pok%C3%A9dex_number'
    contents = crawler.fetch_or_download(filename, url)
    soup = BeautifulSoup(contents, 'lxml').html.body
    
    h2 = soup.find('span', id='List_of_Pok.C3.A9mon_by_National_Pok.C3.A9dex_number').parent
    
    for h3 in h2.find_next_siblings('h3'):
        table = h3.find_next_sibling('table')
        
        for row in table.find_all('tr')[1:]:
            url = 'http:' + row.img['src']
            cache_name = url.split('/')[-1].replace('MS', '').replace('XY', '').rstrip('.png')
            
            print('Processing {}: {}'.format(cache_name, url))
            
            filename = image_path + '_ByNumber/{}-sprite.png'.format(cache_name)
            crawler.download_image(url, filename)
                    
    print("Done!")

if __name__ == '__main__':
    main()
