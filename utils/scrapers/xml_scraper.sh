#! /bin/bash

source $HOME/Applications/Empr/config/empr/settings.sh
SLUG="$1"
SCRAPERSDIR="$UTILSDIR/scrapers"
CACHEDIR="$UTILSDIR/scrapers/.cache"
XMLDIR="$CACHEDIR/xml"
XMLTMP="$XMLDIR/game.tmp.xml"

game_list=$(xmllint --format -xpath "//gameList/game/*/text()" "$XMLDIR/$SLUG.gamelist.xml")

echo "$game_list"

#game_array=($game_list)

#echo -e "${game_array[@]}"