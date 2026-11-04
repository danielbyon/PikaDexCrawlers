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
import PokemonDB as pdb

def process_file(contents):
    soup = BeautifulSoup(contents, 'lxml').html.body
    entries = {}
    
    table = soup.main.h1
    if table is None:
        return None
    table = table.find_next_sibling('h2')
    if table is None:
        return None 
    table = table.find_next_sibling().table
    for row in table.find_all('tr'):
        description = row.td.text.strip()
        for game_node in row.find_all('span'):
            game = game_node.text.strip()
            entries[game] = description
    
    return entries

def main():
    print('This is the Pokepedia Items Crawler')

    all_entries = {}
    
    file_path = 'Cached/Items/PokemonDB/'
    
    filename = file_path + '_AllItems.html'
    url = 'https://pokemondb.net/item/all'
    contents = crawler.fetch_or_download(filename, url)
    soup = BeautifulSoup(contents, 'lxml').html.body
    
    for row in soup.table.find_all('tr'):
        link = row.a
        if link is None:
            continue
        name = link.text.strip()
        print('Processing {}'.format(name))
        
        url = 'https://pokemondb.net' + link['href']
        
#       print('{}\t{}'.format(name, url)) # Used for external links
        
        filename = file_path + '{}.html'.format(name.replace(' ', '-'))
        contents = crawler.fetch_or_download(filename, url)
        entries = process_file(contents)
        if entries:
            all_entries[name] = entries
        
    
    filename = file_path + '_AllKeyItems.html'
    url = 'https://pokemondb.net/item/type/key'
    contents = crawler.fetch_or_download(filename, url)
    soup = BeautifulSoup(contents, 'lxml').html.body
    
    for row in soup.table.find_all('tr'):
        link = row.a
        if link is None:
            continue
        name = link.text.strip()
        print('Processing {}'.format(name))
        
        url = 'https://pokemondb.net' + link['href']
        
#       print('{}\t{}'.format(name, url)) # Used for external links
        
        filename = file_path + '{}.html'.format(name.replace(' ', '-'))
        contents = crawler.fetch_or_download(filename, url)
        entries = process_file(contents)
        if entries:
            entries['pokemonDBURL'] = url
            all_entries[name] = entries
        
    crawler.write_data_to_file(all_entries, "Data/PokemonDBItems")
#    print(all_entries)
    print("Done!")

if __name__ == '__main__':
    main()
    