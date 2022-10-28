#! /bin/bash

DIR="$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
SCRAPERS="$(dirname $DIR)"
UTILS="$(dirname $SCRAPERS)"
source $UTILS/utils.sh

PLATFORM="$1"
PLATFORMDIR="$ROMSDIR/$PLATFORM"
ESGAMELISTDIR="$HOME/.emulationstation/gamelists/$PLATFORM"
GAMES=$(ls -1 $PLATFORMDIR)
MEDIADIR="$APPFILES/media"

echo -e "<?xml version=\"1.0\"?>
<gameList>" >$ESGAMELISTDIR/gamelist.xml

for g in $GAMES
do
  ID_QUERY=$(sqlite3 "$APPDB" "select id from games_game where path = '$g'";)
  TITLE_QUERY=$(sqlite3 "$APPDB" "select title from games_game where id = '$ID_QUERY'";)
  DESC_QUERY=$(sqlite3 "$APPDB" "select description from games_game where id = '$ID_QUERY'";)
  DEV_QUERY=$(sqlite3 "$APPDB" "select developer from games_game where id = '$ID_QUERY'";)
  PUB_QUERY=$(sqlite3 "$APPDB" "select publisher from games_game where id = '$ID_QUERY'";)
  ESRB_QUERY=$(sqlite3 "$APPDB" "select esrb from games_game where id = '$ID_QUERY'";)
  GENREID_QUERY=$(sqlite3 "$APPDB" "select genre_id from games_game where id = '$ID_QUERY'";)
  GENRE_QUERY=$(sqlite3 "$APPDB" "select name from games_genre where id = '$GENREID_QUERY'";)
  RELEASEDATE_QUERY=$(sqlite3 "$APPDB" "select release_date from games_game where id = '$ID_QUERY'";)
  PLAYER_QUERY=$(sqlite3 "$APPDB" "select player from games_game where id = '$ID_QUERY'";)

  IFS=$'\n'
  TAGID_QUERY=($(sqlite3 "$APPDB" "select tag_id from games_game_tags where game_id = '$ID_QUERY'";))
  TAGARRAY=()
  for TAGID in "${TAGID_QUERY[@]}"
  do
    TAGS=$(sqlite3 "$APPDB" "select name from games_tag where id = '$TAGID';")
    TAGARRAY+=($TAGS)
  done

  DISPLAY_QUERY=$(sqlite3 "$APPDB" "select display from games_game where id = '$ID_QUERY'";)
  BOXART_QUERY=$(sqlite3 "$APPDB" "select boxart from games_game where id = '$ID_QUERY'";)

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
    <image>$MEDIADIR/$DISPLAY_QUERY</image>
  </game>" >>$ESGAMELISTDIR/gamelist.xml
  fi
done

echo -e "</gameList>" >>$ESGAMELISTDIR/gamelist.xml
