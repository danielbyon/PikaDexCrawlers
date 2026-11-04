#!/usr/bin/env python3
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

def main():
	print("Pokedex entries Crawler")
	
	all_entries = []
	
	filename = "Cached/PokemonDBPokemon/_AllPokemon.html"
	url = "https://pokemondb.net/pokedex/all"
	contents = crawler.fetch_or_download(filename, url)
	soup = BeautifulSoup(contents, 'lxml').html.body
	table = soup.find('table', id='pokedex')
	
	names = set()
	for row in table.tbody.find_all('tr'):		
		cells = row.find_all('td')
		name = cells[1].a.text.strip()
		if name in names:
			# Don't process same Pokemon multiple times (i.e. Mega evolutions)
			continue
		names.add(name)
		
		entry = {}
		
		entry['number'] = cells[0].text.strip()
		entry['name'] = name
		
		type_cells = cells[2].find_all('a')
		entry['primaryType'] = type_cells[0].text.strip()
		if len(type_cells) == 2:
			entry['secondaryType'] = type_cells[1].text.strip()
		
		all_entries.append(entry)
		
		
	fieldnames = [u'number', u'name', u'primaryType', u'secondaryType']
	crawler.write_entries_to_tsv(all_entries, fieldnames, "Data/PokemonTypes")
	
	print("Done!")
	
if __name__ == '__main__':
	main()
	