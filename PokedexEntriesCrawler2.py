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

def process_table(table):
	entries = {}
	
	for row in table.find_all('tr'):		
		text = row.td.text
		
		for game_node in row.th.find_all('span'):
			entries[game_node.text] = text
	
	return entries

def process_file(contents, pokemon_name):
	soup = BeautifulSoup(contents, 'lxml').html.body
	entries = {}
	
	entries_table = None
	has_multiple_forms = False
	form_name = pokemon_name
	for node in soup.find_all('h2'):
		if node.text == u'Pokédex entries':
			entries_table_node = node.find_next_sibling()
			if entries_table_node.name == 'h3':
				has_multiple_forms = True
				form_name = entries_table_node.text
				entries_table_node = entries_table_node.find_next_sibling()
			entries_table = entries_table_node.table

	if entries_table is None:
		print('Could not find entries table')
		return None
	
	form_entries = process_table(entries_table)
	entries[form_name] = form_entries
	
	if has_multiple_forms:
		while True:
			entries_table_node = entries_table_node.find_next_sibling()
			if entries_table_node.name != 'h3':
				break
			form_name = entries_table_node.text
			entries_table_node = entries_table_node.find_next_sibling()
			entries_table = entries_table_node.table
			
			form_entries = process_table(entries_table)
			entries[form_name] = form_entries
			

	return entries

def main():
	print("Pokedex entries Crawler")
	
	all_entries = {}
	
	filename = "Cached/PokemonDBPokemon/_AllPokemon.html"
	url = "https://pokemondb.net/pokedex/all"
	contents = crawler.fetch_or_download(filename, url)
	soup = BeautifulSoup(contents, 'lxml').html.body
	table = soup.find('table', id='pokedex')
	
	for row in table.tbody.find_all('tr'):
		cells = row.find_all('td')
		number = cells[0].text.strip()
		urlNode = cells[1].a
		name = cells[1].a.text.strip()
		urlPath = urlNode['href']
		
		if name in all_entries:
			# Don't process the same pokemon multiple times
			continue
		
		print('Processing {}'.format(name))
		url = 'https://pokemondb.net' + urlPath
		filename = 'Cached/PokemonDBPokemon/{}-{}.html'.format(number, name, )
		
		contents = crawler.fetch_or_download(filename, url)
		soup = BeautifulSoup(contents, 'lxml').html.body
		entries = process_file(contents, name)
		
		if entries:
			entries[u'number'] = number
			all_entries[name] = entries
				
	crawler.write_data_to_file(all_entries, "Data/PokedexEntries2")
	
	all_games = [u'Red', u'Blue', u'Yellow', u'Gold', u'Silver', u'Crystal', u'Ruby', u'Sapphire', u'Emerald', u'FireRed', u'LeafGreen', u'Diamond', u'Pearl', u'Platinum', u'HeartGold', u'SoulSilver', u'Black', u'White', u'Black 2', u'White 2', u'X', u'Y', u'Omega Ruby', u'Alpha Sapphire', u'Sun', u'Moon', u'Ultra Sun', u'Ultra Moon', u'Let\'s Go Pikachu', u'Let\'s Go Eevee', u'Sword', u'Shield', u'Brilliant Diamond', u'Shining Pearl', u'Legends: Arceus', u'Scarlet', u'Violet']
	all_games = [u'Scarlet', u'Violet']
	all_vertical_entries = []
	for pokemon_name in all_entries:
		pokemon_entry = all_entries[pokemon_name]
		
		for form_name in pokemon_entry:
			entries = pokemon_entry[form_name]
			number = pokemon_entry[u'number']
			
			for game in all_games:
				if game not in entries:
					continue
				
				value = entries[game]
				
				modified = {}
				modified[u'number'] = number
				modified[u'name'] = pokemon_name
				modified[u'formName'] = form_name
				modified[u'game'] = game
				modified[u'entry'] = value
				all_vertical_entries.append(modified)
	all_vertical_fieldnames = [u'number', u'name', u'formName', u'game', u'entry']
	crawler.write_entries_to_tsv(all_vertical_entries, all_vertical_fieldnames, "Data/PokedexEntries2-Vertical")
	
#	print(all_entries)
	print("Done!")
	
if __name__ == '__main__':
	main()
	