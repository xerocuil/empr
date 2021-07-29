#!/bin/bash

source $HOME/.config/empr/config.sh


# check_pc_games(){
# 	find_pc_path(){
# 		$SQLITE "$APPDB" "select path from games_platform where slug = 'pc'";
# 	}
# 	PCPATH=$(find_pc_path)
# 	echo -e "\nPCPATH: $PCPATH\n"
# }

list_platforms(){
	$SQLITE "$APPDB" "select id,slug,platform_type from games_platform where 1;"
}

list_games(){
	$SQLITE "$APPDB" "select path from games_game where platform_id = $PLATFORMID order by path;"
}

PLATFORMLIST=($(list_platforms))

#echo ${PLATFORMLIST[@]}

for platform in ${PLATFORMLIST[@]}
do
	PLATFORMID=$(echo $platform | cut -d "|" -f 1)
	PLATFORMSLUG=$(echo $platform | cut -d "|" -f 2)
	PLATFORMTYPE=$(echo $platform | cut -d "|" -f 3)

	echo -e "\nid: $PLATFORMID\nslug: $PLATFORMSLUG\ntype: $PLATFORMTYPE"
	mkdir -p $CONFIGDIR/gamelists/$PLATFORMSLUG

	if [[ $PLATFORMTYPE == "APP" ]];then
		PLATFORMDIR=$GAMEDIR/launchers/$PLATFORMSLUG
	elif [[ $PLATFORMTYPE == "EMU" ]]; then
		PLATFORMDIR=$GAMEDIR/$PLATFORMSLUG
	else
		echo -e "\nError finding platform type."
	fi

	GAMELIST=($(list_games))
	for game in ${GAMELIST[@]}
	do
		if [[ -f $PLATFORMDIR/$game ]]; then
			echo "$game found!"
		else
			echo "$game not found."
		fi
	done
done

# path_query(){
# 	$SQLITE "$APPDB" "select path,platform_id from games_game where 1 order by path;"
# }

# platform_query(){
# 	$SQLITE "$APPDB" "select slug,platform_type from games_platform where id = '$GAMEPLATFORMID';"
# }

# #check_pc_games


# GAMEDATA=($(path_query))
# for i in "${GAMEDATA[@]}"
# do
# 	IFS="|"
# 	GAME=($i)
# 	GAMEPATH=${GAME[0]}
# 	GAMEPLATFORMID=${GAME[1]}
# 	PLATFORMDATA=($(platform_query))
# 	PLATFORMSLUG=${PLATFORMDATA[0]}
# 	PLATFORMTYPE=${PLATFORMDATA[1]}
# 	if [[ $PLATFORMTYPE == "APP" ]]; then
# 		PLATFORMPATH=$GAMEDIR/launchers/$PLATFORMSLUG
# 	elif [[ $PLATFORMTYPE == "EMU" ]]; then
# 		PLATFORMPATH=$GAMEDIR/$PLATFORMSLUG
# 	else
# 		echo -e "\nError finding platform path."
# 	fi

# 	FULLPATH=$PLATFORMPATH/$GAMEPATH

# 	if [[ -e $FULLPATH ]]; then
# 		echo "something here: $FULLPATH"
# 	else
# 		echo "nothing at $FULLPATH"
# 	fi

# 	echo "
# GAMEPATH: $GAMEPATH
# GAMEPLATFORMID: $GAMEPLATFORMID
# PLATFORMSLUG: $PLATFORMSLUG
# PLATFORMTYPE: $PLATFORMTYPE
# FULLPATH: $FULLPATH
# "

# done
