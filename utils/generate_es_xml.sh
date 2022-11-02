#! /bin/bash

UTILS="$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
APPDIR="$(dirname $UTILS)"
source $UTILS/utils.sh

PLATFORMS=($(sqlite3 "$APPDB" "select slug from games_platform";))
MEDIADIR="$APPFILES/media"

generate_xml(){
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

    if [[ -z $DISPLAY_QUERY ]]; then
      IMAGE="$BOXART_QUERY"
    else
      IMAGE="$DISPLAY_QUERY"
    fi

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
      <image>$MEDIADIR/$IMAGE</image>
    </game>" >>"$ESGAMELISTDIR/gamelist.xml"
    fi
  done

  echo -e "</gameList>" >>"$ESGAMELISTDIR/gamelist.xml"

  echo -e "<theme>
    <formatVersion>4</formatVersion>
    <include>./../empr.xml</include>  
    <view name=\"system, basic, detailed\">
      <image name=\"logo\">
        <path>./system.svg</path>
      </image>
    </view>
  </theme>" >"$ESTHEME/theme.xml"
}

echo -e "
UTILS: $UTILS
APPDIR: $APPDIR
"

for PLATFORM in ${PLATFORMS[*]}
do
  PLATFORMDIR="$ROMSDIR/$PLATFORM"
  ESGAMELISTDIR="$HOME/.emulationstation/gamelists/$PLATFORM"
  ESTHEME="$HOME/.emulationstation/themes/empr/$PLATFORM"

  if [[ -d $PLATFORMDIR ]]; then
    GAMES=$(ls -1 $PLATFORMDIR)
  fi

  if [[ -d $PLATFORMDIR ]]; then
    mkdir -p $ESGAMELISTDIR $ESTHEME
    generate_xml "$PLATFORM"
  fi
done
