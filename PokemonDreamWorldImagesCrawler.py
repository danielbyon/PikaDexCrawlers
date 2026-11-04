#!/usr/bin/env python3 -tt
# -*- coding: utf-8 -*-

import CrawlerUtils as crawler

URLS = [
    'https://archives.bulbagarden.net/wiki/Category:Pok%C3%A9mon_Dream_World_artwork',
    'https://archives.bulbagarden.net/w/index.php?title=Category:Pok%C3%A9mon_Dream_World_artwork&filefrom=*124%0A124Jynx+Dream.png',
    'https://archives.bulbagarden.net/w/index.php?title=Category:Pok%C3%A9mon_Dream_World_artwork&filefrom=*245%0A245Suicune+Dream+2.png',
    'https://archives.bulbagarden.net/w/index.php?title=Category:Pok%C3%A9mon_Dream_World_artwork&filefrom=*398%0A398Staraptor+Dream.png',
    'https://archives.bulbagarden.net/w/index.php?title=Category:Pok%C3%A9mon_Dream_World_artwork&filefrom=*545%0A545Scolipede+Dream.png',
    'https://archives.bulbagarden.net/w/index.php?title=Category:Pok%C3%A9mon_Dream_World_artwork&filefrom=*676%0A676Furfrou+Debutante+Dream.png',
    'https://archives.bulbagarden.net/w/index.php?title=Category:Pok%C3%A9mon_Dream_World_artwork&filefrom=*804%0A804Naganadel+Dream.png'
]

FILE_PATH = 'Cached/PokemonSprites/DreamWorld/'
IMAGE_PATH = 'Artwork/RawPokemon/DreamWorld/'

def main():
    print('This is the Pokepedia Pokemon Sprite Crawler')
    
    count = 0
    for page_url in URLS:
        crawler.download_images_from_bulbapedia(page_url, count, FILE_PATH, IMAGE_PATH)
        count += 1
    
    print("Done!")

if __name__ == '__main__':
    main()
