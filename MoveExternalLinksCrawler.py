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

def main():
	file_path = 'Cached/PokemonDBMoves/'
		
	filename = "Cached/PokemonDBMoves/_AllMoves.html"
	url = "https://pokemondb.net/move/all"
	contents = crawler.fetch_or_download(filename, url)
	soup = BeautifulSoup(contents, 'lxml').html.body
	table = soup.find('table', id='moves')
	
	for row in table.tbody.find_all('tr'):
		cells = row.find_all('td')
		name = cells[0].text.strip()
		urlPath = cells[0].a['href'].strip()
		
		bulbapediaURL = 'http://bulbapedia.bulbagarden.net/wiki/' + name + '_(move)'
		pokemonDBURL = 'https://pokemondb.net' + urlPath
		
		# Sanitize
		bulbapediaURL = bulbapediaURL.replace(" ", "_")
		pokemonDBURL = pokemonDBURL.replace(" ", "_")
		
		# Copy into MoveExternalLinks.numbers and export
		print(name + '\t' + bulbapediaURL + '\t' + pokemonDBURL)
	
if __name__ == '__main__':
	main()
	