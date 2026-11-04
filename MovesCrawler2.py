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

def targetIsSelected(target):
	if 'mt-selected' in target['class']:
		return '1'
	else:
		return '0'

def process_move(contents):
	entry = {}
	soup = BeautifulSoup(contents, 'lxml').html.body
	
	# Metadata
	for h2 in soup.find_all('h2'):
		if h2.text.strip() == "Move data":
			table = h2.find_next_sibling()
			if table is None:
				print("wtf no metadata")
				break
			
			for tr in table.find_all('tr'):
				key = tr.th.text.strip()
				value = tr.td.text.strip()
				if key == 'Type':
					entry['type'] = value
				elif key == 'Category':
					entry['category'] = value
				elif key == 'Power':
					entry['power'] = value
				elif key == 'Accuracy':
					accuracy = value
					# dash means no accuracy value
					if accuracy != u'—':
						entry['accuracy'] = accuracy
				elif key == 'PP':
					values = re.findall(r'\d+', value)
					if len(values) == 0:
						print("wtf")
					elif len(values) == 1:
						entry['pp'] = values[0]
					elif len(values) == 2:
						entry['pp'] = values[0]
						entry['maxPP'] = values[1]
				elif key == 'Priority':
					entry['priority'] = value
				elif key == 'Introduced':
					entry['generationIntroduced'] = value
			
			break
	
	# Move Target
	for h2 in soup.find_all('h2'):
		if h2.text.strip() == "Move target":
			overall_div = h2.find_next_sibling()
			if overall_div.div is None:
				print("wtf no target?")
				break
			targets = overall_div.div.find_all('div')
			
			if len(targets) < 6:
				print('wtf not 6 targets?')
				break
			
			entry['targetFoe1'] = targetIsSelected(targets[0])			
			entry['targetFoe2'] = targetIsSelected(targets[1])			
			entry['targetFoe3'] = targetIsSelected(targets[2])			
			entry['targetSelf'] = targetIsSelected(targets[3])			
			entry['targetAlly1'] = targetIsSelected(targets[4])			
			entry['targetAlly2'] = targetIsSelected(targets[5])
			
			entry['targetDescription'] = overall_div.find_next_sibling('p').text.strip()
			
			break
	
	# Descriptions
	header = soup.find('h2', id='move-descr')
	if not header:
		return entry
	table_parent = header.find_next_sibling()
	if not table_parent:
		return entry
	table = table_parent.table
	rows = table.find_all('tr')
	for row in rows:
		game_nodes = row.th.find_all('span')
		description = row.td.text.strip()
		for game_node in game_nodes:
			game_name = game_node.text.strip()
			entry[game_name] = description
			
	return entry

def main():
	print("Starting...")
	file_path = 'Cached/PokemonDBMoves/'
	
	all_entries = {}
	
	filename = "Cached/PokemonDBMoves/_AllMoves.html"
	url = "https://pokemondb.net/move/all"
	contents = crawler.fetch_or_download(filename, url)
	soup = BeautifulSoup(contents, 'lxml').html.body
	table = soup.find('table', id='moves')
	
	for row in table.tbody.find_all('tr'):
		cells = row.find_all('td')
		name = cells[0].text.strip()
		urlPath = cells[0].a['href'].strip()
				
		print('Processing {}'.format(name))
		url = 'https://pokemondb.net' + urlPath
		filename = 'Cached/PokemonDBMoves/{}.html'.format(name)
		
		contents = crawler.fetch_or_download(filename, url)
		entries = process_move(contents)
		
		entries[u'name'] = name
		
		dict_name = re.sub(r'[^a-zA-Z0-9]', '', name).lower()
		all_entries[dict_name] = entries
		
#		break # debug
		
	crawler.write_data_to_file(all_entries, "Data/MoveDescriptions2")
	
	print(all_entries)
	print("Done!")
	
if __name__ == '__main__':
	main()
	