#!/usr/bin/env python3 -tt
# -*- coding: utf-8 -*-

import CrawlerUtils as crawler

URLS = [
    'https://archives.bulbagarden.net/wiki/Category:Bag_sprites',
    'https://archives.bulbagarden.net/w/index.php?title=Category:Bag_sprites&filefrom=Bag+Dowsing+MCHN+IV+Sprite.png#mw-category-media',
    'https://archives.bulbagarden.net/w/index.php?title=Category:Bag_sprites&filefrom=Bag+Insect+Plate+Sprite.png#mw-category-media',
    'https://archives.bulbagarden.net/w/index.php?title=Category:Bag_sprites&filefrom=Bag+Pewter+Crunchies+Sprite.png#mw-category-media',
    'https://archives.bulbagarden.net/w/index.php?title=Category:Bag_sprites&filefrom=Bag+Sky+Plate+Sprite.png#mw-category-media',
    'https://archives.bulbagarden.net/w/index.php?title=Category:Bag_sprites&filefrom=Bag+X+Defend+3+Sprite.png#mw-category-media'
]

FILE_PATH = 'Cached/Items/BagSprites/'
IMAGE_PATH = 'Artwork/RawItems/BagSprites/'

def main():
    print('This is the Pokepedia Item Image Crawler')
    
    count = 0
    for page_url in URLS:
        crawler.download_images_from_bulbapedia(page_url, count, FILE_PATH, IMAGE_PATH)
        count += 1
    
    print("Done!")

if __name__ == '__main__':
    main()
