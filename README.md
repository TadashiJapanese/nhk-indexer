# nhk-indexer

A small tool to generate a static site that lists what percentage of NHK News Easy article Kanji can be read by a person at
any given level of WaniKani.

## Using the Extractor

Before you begin you will need a sqlite3 export of the WaniKani corpus. It is not included in this repo.

Using this tool is a two step process:

1. run ```nhk_analayse.py``` which will use the NHK News Easy API to grab recent NHK Articles and their content and dumps it into a local sqlite3 database
2. run ```nhk_buildsite.py``` which regenerates a static website from the sqlite3 database
