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
 
moveset_keys = [
    "gen9",
    "gen1",
    "gen2",
    "gen3",
    "gen4", 
    "gen5",
    "gen6",
    "gen7",
    'gen8'
]
moveset_file_suffixes = [
    "", 
    "-Generation_I_learnset",
    "-Generation_II_learnset",
    "-Generation_III_learnset",
    "-Generation_IV_learnset", 
    "-Generation_V_learnset",
    "-Generation_VI_learnset",
    "-Generation_VII_learnset",
    '-Generation_VIII_learnset'
]
moveset_page_suffixes = [
    "", 
    "/Generation_I_learnset",
    "/Generation_II_learnset",
    "/Generation_III_learnset",
    "/Generation_IV_learnset", 
    "/Generation_V_learnset",
    "/Generation_VI_learnset",
    "/Generation_VII_learnset",
    '/Generation_VIII_learnset'
]

def base_page_name(name):
    return name.strip().replace(' ', '_')

def process_file(key, contents):
    soup = BeautifulSoup(contents, 'lxml').html.body

    entries = {}

    try:
        node = soup.find('span', id='By_breeding')
        if node is None:
            return {}
        
        node = node.find_parent().find_next_sibling('table')
        if node is None:
            return {}

        if key == "gen8":
            table = node.find_all('table')[2]
            children = table.find_all('tr')
        else:
            children = node.find_all('tr')[4:]

        count = 0
        for child in children:
            count += 1
            if count <= 1:
                continue

            pokemons = []
            childTd = child.td
            if childTd is None:
                continue
            for link in child.td.find_all('a'):
                pokemon = link['title']
                if pokemon == "Light Ball":
                    continue
                if pokemon == "000":
                    pokemons = []
                    break
                if pokemon not in pokemons:
                    pokemons.append(pokemon)

            if len(pokemons) == 0:
                continue
            moveNode = child.td.find_next_sibling()
            if moveNode is None:
                continue
            moveNode = moveNode.span
            if moveNode is None:
                continue
            moveName = moveNode.text
            entries[moveName] = pokemons

        return entries
        
    except AttributeError as e:
        print("Error parsing attribute:")
        print(e)
    except IndexError as e:
        print("Index out of range: {}".format(e))
        return {}
    
    return entries

def main():
    print("This is the Pokepedia Pokemon Crawler")

    all_entries = {}
    
    with codecs.open("PokemonList.txt", 'r', encoding='utf8') as f:
        for line in f:
            pokemon_entries = {}
            for i in range(0, len(moveset_keys)):
                pokemon = base_page_name(line)
                file_suffix = moveset_file_suffixes[i]
                page_suffix = moveset_page_suffixes[i]

                print(u"Processing {0}{1}".format(pokemon.encode('ascii', 'ignore').decode('ascii'), file_suffix))

                filename = u"Cached/Learnsets/{0}{1}.html".format(pokemon.rstrip('.'), file_suffix)
                
                url = u"http://bulbapedia.bulbagarden.net/wiki/{0}_(Pokémon){1}".format(pokemon, page_suffix)
                contents = crawler.fetch_or_download(filename, url)
                if contents is None:
                    continue

                key = moveset_keys[i]

                entries = process_file(key, contents)
                pokemon_entries[key] = entries
                
            if not pokemon_entries:
                print(u"Empty entries for {}".format(pokemon))
                sys.exit(1)
            
            all_entries[line.strip()] = pokemon_entries

    crawler.write_data_to_file(all_entries, "Data/LearnsetBreeding")

if __name__ == '__main__':
    main()
