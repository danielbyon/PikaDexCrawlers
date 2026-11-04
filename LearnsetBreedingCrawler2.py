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

def process_file(contents, generation, pokemon_name):
	soup = BeautifulSoup(contents, 'lxml').html.body
	entries = {}
	
	h2 = soup.h2
	
	if not h2 or 'egg move parents' not in h2.text:
		print('could not find h2, or incorrect node found for {}'.format(pokemon_name))
		return entries
	
	for table_candidate in h2.find_next_siblings('div'):
		if 'tabset-eggmoves' in table_candidate['class']:
			table = table_candidate
			break
	if not table:
		print('could not find table for {}'.format(pokemon_name))
		return None
	
	
	div = h2.find_next_sibling('div')
	if 'tabset-eggmoves' in div['class'] or 'tabs-wrapper' in div['class'] or 'sv-tabs-wrapper' in div['class']:
		form_names = []
		tab_list = div.div
		for tab in tab_list.find_all('a'):
			form_names.append(tab.text.strip())
		table_div = tab_list.find_next_sibling().div
	else:
		form_names = [pokemon_name]
		table_div = div
		
	for form_name in form_names:
		moves = []
		
		for h3 in table_div.find_all('h3'):
			move = h3.text.strip()
			if move == 'Egg moves':
				# Skip top-level egg moves list
				continue
			
			move_table = h3.find_next_sibling()
			if not move_table:
				print('could not find move table for form {}'.format(form_name))
				continue
			move_table = move_table.table.tbody
			move_table_trs = move_table.find_all('tr')
			
			for tr in move_table_trs:
				if 'Level up' not in tr.td.text:
					continue
				
				parents = []
				for parent_a in tr.find_all('a'):
					parents.append(parent_a.text.strip())
				
				moves.append({
					'name': move,
					'parents': parents
				})
		
		key = 'gen{}.{}'.format(generation, form_name)
		entries[key] = moves
			
		table_div = table_div.find_next_sibling()
		if table_div is None:
			break
	
	
#	tab_ids = pdb.MOVE_TAB_HEADER_IDS[generation]
#	for tab_id in tab_ids:
#		tab = soup.find('div', id=tab_id)
#		if tab is None:
#			return None
#		headers = tab.find_all('h3')
#		for header in headers:
#			if header.text.strip() != 'Moves learnt by level up':
#				continue
#			div = header.find_next_sibling().find_next_sibling()
#			if div is None or div.name != 'div':
#				continue
#			
#			if 'tabset-eggmoves' in div['class'] or 'tabs-wrapper' in div['class'] or 'sv-tabs-wrapper' in div['class']:
#				form_names = []
#				tab_list = div.div
#				for tab in tab_list.find_all('a'):
#					form_names.append(tab.text.strip())
#				table_div = tab_list.find_next_sibling().div
#			else:
#				form_names = [pokemon_name]
#				table_div = div
#				
#			for form_name in form_names:
#				table = table_div.table
#				
#				if table is None or table.tbody is None:
#					break
#				
#				rows = table.tbody.find_all('tr')
#				moves = []
#				for row in rows:
#					tds = row.find_all('td')
#					level = tds[0].text.strip()
#					name = tds[1].text.strip()
#					move = {
#						'level': level,
#						'name': name
#					}
#					moves.append(move)
#			
#				games = pdb.MOVE_GAMES_FOR_TAB[tab_id]
#				for game in games:
#					key = '{}.{}'.format(game, form_name)
#					entries[key] = moves
#				
#				table_div = table_div.find_next_sibling()
#				if table_div is None:
#					break
	
	return entries

def main():
	print("This is the Pokepedia Moves Crawler")

	all_entries = {}
	
	filename = "Cached/PokemonDBPokemon/_AllPokemon.html"
	url = "https://pokemondb.net/pokedex/all"
	contents = crawler.fetch_or_download(filename, url)
	soup = BeautifulSoup(contents, 'lxml').html.body
	table = soup.find('table', id='pokedex')
	
	pokemons = []
	
	for row in table.tbody.find_all('tr'):
		cells = row.find_all('td')
		number = cells[0].text.strip()
		moveNode = cells[1].a
		name = cells[1].a.text.strip()
		urlPath = moveNode['href']
		
		pokemons.append({
			'name': name,
			'number': number,
			'urlPath': urlPath
		})
		
	for pokemon in pokemons:
		name = pokemon['name']
		number = pokemon['number']
		urlPath = pokemon['urlPath']
		
		if name in all_entries:
			# Don't process the same pokemon multiple times
			continue
			
		print('Processing {}'.format(name))
			
		pokemon_entries = {}
		
		generations = pdb.generations_from_number(int(number))
		for gen in generations:
			url = 'https://pokemondb.net' + urlPath + '/moves/{}'.format(gen)
			filename = 'Cached/PokemonDBPokemon/{}-{}-moves-{}.html'.format(number, name, gen)
			print('Processing {}'.format('{} - gen {}'.format(name, gen)))
			
			contents = crawler.fetch_or_download(filename, url)
			soup = BeautifulSoup(contents, 'lxml').html.body
			entries = process_file(contents, gen, name)
			if entries is not None:
				pokemon_entries['gen{}'.format(gen)] = entries
		
		all_entries[name] = pokemon_entries

	crawler.write_data_to_file(all_entries, "Data/LearnsetBreeding2")
#	print(all_entries)
	print("Done!")

if __name__ == '__main__':
	main()
	