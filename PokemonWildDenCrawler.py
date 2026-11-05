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

CACHE_FOLDER = 'Cached/Locations/WildDen/'
URLS = [
    {
        'name': 'Watchtower Ruins',
        'url': 'https://bulbapedia.bulbagarden.net/wiki/Watchtower_Ruins/Dens'
    },
    {
        'name': 'East Lake Axewell',
        'url': 'https://bulbapedia.bulbagarden.net/wiki/East_Lake_Axewell/Dens'
    },
    {
        'name': 'Axew\'s Eye',
        'url': 'https://bulbapedia.bulbagarden.net/wiki/Axew%27s_Eye/Dens'
    },
    {
        'name': 'North Lake Miloch',
        'url': 'https://bulbapedia.bulbagarden.net/wiki/North_Lake_Miloch/Dens'
    },
    {
        'name': 'West Lake Axewell',
        'url': 'https://bulbapedia.bulbagarden.net/wiki/West_Lake_Axewell/Dens'
    },
    {
        'name': 'Dappled Grove',
        'url': 'https://bulbapedia.bulbagarden.net/wiki/Dappled_Grove/Dens'
    },
    {
        'name': 'Rolling Fields',
        'url': 'https://bulbapedia.bulbagarden.net/wiki/Rolling_Fields/Dens'
    },
    {
        'name': 'South Lake Miloch',
        'url': 'https://bulbapedia.bulbagarden.net/wiki/South_Lake_Miloch/Dens'
    },
    {
        'name': 'Giant\'s Seat',
        'url': 'https://bulbapedia.bulbagarden.net/wiki/Giant%27s_Seat/Dens'
    },
    {
        'name': 'Lake of Outrage',
        'url': 'https://bulbapedia.bulbagarden.net/wiki/Lake_of_Outrage/Dens'
    },
    {
        'name': 'Hammerlocke Hills',
        'url': 'https://bulbapedia.bulbagarden.net/wiki/Hammerlocke_Hills/Dens'
    },
    {
        'name': 'Giant\'s Cap',
        'url': 'https://bulbapedia.bulbagarden.net/wiki/Giant%27s_Cap/Dens'
    },
    {
        'name': 'Dusty Bowl',
        'url': 'https://bulbapedia.bulbagarden.net/wiki/Dusty_Bowl/Dens'
    },
    {
        'name': 'Giant\'s Mirror',
        'url': 'https://bulbapedia.bulbagarden.net/wiki/Giant%27s_Mirror/Dens'
    },
    {
        'name': 'Stony Wilderness',
        'url': 'https://bulbapedia.bulbagarden.net/wiki/Stony_Wilderness/Dens'
    },
    {
        'name': 'Bridge Field',
        'url': 'https://bulbapedia.bulbagarden.net/wiki/Bridge_Field/Dens'
    },
    {
        'name': 'Motostoke Riverbank',
        'url': 'https://bulbapedia.bulbagarden.net/wiki/Motostoke_Riverbank/Dens'
    },
]

def process_entry_table(table):
    den_entries = []
    for row in table.find_all('tr')[2:]:
        entry = {}
        
        pokemon_node = row.td
        if pokemon_node.span is None:
            continue
        pokemon = pokemon_node.span.text.strip()
        form_node = pokemon_node.small
        if form_node is not None:
            form = form_node.span.text.strip()
        else:
            form = ''
        print('Found Pokemon {}: {}'.format(pokemon, form))
        
        entry['pokemon'] = pokemon
        entry['form'] = form
        
        sword_node = pokemon_node.find_next_sibling()
        shield_node = sword_node.find_next_sibling()
        
        entry['sword'] = '#FFF' not in sword_node['style']
        entry['shield'] = '#FFF' not in shield_node['style']
        
        star_nodes = row.find_all('td')[-5:]
        if len(star_nodes) != 5:
            sys.exit(1)
        
        entry['one'] = star_nodes[0].text.strip()
        entry['two'] = star_nodes[1].text.strip()
        entry['three'] = star_nodes[2].text.strip()
        entry['four'] = star_nodes[3].text.strip()
        entry['five'] = star_nodes[4].text.strip()
        
        den_entries.append(entry)
    
    return den_entries

def process_file(contents):
    soup = BeautifulSoup(contents, 'lxml').html.body
    entries = {}
    
    body = soup.find('div', id='bodyContent')
    
    h2s = body.find_all('h2')
    for h2 in h2s:
        if h2.span is None:
            print('error 1')
            continue
        den_name = h2.span.text.strip()
        if len(den_name) > 1:
            print('error 2')
            continue
        
        # Common pool
        h3 = h2.find_next_sibling('h3')
        if h3.name != 'h3' or h3.span is None:
            print('error 3')
            continue
        den_pool_name = h3.span.text.strip()
        
        den_entries = {}
        
        table = h3.find_next_sibling('h4').find_next_sibling('h4').find_next_sibling('table')
        if table.name != 'table':
            print('error 4')
            continue
        
        den_pool_entries = process_entry_table(table)
        den_entries[den_pool_name] = den_pool_entries
        
        # Rare pool
        h3 = table.find_next_sibling().find_next_sibling()
        if h3.name != 'h3' or h3.span is None:
            print('error 5')
            continue
        den_pool_name = h3.span.text.strip()
        
        table = h3.find_next_sibling('h4').find_next_sibling('h4').find_next_sibling('table')
        if table.name != 'table':
            print('error 6')
            continue
        
        den_pool_entries = process_entry_table(table)
        den_entries[den_pool_name] = den_pool_entries
        
        entries[den_name] = den_entries
                
    return entries

def main():
    all_entries = {}
    
    for url_dict in URLS:
        name = url_dict['name']
        print('Processing {}'.format(name))
        
        url = url_dict['url']
        filename = '{}{}.html'.format(CACHE_FOLDER, name)
        contents = crawler.fetch_or_download(filename, url)
        entries = process_file(contents)
        all_entries[name] = entries
    
    crawler.write_data_to_file(all_entries, "Data/PokemonWildDen")
#    print(all_entries)
    print("Done!")

if __name__ == '__main__':
    main()
