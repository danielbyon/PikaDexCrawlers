#!/usr/bin/env python3 -tt
# -*- coding: utf-8 -*-

import CrawlerUtils as crawler

URLS = [
    'https://archives.bulbagarden.net/wiki/Category:Ken_Sugimori_Pok%C3%A9mon_artwork',
    'https://archives.bulbagarden.net/w/index.php?title=Category:Ken_Sugimori_Pok%C3%A9mon_artwork&filefrom=%2A053%0A053Persian.png#mw-category-media',
    'https://archives.bulbagarden.net/w/index.php?title=Category:Ken_Sugimori_Pok%C3%A9mon_artwork&filefrom=%2A113%0A113Chansey.png#mw-category-media',
    'https://archives.bulbagarden.net/w/index.php?title=Category:Ken_Sugimori_Pok%C3%A9mon_artwork&filefrom=%2A185%0A185Sudowoodo+GS.png#mw-category-media',
    'https://archives.bulbagarden.net/w/index.php?title=Category:Ken_Sugimori_Pok%C3%A9mon_artwork&filefrom=%2A289%0A289Slaking.png#mw-category-media',
    'https://archives.bulbagarden.net/w/index.php?title=Category:Ken_Sugimori_Pok%C3%A9mon_artwork&filefrom=%2A443%0A443Gible.png#mw-category-media',
    'https://archives.bulbagarden.net/w/index.php?title=Category:Ken_Sugimori_Pok%C3%A9mon_artwork&filefrom=%2A602%0A602Tynamo.png#mw-category-media',
    'https://archives.bulbagarden.net/w/index.php?title=Category:Ken_Sugimori_Pok%C3%A9mon_artwork&filefrom=%2A744%0A744Rockruff.png#mw-category-media',
    'https://archives.bulbagarden.net/w/index.php?title=Category:Ken_Sugimori_Pok%C3%A9mon_artwork&filefrom=%2A%3F%3F%3F%0ACalyrex+2.png#mw-category-media'
]

FILE_PATH = 'Cached/PokemonSprites/KenSugimori/'
IMAGE_PATH = 'Artwork/RawPokemon/KenSugimori/'

def main():
    print('This is the Pokepedia Pokemon Sprite Crawler')
    
    count = 0
    for page_url in URLS:
    crawler.download_images_from_bulbapedia(page_url, count, FILE_PATH, IMAGE_PATH)
        count += 1
    
    print("Done!")

if __name__ == '__main__':
    main()
