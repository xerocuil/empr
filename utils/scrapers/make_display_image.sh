#!/bin/bash

source /opt/empr/config/settings.sh

MEDIADIR=$CMSDIR/media
SCRAPERDIR=$UTILSDIR/scrapers
SKYSCRAPERDIR=$HOME/.empr/screenscraper/import
PATH="$1"
FILENAME=${PATH##*/}
SLUG=${FILENAME%.*}
REMOTEDB=""
IMPORTDATAFILE=$APPDIR/docs/csv/import_display.csv

id_query(){
	$SQLITE "$APPDB" "select id from games_game where path = '$FILENAME'"
}

ID=$(id_query)

if [[ -z $ID ]];then
  echo "$FILENAME not found in database."
  exit
fi

platform_id=$($SQLITE "$APPDB" "select platform_id from games_game where id = '$ID'")
platform_name=$($SQLITE "$APPDB" "select name from games_platform where id = '$platform_id'")
platform_slug=$($SQLITE "$APPDB" "select slug from games_platform where id = '$platform_id'")


boxart=$($SQLITE "$APPDB" "select boxart from games_game where id = '$ID'")
screenshot=$($SQLITE "$APPDB" "select screenshot from games_game where id = '$ID'")
title_image=$($SQLITE "$APPDB" "select title_image from games_game where id = '$ID'")
wallpaper=$($SQLITE "$APPDB" "select wallpaper from games_game where id = '$ID'")

echo "
ID: $ID
PATH: $PATH
FILENAME: $(basename $PATH)
platform_name: $platform_name
platform_slug: $platform_slug
"

DISPLAYIMAGES=$CACHEDIR/skyscraper/$platform_slug/screenshots

## Get Images

if [[ -f $MEDIADIR/$boxart ]]; then
	/usr/bin/cp -v $MEDIADIR/$boxart $SKYSCRAPERDIR/$platform_slug/covers/$SLUG.jpg
fi

if [[ -f $MEDIADIR/$screenshot ]]; then
	/usr/bin/cp -v $MEDIADIR/$screenshot $SKYSCRAPERDIR/$platform_slug/screenshots/$SLUG.jpg
else
	/usr/bin/cp -v $MEDIADIR/$wallpaper $SKYSCRAPERDIR/$platform_slug/screenshots/$SLUG.jpg
fi

if [[ -f $MEDIADIR/$title_image ]]; then
	/usr/bin/cp -v $MEDIADIR/$title_image $SKYSCRAPERDIR/$platform_slug/wheels/$SLUG.png
fi

/usr/local/bin/skyscraper -p $platform_slug -i import $PATH
/usr/local/bin/skyscraper -p $platform_slug $PATH

#"$SQLITE" "$APPDB" "update games_game set display = 'games/display/$SLUG.png' where id = $ID"

echo "id,path,display
$ID,$FILENAME,games/display/$SLUG.png
" >$IMPORTDATAFILE

/usr/bin/scp $IMPORTDATAFILE brinstar:$IMPORTDATAFILE
/usr/bin/scp $DISPLAYIMAGES/$SLUG.png brinstar:$CMSDIR/media/games/display/

. $VENV/bin/activate
cd $CMSDIR

ssh brinstar "/opt/empr/utils/import_game_display.sh"

#/usr/bin/mv $IMPORTDATAFILE $IMPORTDATAFILE.bak