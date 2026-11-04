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

ITEMS_TO_SKIP = [
    u'ぅ',
    '4',
    '$ ぅ',
    'Cancel',
    'Nothing',
    'unknown',
    'None',
    'Medicine Pocket',
    'Candy Jar',
    'Power-Up Pocket',
    'Clothing Trunk',
    'Catching Pocket',
    'Battle Pocket',
    '[[]]',
]

def sanitize_pocket_name(name):
    if '24px' in name:
        return "other items"
    else:
        return name

def process_file(contents, item_name):
    soup = BeautifulSoup(contents, 'lxml').html.body
    entries = {}
    
    outer_table = soup.find('div', id='mw-content-text')
    
    # Generation introduced
    for td in outer_table.find_all('td'):
        text = td.text.strip()
        if "Introduced in" not in text:
            continue
        
        if "Introduced in Generation I\n" in text:
            entries['generationIntroduced'] = '1'
        elif "Introduced in Generation II\n" in text:
            entries['generationIntroduced'] = '2'
        elif "Introduced in Generation III\n" in text:
            entries['generationIntroduced'] = '3'
        elif "Introduced in Generation IV\n" in text:
            entries['generationIntroduced'] = '4'
        elif "Introduced in Generation V\n" in text:
            entries['generationIntroduced'] = '5'
        elif "Introduced in Generation VI\n" in text:
            entries['generationIntroduced'] = '6'
        elif "Introduced in Generation VII\n" in text:
            entries['generationIntroduced'] = '7'
        elif "Introduced in Generation VIII\n" in text:
            entries['generationIntroduced'] = '8'
        elif "Introduced in Generation IX\n" in text:
            entries['generationIntroduced'] = '9'
        
        break
    
    # Pocket
    for th in outer_table.find_all('th'):
        if th.text.strip() != 'Pocket':
            continue
        
        pocket = {}
        for row in th.parent.find_next_siblings('tr'):
            gen = row.th.text.strip()
            if row.td.sup is not None or row.td.small is not None:
                if row.td.small is not None:
                    to_remove = row.td.small.text.strip()
                else:
                    to_remove = row.td.sup.text.strip()
                name = row.td.text.strip().replace(to_remove, '').strip().lower()
                name = sanitize_pocket_name(name)
                
                games = pdb.parse_game_titles(row.td)
                if games:
                    for game in pdb.parse_game_titles(row.td):
                        pocket[game] = name
                else:
                    pocket[gen] = name
            else:
                name = row.td.text.strip().lower()
                name = sanitize_pocket_name(name)
                pocket[gen] = name
        if not pocket:
#           print("Invalid pocket entries")
            return None
        entries['pocket'] = pocket
        break
        
    # Price
    price_header = outer_table.find('span', id='Price')
    if price_header is not None:
        for table_candidate in price_header.parent.find_next_siblings('table'):
            if table_candidate.table is None:
                continue
        
            price = {}
            for row in table_candidate.table.find_all('tr')[1:]:
                tds = row.find_all('td')
                cost = tds[1].text.strip().replace(',', '')
                sell = tds[2].text.strip().replace(',', '')
                
                game_price = {}
                game_price['cost'] = cost
                game_price['sell'] = sell
                
                pdb.parse_game_specific_values(tds[0], price, game_price)
            
            if not price:
#               print("Invalid price entries")
                return None
            entries['prices'] = price
            break
    
    # Description
    description_header = outer_table.find('span', id='Description')
    if description_header is not None:
        for table_candidate in description_header.parent.find_next_siblings('table'):
            if table_candidate.table is None:
                continue
            
            descriptions = {}
            for row in table_candidate.table.find_all('tr')[1:]:
                tds = row.find_all('td')
                
                description = tds[1].text.strip()
                
                pdb.parse_game_specific_values(tds[0], descriptions, description)
            
            if not descriptions:
#               print("Invalid descriptions entries")
                return None
            entries['descriptions'] = descriptions
            break
    
    if not 'pocket' in entries:
        return None
    if not 'descriptions' in entries:
        return None
    return entries

def entryExists(name, all_entries):
    for entry in all_entries:
        if entry['name'] == name:
            return True
    return False

def addItems(gen, filename, url, link_column, items, items_set, skip_asterisk):
    contents = crawler.fetch_or_download(filename, url)
    soup = BeautifulSoup(contents, 'lxml').html.body
    
    outer_table = soup.h1.find_next_sibling().table
    if 'This article is incomplete' in outer_table.text:
        outer_table = outer_table.find_next_sibling().find_next_sibling().find_next_sibling()
    
    if gen == '2':
        outer_table = outer_table.find_next_sibling('table')
    
    for row in outer_table.table.tbody.find_all("tr")[1:]:
        td = row.find_all("td")[link_column]
        name = td.text.strip()
        if name in items_set:
            continue
        if '?' in name or '★' in name or name in ITEMS_TO_SKIP:
#           print('skipping item: {}'.format(name))
            continue
        if '*' in name:
            if skip_asterisk:
#               print('skipping item: {}'.format(name))
                continue
            else:
                name = name.replace('*', '')
        
        link = td.a['href']
        item_url = 'https://bulbapedia.bulbagarden.net' + link
        
        item = {
            'name': name,
#           'generationIntroduced': gen,
            'url': item_url,
        }
        items.append(item)
        items_set.add(name)

def main():
    print('This is the Pokepedia Items Crawler')

    all_entries = []
    
    file_path = 'Cached/Items/Bulbapedia/'
    
    items = []
    items_set = set()
    
    addItems(
        '9',
        file_path + '_AllItemsGen9.html',
        'https://bulbapedia.bulbagarden.net/wiki/List_of_items_by_index_number_(Generation_IX)',
        3,
        items,
        items_set,
        False
    )
    
    addItems(
        '8',
        file_path + '_AllItemsGen8.html',
        'https://bulbapedia.bulbagarden.net/wiki/List_of_items_by_index_number_(Generation_VIII)',
        3,
        items,
        items_set,
        False
    )
    
    addItems(
        '7',
        file_path + '_AllItemsGen7.html',
        'https://bulbapedia.bulbagarden.net/wiki/List_of_items_by_index_number_(Generation_VII)',
        3,
        items,
        items_set,
        False
    )
    
    addItems(
        '6',
        file_path + '_AllItemsGen6.html',
        'https://bulbapedia.bulbagarden.net/wiki/List_of_items_by_index_number_(Generation_VI)',
        3,
        items,
        items_set,
        False
    )
    
    addItems(
        '5',
        file_path + '_AllItemsGen5.html',
        'https://bulbapedia.bulbagarden.net/wiki/List_of_items_by_index_number_(Generation_V)',
        3,
        items,
        items_set,
        False
    )
    
    addItems(
        '4',
        file_path + '_AllItemsGen4.html',
        'https://bulbapedia.bulbagarden.net/wiki/List_of_items_by_index_number_(Generation_IV)',
        3,
        items,
        items_set,
        False
    )
    
    addItems(
        '3',
        file_path + '_AllItemsGen3.html',
        'https://bulbapedia.bulbagarden.net/wiki/List_of_items_by_index_number_(Generation_III)',
        3,
        items,
        items_set,
        False
    )
    
    addItems(
        '2',
        file_path + '_AllItemsGen2.html',
        'https://bulbapedia.bulbagarden.net/wiki/List_of_items_by_index_number_(Generation_II)',
        2,
        items,
        items_set,
        False
    )
    
    addItems(
        '1',
        file_path + '_AllItemsGen1.html',
        'https://bulbapedia.bulbagarden.net/wiki/List_of_items_by_index_number_(Generation_I)',
        2,
        items,
        items_set,
        True
    )
    
    for item in items:
        name = item['name']
        # Special case rename
        if name == "Adventure Guide":
            name = "Adventure Rules"
        
        url = item['url']
        
        filename = file_path + '{}.html'.format(name.replace(' ', '-'))
        
        print('Processing {}'.format(name))
        
        contents = crawler.fetch_or_download(filename, url)
        entries = process_file(contents, name)
        if entries:
            entries['name'] = name
            entries['imageName'] = name.replace(' ', '-').lower()
            entries['bulbapediaURL'] = url
            all_entries.append(entries)
            
    crawler.write_data_to_file(all_entries, "Data/BulbapediaItems")
#    print(all_entries)
    print("Done!")

if __name__ == '__main__':
    main()
    