#!/bin/bash

source /opt/empr/config/settings.sh

PLATFORM="$1"
PLATFORMDIR="$ROMSDIR/$PLATFORM"
ESGAMELISTDIR="$APPDIR/plugins/emulationstation/gamelists/$PLATFORM"
GAMES=$(ls -1 $PLATFORMDIR)
MEDIADIR="$APPDIR/cms/media"

echo -e "<?xml version=\"1.0\"?>
<gameList>" >$ESGAMELISTDIR/gamelist.xml

for g in $GAMES
do
  ID_QUERY=$(sqlite3 "$LOCALDB" "select id from games_game where path = '$g'";)
  TITLE_QUERY=$(sqlite3 "$LOCALDB" "select title from games_game where id = '$ID_QUERY'";)
  DESC_QUERY=$(sqlite3 "$LOCALDB" "select description from games_game where id = '$ID_QUERY'";)
  DEV_QUERY=$(sqlite3 "$LOCALDB" "select developer from games_game where id = '$ID_QUERY'";)
  PUB_QUERY=$(sqlite3 "$LOCALDB" "select publisher from games_game where id = '$ID_QUERY'";)
  ESRB_QUERY=$(sqlite3 "$LOCALDB" "select esrb from games_game where id = '$ID_QUERY'";)
  GENREID_QUERY=$(sqlite3 "$LOCALDB" "select genre_id from games_game where id = '$ID_QUERY'";)
  GENRE_QUERY=$(sqlite3 "$LOCALDB" "select name from games_genre where id = '$GENREID_QUERY'";)
  RELEASEDATE_QUERY=$(sqlite3 "$LOCALDB" "select release_date from games_game where id = '$ID_QUERY'";)
  PLAYER_QUERY=$(sqlite3 "$LOCALDB" "select player from games_game where id = '$ID_QUERY'";)

  IFS=$'\n'
  TAGID_QUERY=($(sqlite3 "$LOCALDB" "select tag_id from games_game_tags where game_id = '$ID_QUERY'";))
  TAGARRAY=()
  for TAGID in "${TAGID_QUERY[@]}"
  do
    TAGS=$(sqlite3 "$LOCALDB" "select name from games_tag where id = '$TAGID';")
    TAGARRAY+=($TAGS)
  done

  DISPLAY_QUERY=$(sqlite3 "$LOCALDB" "select display from games_game where id = '$ID_QUERY'";)
  BOXART_QUERY=$(sqlite3 "$LOCALDB" "select boxart from games_game where id = '$ID_QUERY'";)

  # if [[ -z $DISPLAY_QUERY ]]; then
  #   IMAGE="$BOXART_QUERY"
  # else
  #   IMAGE="$DISPLAY_QUERY"
  # fi

  if [[ ! -z $TITLE_QUERY ]]; then
    echo -e "  <game>
    <path>./$g</path>
    <name>$TITLE_QUERY</name>
    <desc>$DESC_QUERY</desc>
    <developer>$DEV_QUERY</developer>
    <publisher>$PUB_QUERY</publisher>
    <esrb>$ESRB_QUERY</esrb>
    <genre>$GENRE_QUERY</genre>
    <releasedate>$RELEASEDATE_QUERY</releasedate>
    <players>$PLAYER_QUERY</players>
    <image>$MEDIADIR/$BOXART_QUERY</image>
  </game>" >>$ESGAMELISTDIR/gamelist.xml
  fi
done

echo -e "</gameList>" >>$ESGAMELISTDIR/gamelist.xml



#<tags>$(printf '%s\n' ${TAGARRAY[@]})</tags>



# PATH_LIST=$HOME/Downloads/path_list.txt

# IFS=$'\n'

# LINES=$(cat $PATH_LIST)

# for i in $LINES
# do
#   sqlite3 $LOCALDB "update games_game set path = '$i.sh' where path = '$i';"
# done

# CMD="$1"
# PATH="$2"
# FILENAME="$(/usr/bin/basename $PATH)"
# path_query(){
#   echo $FILENAME
# }

# $CMD
