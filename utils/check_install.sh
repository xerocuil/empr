#!/bin/bash

source $HOME/Applications/Empr/config/empr/settings.sh
echo -e "
APPDIR: $APPDIR
APPDIR: $APPDB
UTILS: $UTILSDIR
SQLITE: $SQLITE
"

path_query(){
	$SQLITE "$APPDB" "select path,platform_id from games_game where 1;"
}

platform_query(){
	$SQLITE "$APPDB" "select slug,path from games_platform where id = '$GAMEPLATFORMID';"
}

GAMEDATA=($(path_query))
for i in "${GAMEDATA[@]}"
do
	IFS="|"
	GAME=($i)
	GAMEPATH=${GAME[0]}
	GAMEPLATFORMID=${GAME[1]}
	PLATFORMDATA=($(platform_query))
	PLATFORMSLUG=${PLATFORMDATA[0]}
	PLATFORMPATH=${PLATFORMDATA[1]}
	FULLPATH="$PLATFORMPATH/$GAMEPATH"

	if [[ -f $FULLPATH ]]; then
		echo "something here: $FULLPATH"
	else
		echo "nothing at $FULLPATH"
	fi

# 	echo "
# GAMEPATH: $GAMEPATH
# GAMEPLATFORMID: $GAMEPLATFORMID
# PLATFORMSLUG: $PLATFORMSLUG
# PLATFORMPATH: $PLATFORMPATH

# FULLPATH: $FULLPATH
# "
done
