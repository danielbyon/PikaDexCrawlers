#!/usr/bin/env python3 -tt

MOVE_TAB_HEADER_IDS = {
	1: ['tab-moves-1', 'tab-moves-2'],
	2: ['tab-moves-3', 'tab-moves-4'],
	3: ['tab-moves-5', 'tab-moves-6', 'tab-moves-7'],
	4: ['tab-moves-8', 'tab-moves-9', 'tab-moves-10'],
	5: ['tab-moves-11', 'tab-moves-12'],
	6: ['tab-moves-13', 'tab-moves-14'],
	7: ['tab-moves-15', 'tab-moves-16', 'tab-moves-17'],
	8: ['tab-moves-18', 'tab-moves-19', 'tab-moves-20'],
	9: ['tab-moves-21']
}

MOVE_GAMES_FOR_TAB = {
	'tab-moves-1': ['red', 'blue'],
	'tab-moves-2': ['yellow'],
	'tab-moves-3': ['gold', 'silver'],
	'tab-moves-4': ['crystal'],
	'tab-moves-5': ['ruby', 'sapphire'],
	'tab-moves-6': ['fireRed', 'leafGreen'],
	'tab-moves-7': ['emerald'],
	'tab-moves-8': ['diamond', 'pearl'],
	'tab-moves-9': ['platinum'],
	'tab-moves-10': ['heartGold', 'soulSilver'],
	'tab-moves-11': ['black', 'white'],
	'tab-moves-12': ['black2', 'white2'],
	'tab-moves-13': ['x', 'y'],
	'tab-moves-14': ['omegaRuby', 'alphaSapphire'],
	'tab-moves-15': ['sun', 'moon'],
	'tab-moves-16': ['ultraSun', 'ultraMoon'],
	'tab-moves-17': ['letsGoPikachu', 'letsGoEevee'],
	'tab-moves-18': ['sword', 'shield'],
	'tab-moves-19': ['brilliantDiamond', 'shiningPearl'],
	'tab-moves-20': ['legendsArceus'],
	'tab-moves-21': ['scarlet', 'violet']
}

def generations_from_number(number):
	gens = [9]
	if number < 906:
		gens.append(8)
	if number < 810:
		gens.append(7)
	if number < 722:
		gens.append(6)
	if number < 650:
		gens.append(5)
	if number < 494:
		gens.append(4)
	if number < 387:
		gens.append(3)
	if number < 252:
		gens.append(2)
	if number < 152:
		gens.append(1)
	return gens
	
def parse_game_titles(node):
	games = []
	for game_node in node.find_all('a'):
		try:
			title = game_node['title']
		except KeyError:
			continue
		if title == u'Pokémon Red and Blue Versions':
			games.append('red')
			games.append('blue')
		elif title == u'Pokémon Yellow Version':
			games.append('yellow')
		elif title == u'Pokémon Gold and Silver Versions':
			games.append('gold')
			games.append('silver')
		elif title == u'Pokémon Crystal Version':
			games.append('crystal')
		elif title == u'Pokémon Ruby and Sapphire Versions':
			games.append('ruby')
			games.append('sapphire')
		elif title == u'Pokémon Emerald Version':
			games.append('emerald')
		elif title == u'Pokémon FireRed and LeafGreen Versions':
			games.append('fireRed')
			games.append('leafGreen')
		elif title == u'Pokémon Diamond and Pearl Versions':
			games.append('diamond')
			games.append('pearl')
		elif title == u'Pokémon Platinum Version':
			games.append('platinum')
		elif title == u'Pokémon HeartGold and SoulSilver Versions':
			games.append('heartGold')
			games.append('soulSilver')
		elif title == u'Pokémon Black and White Versions':
			games.append('black')
			games.append('white')
		elif title == u'Pokémon Black and White Versions 2':
			games.append('black2')
			games.append('white2')
		elif title == u'Pokémon X and Y':
			games.append('x')
			games.append('y')
		elif title == u'Pokémon Omega Ruby and Alpha Sapphire':
			games.append('omegaRuby')
			games.append('alphaSapphire')
		elif title == u'Pokémon Sun and Moon':
			games.append('sun')
			games.append('moon')
		elif title == u'Pokémon Ultra Sun and Ultra Moon':
			games.append('ultraSun')
			games.append('ultraMoon')
		elif title == u'Pokémon: Let\'s Go, Pikachu! and Let\'s Go, Eevee!':
			games.append('letsGoPikachu')
			games.append('letsGoEevee')
		elif title == u'Pokémon Sword and Shield':
			games.append('sword')
			games.append('shield')
		elif title == u'Pokémon Brilliant Diamond and Shining Pearl':
			games.append('brilliantDiamond')
			games.append('shiningPearl')
		elif title == u'Pokémon Legends: Arceus':
			games.append('legendsArceus')
		elif title == u'Pokémon Scarlet and Violet':
			games.append('scarlet')
			games.append('violet')
	return games

def parse_game_specific_values(node, all_dict, game_specific_value):
	for game in parse_game_titles(node):
		all_dict[game] = game_specific_value
