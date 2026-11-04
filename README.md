# PikaDexCrawlers

This repository holds the crawler scripts, artwork, and reviewed source data
used by PikaDex. PikaDex pins an exact commit in
`Scripts/DataPipeline/crawler-source.json` and keeps its existing logical
`Crawlers/...` manifest paths. The database pipeline reads crawler inputs from
this repository and keeps them in their original reviewed order when it
prepares loader inputs.

The root `Cached/` directory is local website cache material. Keep it out of
Git. It is ignored by the repository rules and excluded from current and
historical security scans.

To update PikaDex's source revision, review the crawler change, update the
source reference in PikaDex, check every manifest-declared input checksum, and
run the documented generation and native verification workflow. A changed
input is not approved by changing the pin alone.
