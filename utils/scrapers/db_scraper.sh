#!/bin/bash

source $HOME/.config/empr/config.sh

SCRAPERDIR=$UTILSDIR/scrapers
CACHE=$CACHEDIR/xml
PLATFORM_SLUG="$1"

game_query(){
	PATH="$1"

	path_query(){
		$SQLITE "$APPDB" "select * from games_game where path = '$PATH'"
	}

	genre_query(){
		$SQLITE "$APPDB" "select name from games_genre where id = '$game_genre_id'"
	}

	IFS="|"
	GAMEDATA=($(path_query))

	game_id=${GAMEDATA[0]}
	game_title=${GAMEDATA[1]}
	game_sort_title=${GAMEDATA[2]}
	game_controller_support=${GAMEDATA[3]}
	game_date_added=${GAMEDATA[4]}
	game_date_modified=${GAMEDATA[5]}
	game_description=${GAMEDATA[6]}
	game_developer=${GAMEDATA[7]}
	game_esrb=${GAMEDATA[8]}
	game_hidden=${GAMEDATA[9]}
	game_notes=${GAMEDATA[10]}
	game_path=${GAMEDATA[11]}
	game_player=${GAMEDATA[12]}
	game_online_multiplayer=${GAMEDATA[13]}
	game_publisher=${GAMEDATA[14]}
	game_rating=${GAMEDATA[15]}
	game_region=${GAMEDATA[16]}
	game_release_date=${GAMEDATA[17]}
	game_store=${GAMEDATA[18]}
	game_genre_id=${GAMEDATA[19]}
	game_genre=$(genre_query)
	game_platform_id=${GAMEDATA[20]}
	game_boxart=${GAMEDATA[21]}
	game_wallpaper=${GAMEDATA[22]}
	game_favorite=${GAMEDATA[23]}
	game_kid_friendly=${GAMEDATA[24]}
	game_co_op=${GAMEDATA[25]}
	game_installed=${GAMEDATA[25]}

	favorite_bool(){
		if [[ $game_favorite == '0' ]]; then
			echo "False"
		else
			echo "True"
		fi
	}

	echo "	<game>
		<path>./$PATH</path>
		<name>$game_title</name>
		<sortname>$game_sort_title</sortname>
		<desc>$game_description</desc>
		<image>~/.empr/$game_boxart</image>
		<releasedate>$game_release_date</releasedate>
		<developer>$game_developer</developer>
		<publisher>$game_publisher</publisher>
		<genre>$game_genre</genre>
		<players>$game_player</players>
		<favorite>$(favorite_bool)</favorite>
	</game>" >>$CACHE/$PLATFORM_SLUG.gamelist.xml
}

list_games(){
	PLATFORM_ID=$($SQLITE "$APPDB" "select id from games_platform where slug = '$PLATFORM_SLUG'")
	$SQLITE "$APPDB" "select path from games_game where platform_id = '$PLATFORM_ID' and installed = '1'"
}

mkdir -p $CACHE

echo "<?xml version=\"1.0\"?>
<gameList>" >$CACHE/$PLATFORM_SLUG.gamelist.xml

for g in $(list_games)
do
	game_query "$g"
done

echo "</gameList>" >>$CACHE/$PLATFORM_SLUG.gamelist.xml