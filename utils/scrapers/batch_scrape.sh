#!/bin/bash

source /opt/empr/config/settings.sh

SCRAPERDIR=$UTILSDIR/scrapers
DBSCRAPER=$SCRAPERDIR/db/db_scraper.sh
GAMESDIR=~/Games/roms/pc

for game in $(ls $GAMESDIR)
do
	$DBSCRAPER $game
done

skyscraper -p pc -s import
skyscraper -p pc
