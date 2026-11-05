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

def process_file(name, contents):
    soup = BeautifulSoup(contents, 'lxml')
    entries = {}
    
    try:
        ability_link = soup.html.body.find("a", title="Ability")
        if ability_link is None:
            print("could not find ability link")
            return
        
        table = ability_link.find_parent().find_next_sibling()
        if table is None:
            print("could not find table")
            return

        for td in table.find_all("td"):
            if td.get("style") == "display:none;" or td.get("style") == "display: none":
                continue

            ability = td.a.span.text.strip()

            isHidden = False
            hidden_node = td.small
            if hidden_node is not None:
                small_text = hidden_node.text.strip()
                if small_text == "Hidden Ability":
                    isHidden = True
                elif small_text.startswith("Mega"):
                    # Don't support mega evolutions yet
                    continue

            if isHidden:
                entries["hidden"] = ability
            elif entries.get("first") is None:
                entries["first"] = ability
            else:
                entries["second"] = ability

    except AttributeError as e:
        print("Error parsing attribute:")
        print(e)

    if not entries:
        print("Empty entries for {}".format(name))
        sys.exit(1)
    
    return entries

def main():
    print("This is the Pokepedia Pokemon Crawler")

    all_entries = {}
    
    index = 0
    with codecs.open("PokemonList.txt", 'r', encoding='utf8') as f:
        for line in f:
            index += 1
            pokemon = line.strip().replace(' ', '_')

            print(u"Processing " + pokemon.encode('ascii', 'ignore').decode('ascii'))

            filename = u"Cached/Pokemon/{:03d}-{}.html".format(index, pokemon.rstrip('.'))

            url = u"http://bulbapedia.bulbagarden.net/wiki/" + pokemon + "_(Pokémon)"
            contents = crawler.fetch_or_download(filename, url)
            if contents is None:
                continue

            entries = process_file(pokemon, contents)
            all_entries[line.strip()] = entries

    crawler.write_data_to_file(all_entries, "Data/PokemonAbilities")

if __name__ == '__main__':
    main()
