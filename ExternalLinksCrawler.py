#!/usr/bin/env python3 -tt
# -*- coding: utf-8 -*-

import codecs
import CrawlerUtils as crawler

def main():
    print("This is the Pokepedia Pokemon Crawler")

    all_entries = {}
    
    with codecs.open("PokemonList.txt", 'r', encoding='utf8') as f:
        for line in f:
            pokemon = line.strip().replace(' ', '_').rstrip('.')

            entries = {}
            url = "https://bulbapedia.bulbagarden.net/wiki/" + pokemon + "_(Pokémon)"
            print(url)
            entries["Bulbapedia"] = "https://bulbapedia.bulbagarden.net/wiki/" + pokemon + "_(Pokemon)"
            all_entries[line.strip()] = entries

    crawler.write_data_to_file(all_entries, "Data/ExternalLinks")

if __name__ == '__main__':
    main()
