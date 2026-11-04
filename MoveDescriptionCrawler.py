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

def process_move(contents):
    entries = {}
    soup = BeautifulSoup(contents, 'lxml').html.body
    header = soup.find('h2', id='move-descr')
    if not header:
        return entries
    table_parent = header.find_next_sibling()
    if not table_parent:
        return entries
    table = table_parent.table
    rows = table.find_all('tr')
    for row in rows:
        game_nodes = row.th.find_all('span')
        description = row.td.text.strip()
        for game_node in game_nodes:
            game_name = game_node.text.strip()
            entries[game_name] = description
    
    return entries

def main():
    print("This is the Pokepedia Moves Crawler")

    all_entries = {}
    
    file_path = 'Cached/PokemonDBMoves/'
    
    filename = "Cached/PokemonDBMoves/_AllMoves.html"
    url = "https://pokemondb.net/move/all"
    contents = crawler.fetch_or_download(filename, url)
    soup = BeautifulSoup(contents, 'lxml').html.body
    table = soup.find('table', id='moves')
    
    for row in table.tbody.find_all('tr'):
        cells = row.find_all('td')
        name = cells[0].text.strip()
        
        move = name.strip().replace(' ', '-').replace('\'', '').replace(',', '')
        
        print("Processing " + move)
    
        filename = file_path + '{}.html'.format(move)
        url = 'https://pokemondb.net/move/' + move
        
        contents = crawler.fetch_or_download(filename, url)
        entries = process_move(contents)
        
        dict_name = re.sub(r'[^a-zA-Z0-9]', '', name).lower()
        all_entries[dict_name] = entries

    crawler.write_data_to_file(all_entries, "Data/MoveDescriptions")
#   print(all_entries)
    print("Done!")

if __name__ == '__main__':
    main()
    