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

DASH = '\u2014'

def process_file(name, contents):
    soup = BeautifulSoup(contents, 'lxml').html.body.find(id='mw-content-text')
#    soup = BeautifulSoup(contents, 'lxml').html.body.div.find(id='mw-content-text')
    entries = {}
    
    node = soup.font.b.text
    if node is None:
        print("--- Not found")

    ### Type
    type = soup.find('a', title='Type').find_parent().find_next_sibling().a.text.strip()
    if type is not None:
        entries['type'] = type
    
    ### Category
    category = soup.find('a', title='Damage category').find_parent().find_next_sibling().a
    if category is not None:
        category = category.text.strip()
        if category is not None:
            entries['category'] = category

    ### Max PP
    ppNode = soup.find('a', title='PP').find_parent().find_next_sibling()
    maxPPNode = ppNode.small
    maxPP = ""
    if maxPPNode is not None:
        maxPP = maxPPNode.text.lstrip('(max.').rstrip(')').strip()
        entries['maxPP'] = maxPPNode.text.lstrip('(max.').rstrip(')').strip()
    
    ### PP
    pp = ppNode.text.strip()
    if pp is not None:
        if maxPPNode is not None:
            pp = pp.rstrip(')').rstrip(maxPP).rstrip('(max. ')
        if pp != DASH:
            entries['pp'] = pp
    
    ### Power
    power = soup.find('a', title='Power').find_parent().find_next_sibling().text.strip()
    if power is not None and power != DASH:
        entries['power'] = power

    ### Accuracy
    accuracy = soup.find('a', title='Accuracy').find_parent().find_next_sibling().text.strip().rstrip('%')
    if accuracy is not None and accuracy != DASH:
        entries['accuracy'] = accuracy
    
    ### Generation Introduced
    generationIntroduced = soup.find('a', href=re.compile('[/]wiki[/]Generation'))
    if generationIntroduced is not None:
        entries['generationIntroduced'] = generationIntroduced.text.strip()

    ### Target
    targetNode = soup.find('b', text="Range")
    if targetNode is not None:
        tds = targetNode.find_next_sibling().find_all('td')
        if len(tds) != 7:
            print('Invalid targets')
        
        i = 0
        keys = ['targetFoe1', 'targetFoe2', 'targetFoe3', 'targetSelf', 'targetAlly1', 'targetAlly2']
        for td in tds[:-1]:
            if td.small is None:
                print('Invalid target row')
                print(td)
                continue
            key = keys[i]
            if td['style'].startswith('background: #FF4500') or td['style'].startswith('background: #ED1C24'):
                entries[key] = "1"
            elif td['style'].startswith('background: #709AD1'):
                entries[key] = "0"
            else:
                print("Invalid check, {0}".format(td['style']))
            i += 1
        entries['targetDescription'] = tds[6].small.text.strip()

    ### Descriptions
    descriptionNode = soup.find('span', id='Description', class_='mw-headline')
    if descriptionNode is not None:
        table = descriptionNode.find_parent().find_next_sibling()
        if "This section is incomplete" in table.text:
            table = table.find_next_sibling()
        if table.text == 'Non-Stellar type':
            table = table.find_next_sibling()
        
        trs = table.tr.td.table.find_all('tr')
        for tr in trs[1:]:
            description = tr.find_all('td')[1].text.strip()
            for a in tr.td.find_all('a'):
                title = a['title']
                if title == u'Pokémon Gold and Silver Versions':
                    entries['gold'] = description
                    entries['silver'] = description
                elif title == u'Pokémon Crystal Version':
                    entries['crystal'] = description
                elif title == u'Pokémon Ruby and Sapphire Versions':
                    entries['ruby'] = description
                    entries['sapphire'] = description
                elif title == u'Pokémon Emerald Version':
                    entries['emerald'] = description
                elif title == u'Pokémon FireRed and LeafGreen Versions':
                    entries['fireRed'] = description
                    entries['leafGreen'] = description
                elif title == u'Pokémon Diamond and Pearl Versions':
                    entries['diamond'] = description
                    entries['pearl'] = description
                elif title == u'Pokémon Platinum Version':
                    entries['platinum'] = description
                elif title == u'Pokémon HeartGold and SoulSilver Versions':
                    entries['heartGold'] = description
                    entries['soulSilver'] = description
                elif title == u'Pokémon Black and White Versions':
                    entries['black'] = description
                    entries['white'] = description
                elif title == u'Pokémon Black and White Versions 2':
                    entries['black2'] = description
                    entries['white2'] = description
                elif title == u'Pokémon X and Y':
                    entries['x'] = description
                    entries['y'] = description
                elif title == u'Pokémon Omega Ruby and Alpha Sapphire':
                    entries['omegaRuby'] = description
                    entries['alphaSapphire'] = description
                elif title == u'Pokémon Sun and Moon':
                    entries['sun'] = description
                    entries['moon'] = description
                elif title == u'Pokémon Ultra Sun and Ultra Moon':
                    entries['ultraSun'] = description
                    entries['ultraMoon'] = description
                elif title == u'Pokémon: Let\'s Go, Pikachu! and Let\'s Go, Eevee!':
                    entries['letsGoPikachu'] = description
                    entries['letsGoEevee'] = description
                elif title == u'Pokémon Sword and Shield':
                    entries['sword'] = description
                    entries['shield'] = description
                elif title == u'Pokémon Brilliant Diamond and Shining Pearl':
                    entries['brilliantDiamond'] = description
                    entries['shiningPearl'] = description
                elif title == u'Pokémon Legends: Arceus':
                    entries['legendsArceus'] = description
                elif title == u'Pokémon Scarlet and Violet':
                    entries['scarlet'] = description
                    entries['violet'] = description
                else:
#                   print('Unsupported game: {}'.format(title))
                    pass
    
    return entries

def main():
    print("This is the Pokepedia Moves Crawler")

    all_entries = {}    
    i = 0
    
    filename = "Cached/PokemonDBMoves/_AllMoves.html"
    url = "https://pokemondb.net/move/all"
    contents = crawler.fetch_or_download(filename, url)
    soup = BeautifulSoup(contents, 'lxml').html.body
    table = soup.find('table', id='moves')
    
    for row in table.tbody.find_all('tr'):
        cells = row.find_all('td')
        name = cells[0].text.strip()
        
        move = name.strip().replace(' ', '_').replace('\'', '').rstrip('.')
        
        print("Processing " + move)
        
        filename = "Cached/Moves/" + move + ".html"
        
        url = "http://bulbapedia.bulbagarden.net/wiki/" + move + "_(move)"
        contents = crawler.fetch_or_download(filename, url)
        if contents is None:
            continue
        
        entries = process_file(move, contents)
        if entries is not None:
            entries["number"] = "{}".format(i)
        all_entries[name.strip()] = entries
        
        i += 1
    
#   with codecs.open("MovesList.txt", 'r', encoding='utf8') as f:
#       for line in f:
#           move = line.strip().replace(' ', '_').rstrip('.')
#
#           print("Processing " + move)
#
#           filename = "Cached/Moves/" + move + ".html"
#
#           url = "http://bulbapedia.bulbagarden.net/wiki/" + move + "_(move)"
#           contents = crawler.fetch_or_download(filename, url)
#           if contents is None:
#               continue
#
#           entries = process_file(move, contents)
#           if entries is not None:
#               entries["number"] = "{}".format(i)
#           all_entries[line.strip()] = entries
#           
#           i += 1

    crawler.write_data_to_file(all_entries, "Data/Moves")
    pass

if __name__ == '__main__':
    main()
    