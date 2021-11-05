#!/bin/bash

source /opt/empr/config/settings.sh

SCRAPERDIR=$UTILSDIR/scrapers
BACKUPDIR=/opt/empr/docs/backup
DBSCRAPER=$SCRAPERDIR/db/db_scraper.sh
GAMESDIR=~/Games/roms
PLATFORM=pc

## Update Local DB
cd $CMSDIR
tar cvzf $BACKUPDIR/db/db-$(date +%Y.%m%d.%H%M).tar.gz db.sqlite3
rsync -hirt brinstar:$APPDB $APPDB
rsync -hirt --progress brinstar:$CMSDIR/media/ $CMSDIR/media/

for game in $(ls $GAMESDIR/$PLATFORM)
do
	$DBSCRAPER $game
done

skyscraper -p pc -s import
skyscraper -p pc
