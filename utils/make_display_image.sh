#! /bin/bash

UTILS="$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
source $UTILS/utils.sh

MEDIADIR=$CMS/media
SCRAPERDIR=$UTILS/scrapers
SKYSCRAPERDIR=$HOME/.empr/skyscraper/import
PATH="$1"
FILENAME=${PATH##*/}
SLUG=${FILENAME%.*}

id_query(){
	$SQLITE $APPDB "select id from games_game where path = '$PATH';"
}

ID=$(id_query)

if [[ -z $ID ]];then
  echo "$FILENAME not found in database."
  exit
fi

platform_id=$(/usr/bin/sqlite3 $APPDB "select platform_id from games_game where id = '$ID';")
platform_name=$(/usr/bin/sqlite3 $APPDB "select name from games_platform where id = '$platform_id';")
platform_slug=$(/usr/bin/sqlite3 $APPDB "select slug from games_platform where id = '$platform_id';")

if [[ $platform_slug = steam ]]; then
	platform_slug="pc"
fi

boxart=$(/usr/bin/sqlite3 $APPDB  "select boxart from games_game where id = '$ID'")
screenshot=$(/usr/bin/sqlite3 $APPDB "select screenshot from games_game where id = '$ID'")
title_image=$(/usr/bin/sqlite3 $APPDB "select title_image from games_game where id = '$ID'")
wallpaper=$(/usr/bin/sqlite3 $APPDB "select wallpaper from games_game where id = '$ID'")

DISPLAYIMAGES=$APPFILES/skyscraper/media/$platform_slug/screenshots

echo "
#########
## DEV ##
#########

ID: $ID
PATH: $PATH
FILENAME: $(/usr/bin/basename $PATH)
boxart: $boxart
platform_name: $platform_name
platform_slug: $platform_slug
screenshot: $screenshot
title_image: $title_image
wallpaper: $wallpaper

DISPLAYIMAGES $DISPLAYIMAGES
"

## Get Images

/usr/bin/cp -v $MEDIADIR/$boxart $SKYSCRAPERDIR/$platform_slug/covers/$SLUG.jpg
/usr/bin/cp -v $MEDIADIR/$screenshot $SKYSCRAPERDIR/$platform_slug/screenshots/$SLUG.jpg
/usr/bin/cp -v $MEDIADIR/$title_image $SKYSCRAPERDIR/$platform_slug/wheels/$SLUG.png

if [[ -f $HOME/Games/roms/$platform_slug/$FILENAME ]]; then
	/usr/bin/echo -e "file found"
else
	/usr/bin/echo -e "file not found"
	/usr/bin/mkdir -p $HOME/Games/roms/$platform_slug
	/usr/bin/touch $HOME/Games/roms/$platform_slug/$FILENAME
fi

if [[ $platform_slug = "ps1" ]]; then
	platform_slug="psx"
elif [[ $platform_slug = "atari-2600" ]]; then
	platform_slug="atari2600"
elif [[ $platform_slug = "gamecube" ]]; then
	platform_slug="gc"
fi

/usr/local/bin/skyscraper -p $platform_slug -s import $FILENAME
/usr/local/bin/skyscraper -p $platform_slug $FILENAME

/usr/bin/cp -v $DISPLAYIMAGES/$SLUG.png $APPFILES/media/games/display/

/usr/bin/sqlite3 $APPDB "update games_game set display = 'games/display/$SLUG.png' where id = $ID;"


