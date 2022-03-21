#!/bin/bash

source /opt/empr/config/settings.sh

MEDIADIR=$CMSDIR/media
SCRAPERDIR=$UTILSDIR/scrapers
SKYSCRAPERDIR=$HOME/.empr/import
PATH="$1"
FILENAME=${PATH##*/}
SLUG=${FILENAME%.*}

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

if [[ $platform_slug = steam ]]; then
	platform_slug="pc"
fi

boxart=$($SQLITE "$APPDB" "select boxart from games_game where id = '$ID'")
screenshot=$($SQLITE "$APPDB" "select screenshot from games_game where id = '$ID'")
title_image=$($SQLITE "$APPDB" "select title_image from games_game where id = '$ID'")
wallpaper=$($SQLITE "$APPDB" "select wallpaper from games_game where id = '$ID'")

echo "
ID: $ID
PATH: $PATH
FILENAME: $(/usr/bin/basename $PATH)
platform_name: $platform_name
platform_slug: $platform_slug
"

DISPLAYIMAGES=$APPFILES/media/$platform_slug/screenshots

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

if [[ $platform_slug = "ps1" ]]; then
	platform_slug="psx"
elif [[ $platform_slug = "atari-2600" ]]; then
	platform_slug="atari2600"
fi

/usr/local/bin/skyscraper -p $platform_slug -s import $FILENAME
/usr/local/bin/skyscraper -p $platform_slug $FILENAME

"$SQLITE" "$APPDB" "update games_game set display = 'games/display/$SLUG.png' where id = $ID"

/usr/bin/cp $DISPLAYIMAGES/$SLUG.png $CMSDIR/media/games/display/
