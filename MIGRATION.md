# Crawler extraction record

## Imported source

PikaDex moved its noncached crawler source inventory to this repository in
commit `0e5672b16e66c78140a699ef32812cdc2f0d4a15`. The source-side extraction
commit is `41f884288ab2a613971446af2b3bfe5b13fa7601`, whose parent is the
SQLite-only commit `be6924d7d3961c7893cd5df1a93d8efb1082a9cf`.

The inventory contains 17,200 files and 2,614,633,092 bytes. Its SHA-256 is
`40e5c1a6761dad2ccd8ed4a550760139192d672819cc2e89de734126f3cdae35`. It
contains 9,424 distinct file hashes, representing 1,220,898,202 bytes of
distinct content. A final comparison against this inventory found no missing
files, content mismatches, or file-mode mismatches. The source inventory covers
the imported files; `README.md` is authored documentation outside that set.

## Accepted inherited whitespace

The migration preserved the imported files byte-for-byte. As a result,
`git show --check 0e5672b16e66c78140a699ef32812cdc2f0d4a15` exits with status 2
and reports 32,415 inherited trailing-whitespace findings in these 40 files:

| Imported path | Findings |
| --- | ---: |
| `AbilitiesCrawler2.py` | 19 |
| `AbilityExternalLinksCrawler.py` | 7 |
| `CrawlerUtils.py` | 18 |
| `Data/PokedexEntries-Vertical.tsv` | 14,080 |
| `Data/PokedexEntries.tsv` | 899 |
| `Data/PokedexEntries2-Vertical.tsv` | 959 |
| `Data/PokemonInfo.tsv` | 1,009 |
| `Data/PokemonTypes.tsv` | 1,026 |
| `ExternalLinksCrawler.py` | 1 |
| `ItemSpriteCrawler.py` | 8 |
| `ItemsBagSpritesCrawler.py` | 2 |
| `ItemsCrawlerBulbapedia.py` | 41 |
| `ItemsCrawlerPokemonDB.py` | 17 |
| `ItemsDreamWorldImagesCrawler.py` | 2 |
| `LearnsetBreedingCrawler.py` | 13 |
| `LearnsetBreedingCrawler2.py` | 34 |
| `LearnsetLevelCrawler3.py` | 20 |
| `LearnsetMachinesCrawler3.py` | 22 |
| `LearnsetTutoringCrawler3.py` | 23 |
| `MoveDescriptionCrawler.py` | 10 |
| `MoveExternalLinksCrawler.py` | 7 |
| `MovesCrawler.py` | 20 |
| `MovesCrawler2.py` | 27 |
| `Playground.py` | 6 |
| `PokedexEntries.backup.json` | 11,225 |
| `PokedexEntries.json` | 152 |
| `PokedexEntriesCrawler.py` | 16 |
| `PokedexEntriesCrawler2.py` | 25 |
| `PokemonAbilities.json` | 2,630 |
| `PokemonAbilitiesCrawler.py` | 4 |
| `PokemonDB.py` | 1 |
| `PokemonDreamWorldImagesCrawler.py` | 2 |
| `PokemonImageCrawler.py` | 3 |
| `PokemonInfoCrawler.py` | 11 |
| `PokemonKenSugimoriImagesCrawler.py` | 2 |
| `PokemonLocationCrawler.py` | 27 |
| `PokemonSpritesCrawler.py` | 5 |
| `PokemonSpritesCrawler2.py` | 7 |
| `PokemonTypeCrawler.py` | 13 |
| `PokemonWildDenCrawler.py` | 22 |

These findings are accepted as part of the byte-preserving import. No imported
file was normalized, and no global whitespace setting or broad suppression was
added. The exception applies only to the 40 listed paths. Newly authored source,
configuration, and documentation remain subject to normal whitespace checks.

## Release verification

PikaDex ran `Scripts/pokedex-release-verification` in a disposable checkout
with this repository pinned at the migration commit above. The run used Xcode
27.2 (build 27B52) and an iPhone 17 simulator running iOS 27.0. All release
gates passed. The detailed gate counts, source validation findings, database
hash comparison, and primary-checkout preservation results are recorded in
PikaDex's `docs/crawler-extraction-evidence.md`.
