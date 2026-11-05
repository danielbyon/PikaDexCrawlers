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
import csv
import re

def process_file(name, contents):
    soup = BeautifulSoup(contents, 'lxml').html.body
    entries = {}
    
    # Base Experience Yield
    base_xp_yield_node = soup.find("a", title="Experience").find_parent().find_next_sibling().tr
    for node in base_xp_yield_node.find_all("td"):
        if 'style' in node.attrs and node['style'] == "display:none;":
            continue
        
        header_node = node.small
        header = None
        if header_node is not None:
            header = header_node.text.strip()
        
        key = 'xp'
        if header is not None:
            key = '{}-{}'.format(key, header)
            
        entries[key] = node.text.strip()
    
    # Species
    species_node = soup.find("a", title="Pokémon category").span
    if species_node is None:
        print("could not find species node")
        return
    
    species_components = species_node.text.strip().split(" ")
    if len(species_components) < 2:
        print("species text invalid: " + species_node.text)
        return

    species_text = " ".join(species_components[:-1])
    entries["species"] = species_text

    # Height
    height_imp_node = soup.find("a", title="List of Pokémon by height").find_parent().find_next_sibling().tr
    if height_imp_node is None:
        print("could not find height (imperial) node")
        return
    
    tds = height_imp_node.find_all("td")
    metric = tds[1].text.strip()

    meters = metric.split(" ")[0]
    entries["heightMeters"] = meters
    
    # Weight
    weight_imp_node = soup.find("a", title="Weight").find_parent().find_next_sibling().tr
    if weight_imp_node is None:
        print("could not find weight (imperial) node")
        return
    
    tds = weight_imp_node.find_all("td")
    metric_weight = tds[1].text.strip()

    kilograms = metric_weight.split(" ")[0]
    entries["weightKilograms"] = kilograms

    # Catch rate
    catch_rate_node = soup.find("a", title="Catch rate").find_parent().find_next_sibling().tr
    if catch_rate_node is None:
        print("could not find catch rate node")
        return
    catch_rate_components = catch_rate_node.text.strip().split(" ")
    entries["catchRate"] = catch_rate_components[0]
    entries["catchRatePercentage"] = catch_rate_components[1].lstrip("(").rstrip("%)")

    # Egg group
    egg_group_node = soup.find("a", title="Egg Group").find_parent().find_next_sibling().tr
    if egg_group_node is None:
        print("could not find egg group node")
        return
    raw_egg_group_text = egg_group_node.text.strip().replace('\xa0', ' ')
    entries["eggGroup"] = ",".join(raw_egg_group_text.split(" and "))

    # Hatch time
    hatch_time_node = soup.find("a", title="Egg cycle").find_parent().find_next_sibling().tr
    if hatch_time_node is None:
        print("could not find hatch time node")
        return
    entries["hatchTime"] = hatch_time_node.text.strip().replace("steps", '').replace('\xa0', '').replace('Egg not obtainable', '')

    # Levelling rate
    levelling_rate_node = soup.find_all("a", title="Experience")[1].find_parent().find_next_sibling().tr
    if levelling_rate_node is None:
        print("could not find levelling rate node")
        return
    entries["levelingRate"] = levelling_rate_node.text.strip()

    # EV yield
    ev_yield_node = soup.find("a", title="List of Pokémon by effort value yield").find_parent().find_next_sibling().find_all('tr')[2]
    if ev_yield_node is None:
        print("could not find EV yield node")
        return
    for td in ev_yield_node.find_all('td'):
        key = td.text.strip()[1:]
        value = td.text.strip()[0]
        entries[key.lstrip('*')] = value.rstrip('*')

    # Color
    color_node = soup.find("a", title="List of Pokémon by color").find_parent().find_next_sibling().tr
    if color_node is None:
        print("could not find color node")
        return
    entries["color"] = color_node.text.strip().replace('Other forms may have other colors.', '')

    # Base friendship
    base_friendship_node = soup.find("a", title="List of Pokémon by base friendship").find_parent().find_next_sibling().tr
    if base_friendship_node is None:
        print("could not find friendship node")
        return
    entries["baseFriendship"] = base_friendship_node.text.strip()

    # Gender ratio
    gender_ratio_node = soup.find("a", title=re.compile("Category:Pokémon with a gender ratio.*"))
    if gender_ratio_node is None:
        gender_ratio_node = soup.find('a', title='List of Pokémon by gender ratio')
        if gender_ratio_node is None:
            print("could not find gender ratio node")
            return
    for node in gender_ratio_node.find_all('span'):
        style = node['style']
        text = node.text.strip().split(' ')[0].rstrip('%')
        if "color:#0000FF;" in style:
            entries["maleRatio"] = text
        else:
            if "color:#FF6060;" in style:
                entries["femaleRatio"] = text

    if not entries:
        print("Empty entries for {}".format(name))
        sys.exit(1)
        
    return entries

def main():
    print("This is the Pokepedia Pokemon Crawler")

    all_entries = []
    index = 0
    with codecs.open("PokemonList.txt", 'r', encoding='utf8') as f:
        for line in f:
            index += 1
            pokemon = line.strip().replace(' ', '_')

            print(u"Processing {} - {}".format(index, pokemon))

            filename = u"Cached/Pokemon/{:03d}-{}.html".format(index, pokemon.rstrip('.'))

            url = u"http://bulbapedia.bulbagarden.net/wiki/" + pokemon + "_(Pokémon)"
            contents = crawler.fetch_or_download(filename, url)
            if contents is None:
                continue

            entries = process_file(pokemon, contents)
            entries['number'] = index
            entries['name'] = line.strip()
            all_entries.append(entries)
            
    fieldnames = ['number', 'name', 'xp', 'xp-Gen. I-III', 'xp-Gen. I-IV', 'xp-Gen. II-III', 'xp-Gen. II-IV', 'xp-Gen. III', 'xp-Gen. III-IV', 'xp-Gen. IV', 'xp-IV', 'xp-V+', 'species', 'heightMeters', 'weightKilograms', 'catchRate', 'catchRatePercentage', 'eggGroup', 'hatchTime', 'levelingRate', 'HP', 'Atk', 'Def', 'Sp.Atk', 'Sp.Def', 'Speed', 'color', 'baseFriendship', 'maleRatio', 'femaleRatio']
    crawler.write_entries_to_tsv(all_entries, fieldnames, "Data/PokemonInfo")

if __name__ == '__main__':
    main()
