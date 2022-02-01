#!/bin/bash

source /opt/empr/config/settings.sh

SCRAPERDIR=$UTILSDIR/scrapers
BACKUPDIR=/opt/empr/docs/backup
GBSCRAPER=$SCRAPERDIR/gb/gb_scraper.sh
SKYSCRAPER=$SCRAPERDIR/ss/skyscraper.sh
TGDBSCRAPER=$SCRAPERDIR/tgdb/tgdb_scraper.sh

FILE="$1"
FILEPATH=$(readlink -f "$FILE")
FILENAME=$(basename $FILEPATH)
SLUG=${FILENAME%.*}
PLATFORMDIR="$(dirname $FILE)"
PLATFORM_SLUG=$(basename $PLATFORMDIR)
ASSETDIR="$CACHEDIR/assets/$SLUG"

echo "
Scraping $FILENAME ..."

$TGDBSCRAPER "$FILE"
$GBSCRAPER "$FILE"

skyscraper -p $PLATFORM_SLUG -s screenscraper $FILEPATH
skyscraper -p $PLATFORM_SLUG $FILEPATH
$SKYSCRAPER "$FILE"

gb_description=$ASSETDIR/gb-$SLUG-description.txt
ss_description=$ASSETDIR/ss-$SLUG-description.txt
tgdb_description=$ASSETDIR/tgdb-$SLUG-description.txt

gb_details=$ASSETDIR/gb-$SLUG-details.txt
ss_details=$ASSETDIR/ss-$SLUG-details.txt
tgdb_details=$ASSETDIR/tgdb-$SLUG-details.txt

echo "
DESCRIPTIONS:

[GB]
$(cat $gb_description)
---

[SS]
$(cat $ss_description)
---

[TGDB]
$(cat $tgdb_description)
---
"

title=$(cat $tgdb_details | grep -m 1 "title:" | cut -d ":" -f 2 | xargs)
sort_title=$(cat $tgdb_details | grep "sort_title:" | cut -d ":" -f 2 | xargs)
path=$FILENAME
platform=$(cat $ss_details | grep "platform:" | cut -d ":" -f 2 | xargs)
platform_slug=$(cat $ss_details | grep "platform_slug:" | cut -d ":" -f 2 | xargs)
genre=$(cat $tgdb_details | grep "genre:" | cut -d ":" -f 2 | xargs)
developer=$(cat $tgdb_details | grep "developer:" | cut -d ":" -f 2 | xargs)
publisher=$(cat $tgdb_details | grep "publisher:" | cut -d ":" -f 2 | xargs)
release_date=$(cat $tgdb_details | grep "release_date:" | cut -d ":" -f 2 | xargs)
players=$(cat $ss_details | grep "players:" | cut -d ":" -f 2 | xargs)
description="$(cat $gb_description)"

echo "
title: $title
sort_title: $sort_title
path: $FILENAME

platform: $platform
platform_slug: $platform_slug

genre: $genre

developer: $developer
publisher: $publisher

release_date: $release_date
players: $players
"

firefox "http://0.0.0.0:8000/admin/games/game/add/?path=$path&title=$title&sort_title=$sort_title&genre=$genre&developer=$developer&publisher=$publisher&release_date=$release_date&path=$path&description=$description" &