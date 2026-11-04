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

def main():
	print("This is the Pokepedia Moves Crawler")
	
	filename = "Cached/_PokemonDBAllAbilities.html"
	url = "https://pokemondb.net/ability"
	contents = crawler.fetch_or_download(filename, url)
	soup = BeautifulSoup(contents, 'lxml').html.body
	table = soup.find('table', id='abilities')
	
	pokemon = set()
	for row in table.tbody.find_all('tr'):
		cell = row.td.a
		name = cell.text.strip()
		urlPath = cell['href']
		
		url = 'https://pokemondb.net' + urlPath
		print(url)
		
	print("Done!")
	
if __name__ == '__main__':
	main()
	