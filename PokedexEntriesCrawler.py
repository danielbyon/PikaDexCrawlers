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

pokedexEntriesKeys = ['Pok.C3.A9dex_entries', 'Pok.C3.A9dex_entries_2', 'Pok.C3.A9dex_entries_3', 'Pok.C3.A9dex_entries_4']

def process_table(outer_table):
    entries = {}
    
    previous_entry = ""
    if outer_table.tbody is None:
        return entries
    
    for tr in outer_table.tbody("tr", recursive=False):
        generation_body_td = tr.td
        if generation_body_td is None:
            # Usually this means this pokemon was unavailable in a specific generation, so there are no entries
            continue

        generation_body = generation_body_td.table.tbody.find_all("tr", recursive=False)[1].td.table

        if generation_body is None:
            continue

        for row in generation_body.tbody.find_all("tr", recursive=False):
            header = row.th.a
            if header is None:
                continue
            header_span = header.span
            if header_span is None:
                continue
            game_name = header_span.text.strip()

            # We don't support Pokemon Stadium/Colosseum
            if game_name.startswith("Stadium") or game_name.startswith("Colosseum"):
                continue
                
            key = game_name

            entry_node = row.td
            if entry_node is not None:                
                entry = entry_node.text.strip()
                entries[key] = entry
                previous_entry = entry
            else:
                entries[key] = previous_entry
                
    return entries

def process_file(index, name, contents):
    soup = BeautifulSoup(contents, 'lxml')
    allFormEntries = []
    
    for outer_table in soup.html.body.find_all('span', id=re.compile('Pok.C3.A9dex_entries*')):
        if outer_table is None:
            continue
            
        outer_table = outer_table.find_parent().find_next_sibling()
        form_name = None
        
        while True:
            if outer_table.name != u"table":
                if outer_table.name == u"h4":
                    form_name = outer_table.span.text.strip()
                resolved_table = outer_table.find_next_sibling()
            else:
                resolved_table = outer_table
            
            entries = process_table(resolved_table)
            
            if entries:
                entries['number'] = index
                entries['name'] = name
                if form_name:
                    entries['formName'] = form_name
                else:
                    entries['formName'] = name
                
                allFormEntries.append(entries)
            
            if form_name:
                outer_table = resolved_table.find_next_sibling()
                if outer_table is None:
                    break
                if outer_table.name == u'br':
                    outer_table = outer_table.find_next_sibling()
                if outer_table.name != u'h4':
                    break
            else:
                break

    if not allFormEntries:
        print("Empty entries for {}".format(name))
        sys.exit(1)

    return allFormEntries

def main():
    print("This is the Pokepedia Pokemon Crawler")

    all_entries = []
    index = 0
    with codecs.open("PokemonList.txt", 'r', encoding='utf8') as f:
        for line in f:
            index += 1
            pokemon = line.strip().replace(' ', '_')
            
            print(u"Processing {} - {}".format(index, pokemon))

            filename = u"Cached/Pokemon/{:04d}-{}.html".format(index, pokemon.rstrip('.'))

            url = u"http://bulbapedia.bulbagarden.net/wiki/" + pokemon + u"_(Pokémon)"
            contents = crawler.fetch_or_download(filename, url)
            if contents is None:
                continue

            allFormEntries = process_file(index, pokemon, contents)
            for entries in allFormEntries:
                all_entries.append(entries)

    fieldnames = [u'number', u'name', u'formName', u'Red', u'Blue', u'Yellow', u'Gold', u'Silver', u'Crystal', u'Ruby', u'Sapphire', u'Emerald', u'FireRed', u'LeafGreen', u'Diamond', u'Pearl', u'Platinum', u'HeartGold', u'SoulSilver', u'Black', u'White', u'Black 2', u'White 2', u'X', u'Y', u'Omega Ruby', u'Alpha Sapphire', u'Sun', u'Moon', u'Ultra Sun', u'Ultra Moon', u'Let\'s Go Pikachu', u'Let\'s Go Eevee', u'Sword', u'Shield', u'Brilliant Diamond', u'Shining Pearl', u'Scarlet', u'Violet']
    crawler.write_entries_to_tsv(all_entries, fieldnames, "Data/PokedexEntries")
    
    all_games = [u'Red', u'Blue', u'Yellow', u'Gold', u'Silver', u'Crystal', u'Ruby', u'Sapphire', u'Emerald', u'FireRed', u'LeafGreen', u'Diamond', u'Pearl', u'Platinum', u'HeartGold', u'SoulSilver', u'Black', u'White', u'Black 2', u'White 2', u'X', u'Y', u'Omega Ruby', u'Alpha Sapphire', u'Sun', u'Moon', u'Ultra Sun', u'Ultra Moon', u'Let\'s Go Pikachu', u'Let\'s Go Eevee', u'Sword', u'Shield', u'Brilliant Diamond', u'Shining Pearl', u'Scarlet', u'Violet']
    all_vertical_entries = []
    for entries in all_entries:
        for game in all_games:
            if game not in entries:
                continue
            
            value = entries[game]
            
            modified = {}
            modified[u'number'] = entries[u'number']
            modified[u'name'] = entries[u'name']
            modified[u'formName'] = entries[u'formName']
            modified[u'game'] = game
            modified[u'entry'] = value
            all_vertical_entries.append(modified)
    all_vertical_fieldnames = [u'number', u'name', u'formName', u'game', u'entry']
    crawler.write_entries_to_tsv(all_vertical_entries, all_vertical_fieldnames, "Data/PokedexEntries-Vertical")

if __name__ == '__main__':
    main()
