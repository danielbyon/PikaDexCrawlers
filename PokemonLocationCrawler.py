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

def pokemon_dicts_from_tbody(tbody, generation_num, entries):
    pokemon_dicts = []
    encounter_condition = 'none'
    
    for row in tbody.find_all('tr'):
        if row.th and 'cell-loc-spacer' in row.th['class']:
            continue
        elif row.th and 'cell-loc-status' in row.th['class']:
            encounter_condition = row.th.text.strip()
            continue
        
        tds = row.find_all('td')
        if len(tds) == 0:
            continue
        
        games = []
        game_nodes = row.find_all('td', class_=re.compile('cell-loc-game*'))
        for node in game_nodes:
            if 'cell-loc-game-blank' in node['class']:
                continue
            games.append(node.text.strip())
        
        pokemon_dict = {}
        pokemon_dict['games'] = games
        pokemon_dict['name'] = tds[0].a.text.strip()
        if tds[0].small:
            pokemon_dict['formName'] = tds[0].small.text.strip()
        
        if generation_num == 4 or generation_num == 7:
            times_of_day = []
            for img in tds[3].find_all('img'):
                times_of_day.append(img['title'])
            if times_of_day:
                pokemon_dict['times_of_day'] = times_of_day
        
        # Applies to all generations
        rarity_node = tds[-3]
        if rarity_node.img is not None:
            pokemon_dict['rarity'] = rarity_node.img['title'].strip()
        else:
            pokemon_dict['rarity'] = rarity_node.text.strip()
        
        pokemon_dict['levels'] = tds[-2].text.strip()
        description = tds[-1].text.strip()
        if description != '':
            pokemon_dict['description'] = description
        
        pokemon_dicts.append(pokemon_dict)
    
    entries[encounter_condition] = pokemon_dicts

def process_file(contents):
    soup = BeautifulSoup(contents, 'lxml').html.body
    entries = {}
    
    h2s = soup.find_all('h2')
    for h2 in h2s:
        generation_and_area = h2.text.strip()
        generation_num = int(generation_and_area.split(' ')[1])
        h3 = h2.find_next_sibling()
        if h3 is None:
            continue
        
        area_dict = {}
        while h3 is not None:
            method_dict = {}
            method = h3.text.strip()
            method_description_node = h3.find_next_sibling('p')
            if method_description_node is None:
                break
            method_description = method_description_node.text.strip()
            
            div = h3.find_next_sibling('div')
            if div is None:
                break
            table = div.table
            if table is None:
                break
            tbody = table.tbody
            if tbody is None:
                break
            
            encounter_dict = {}
            pokemon_dicts_from_tbody(tbody, generation_num, encounter_dict)
            
            # Find any encounter condition-specific pokemon
            for tbody in tbody.find_next_siblings('tbody'):
                pokemon_dicts = pokemon_dicts_from_tbody(tbody, generation_num, encounter_dict)
            
            method_dict['pokemon'] = encounter_dict
            method_dict['description'] = method_description
            
            area_dict[method] = method_dict
            
            h3 = div.find_next_sibling()
            if h3 is None or h3.name != 'h3': # hr means we hit the end of the generation block
                break
        
        components = generation_and_area.split(' - ')
        area = None
        if len(components) == 2:
            area = components[-1] # need to handle "L1-L3"-type cases
        else:
            area = 'Main'
        
        if generation_num in entries:
            existing_dict = entries[generation_num]
            existing_dict[area] = area_dict
            entries[generation_num] = existing_dict
        else:
            entries[generation_num] = {
                area: area_dict
            }
        
    return entries

def main():
    print('This is the Pokepedia Moves Crawler')

    all_entries = {}
    
    filename = 'Cached/Locations/PokemonDB/_AllLocations.html'
    url = 'https://pokemondb.net/location'
    contents = crawler.fetch_or_download(filename, url)
    soup = BeautifulSoup(contents, 'lxml').html.body
    
    for tab in soup.find_all('div', id=re.compile('loc-'), class_=re.compile('tabs-panel*')):
        tab_id = tab['id']
        print('Processing region {}'.format(tab_id))
        links = tab.find_all('a')
        
        tab_dict = {}
        for link in links:
            loc_name = link.text.strip()
            print('Processing {}'.format(loc_name))
            
            url = 'https://pokemondb.net' + link['href']
            filename = 'Cached/Locations/PokemonDB/{}/{}.html'.format(tab_id, loc_name.replace('/', '-'))
            
            contents = crawler.fetch_or_download(filename, url)
            soup = BeautifulSoup(contents, 'lxml').html.body
            entries = process_file(contents)
            if entries:
                tab_dict[loc_name] = entries
        
        all_entries[tab_id.lstrip('loc-')] = tab_dict
    
    crawler.write_data_to_file(all_entries, "Data/PokemonLocations")
#    print(all_entries)
    print("Done!")

if __name__ == '__main__':
    main()
