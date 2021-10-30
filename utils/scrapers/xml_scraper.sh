#! /bin/bash

#source $HOME/Applications/Empr/config/empr/settings.sh

path=$1
file=$2

GAMEPATH=$(xmlstarlet sel --template --value-of "/gameList/game[path = '$path']/path" "$file")
NAME=$(xmlstarlet sel --template --value-of "/gameList/game[path = '$path']/name" "$file")
IMAGE=$(xmlstarlet sel --template --value-of "/gameList/game[path = '$path']/image" "$file")
MARQUEE=$(xmlstarlet sel --template --value-of "/gameList/game[path = '$path']/marquee" "$file")
DESC=$(xmlstarlet sel --template --value-of "/gameList/game[path = '$path']/desc" "$file")
RELEASEDATE=$(xmlstarlet sel --template --value-of "/gameList/game[path = '$path']/releasedate" "$file")
DEVELOPER=$(xmlstarlet sel --template --value-of "/gameList/game[path = '$path']/developer" "$file")
PUBLISHER=$(xmlstarlet sel --template --value-of "/gameList/game[path = '$path']/publisher" "$file")
GENRE=$(xmlstarlet sel --template --value-of "/gameList/game[path = '$path']/genre" "$file")
PLAYERS=$(xmlstarlet sel --template --value-of "/gameList/game[path = '$path']/players" "$file")
KIDGAME=$(xmlstarlet sel --template --value-of "/gameList/game[path = '$path']/kidgame" "$file")

echo -e "
	PATH: $GAMEPATH
	NAME: $NAME
	IMAGE: $IMAGE
	MARQUEE: $MARQUEE
	DESC: $DESC
	RELEASEDATE: $RELEASEDATE
	DEVELOPER: $DEVELOPER
	PUBLISHER: $PUBLISHER
	GENRE: $GENRE
	PLAYERS: $PLAYERS
	KIDGAME: $KIDGAME
"
