#!/usr/bin/env python3 -tt
# -*- coding: utf-8 -*-

import CrawlerUtils as crawler

URLS = [
    'https://archives.bulbagarden.net/wiki/Category:Pok%C3%A9mon_Dream_World_items',
    'https://archives.bulbagarden.net/w/index.php?title=Category:Pok%C3%A9mon_Dream_World_items&filefrom=Dream+Ice+Stone+Sprite.png#mw-category-media',
    'https://archives.bulbagarden.net/w/index.php?title=Category:Pok%C3%A9mon_Dream_World_items&filefrom=Dream+Rowap+Berry+Sprite.png#mw-category-media'
]

FILE_PATH = 'Cached/Items/DreamWorld/'
IMAGE_PATH = 'Artwork/RawItems/DreamWorld/'

def main():
    print('This is the Pokepedia Item Image Crawler')
    
    count = 0
    for page_url in URLS:
        crawler.download_images_from_bulbapedia(page_url, count, FILE_PATH, IMAGE_PATH)
        count += 1
    
    print("Done!")

if __name__ == '__main__':
    main()
