#! /bin/bash

source $HOME/Applications/Empr/config/empr/settings.sh
SCRAPERRDIR=$UTILSDIR/scrapers
CACHEDIR=$SCRAPERRDIR/.cache

## Make sure library is mounted
library=$CACHEDIR/md

if [[ -d $library ]]; then
	echo "Library found."
else
	echo "Library not found."
	mkdir -p $library
fi

## Set variables
file="$1"
path=$(basename $file)
slug=$(echo $path | cut -d "." -f 1)
tgdb_apikey=fc021a8b97fe3d3e5977d7d403f1ca6cc50148ee4bbae951a47296eeb6970183
tgdb_apiurl="https://api.thegamesdb.net"

json_dir="$CACHEDIR/json"
json_file="$json_dir/$slug.json" 
json_search_file="$json_dir/search_$slug.json"
tgdb_file="$json_dir/tgdb_$slug.json"
tgdb_search_file="$json_dir/tgdb_search_$slug.json"
tgdb_image_file="$json_dir/tgdb_image_$slug.json"

developer_list=$CACHEDIR/tgdb/developers.json
genre_list=$CACHEDIR/tgdb/genres.json
platform_list=$CACHEDIR/tgdb/platforms.json
publisher_list=$CACHEDIR/tgdb/publishers.json


## Check file
path_query(){
	$SQLITE "$APPDB" "select id from games_game where path = '$path'"
}

if [[ -z $(path_query) ]];then
	echo "No path in database."
else
	echo "Path found in database: id# $(path_query)"
	exit
fi

## Search for TGDB ID
#####################

if [[ ! -f $tgdb_search_file ]]; then
	curl -o $tgdb_search_file "$tgdb_apiurl/v1.1/Games/ByGameName?apikey=$tgdb_apikey&name='$slug'&fields='genres,platform,release_date'"
fi

### Get remaining API allowance
echo -e "\n ### API Allowance
API calls left: $(cat $tgdb_search_file | jq .remaining_monthly_allowance)"
allowance_refresh_timer=$(cat $tgdb_search_file | jq .allowance_refresh_timer)
refresh_days=$(($allowance_refresh_timer/60/60/24))
echo -e "Days until refresh: $refresh_days\n"

### Get number of results
tgdb_total_results=$(cat $tgdb_search_file | jq .data.count)
tgdb_total_results_cap=$(($tgdb_total_results-1))

### Show HR field data
search_results_json="$(cat $tgdb_search_file | jq '.data.games[] | {game_title: .game_title, release_date: .release_date, platform: .platform, tgdb_id: .id}')"

### Get search result fields
IFS=$'\n'

echo -e "tgdb_result_array\n"
>$CACHEDIR/tgdb/search_results.txt
for tgdb_result in $(seq 0 $tgdb_total_results_cap);
do
	tgdb_result_name=$(cat $tgdb_search_file | jq -r ".data.games[$tgdb_result].game_title")
	tgdb_result_release_date=$(cat $tgdb_search_file | jq -r ".data.games[$tgdb_result].release_date")
	tgdb_result_platform_id=$(cat $tgdb_search_file | jq -r ".data.games[$tgdb_result].platform")
	platform_name=$(cat $platform_list | jq -r ". | select(.id==$tgdb_result_platform_id).name")
	tgdb_result_id=$(cat $tgdb_search_file | jq -r ".data.games[$tgdb_result].id")
	echo "$tgdb_result_id: $tgdb_result_name, $platform_name, $tgdb_result_release_date"
done

tgdb_id=$(zenity --entry \
	--title="Add new game" \
	--text="Enter correct TGDB ID for $slug:" \
)

#read tgdb_id

### If no TGDB ID is entered, the program will exit
if [[ -z $tgdb_id ]]; then rm $json_dir/*; exit; fi

### Get JSON data with TGDB ID
if [[ ! -f $tgdb_file ]]; then
	curl -o $tgdb_file "$tgdb_apiurl/v1/Games/ByGameID?apikey=$tgdb_apikey&id=$tgdb_id&fields=players,publishers,genres,overview,rating,platform,coop,os,processor,ram,hdd,video,sound,alternates"
fi


## Scrape TGDB with selected GUID
#################################

### Set delimiter to carriage return for JSON values.
IFS=$'\n'

### Get fields

coop=$(cat $tgdb_file | jq -r '.data.games[].coop')
description=$(cat $tgdb_file | jq -r '.data.games[].overview')

### Get developer
developer_id_array=()
developer_name_array=()
developer_id_array=$(cat $tgdb_file | jq -r '.data.games[].developers[]')
for dev_id in $developer_id_array
do
	developer_name=$(cat $developer_list | jq -r ". | select(.id==$dev_id).name")
	developer_name_array+=($developer_name)
done

### Get genre
genre_id_array=()
genre_name_array=()
genre_id_array=$(cat $tgdb_file | jq -r '.data.games[].genres[]')
for genre_id in $genre_id_array
do
	genre_name=$(cat $genre_list | jq -r ". | select(.id==$genre_id).name")
	genre_name_array+=($genre_name)
done

### Get platform
platform_id=$(cat $tgdb_file | jq -r ".data.games[].platform")
platform_name=$(cat $platform_list | jq -r ". | select(.id==$platform_id).alias")
platform_title=$(cat $platform_list | jq -r ". | select(.id==$platform_id).name")
players=$(cat $tgdb_file | jq -r ".data.games[].players")

### Get publisher
publisher_id_array=()
publisher_name_array=()
publisher_id_array=$(cat $tgdb_file | jq -r '.data.games[].publishers[]')
for pub_id in $publisher_id_array
do
	publisher_name=$(cat $publisher_list | jq -r ". | select(.id==$pub_id).name")
	publisher_name_array+=($publisher_name)
done

### Get release
release_date=$(cat $tgdb_file | jq -r ".data.games[].release_date")
rating=$(cat $tgdb_file | jq -r ".data.games[].rating"| cut -d ' ' -f 1)
title=$(cat $tgdb_file | jq -r '.data.games[].game_title')

### Get sort title
if [[ $title == A\ * ]]; then
	sort_title="$(echo $title | cut -d " " -f 2-), A"
elif [[ $title == The\ * ]]; then
	sort_title="$(echo $title | cut -d " " -f 2-), The"
else
	sort_title="$title"
fi

### Get images
asset_dir="$APPDIR/cache/assets"
asset_boxart=$asset_dir/$slug-boxart.jpg
asset_background=$asset_dir/$slug-fanart.jpg
readme=$library/$slug.md
mkdir -p $asset_dir

if [[ ! -f $tgdb_image_file ]]; then
	curl -o $tgdb_image_file "$tgdb_apiurl/v1/Games/Images?apikey=$tgdb_apikey&games_id=$tgdb_id"
fi

base_url=$(cat $tgdb_image_file | jq -r ".data.base_url.original")

#### Boxart
boxart_file=$(cat $tgdb_image_file | jq -r '.data.images[][] | select(.side == "front").filename')
boxart_file_base=$(basename $boxart_file | cut -d '.' -f 1)
boxart_file_ext=$(basename $boxart_file | cut -d '.' -f 2)
if [[ ! -f $asset_boxart ]]; then
	echo "No Boxart"
	wget -q -P $asset_dir/ $base_url$boxart_file
	mv $asset_dir/$boxart_file_base.$boxart_file_ext $asset_dir/$slug-boxart.$boxart_file_ext
fi

#### Background
background_file=$(cat $tgdb_image_file | jq -r '.data.images[][] | select(.type == "fanart").filename' | sed '1q;d')
background_file_base=$(basename $background_file | cut -d '.' -f 1)
background_file_ext=$(basename $background_file | cut -d '.' -f 2)
if [[ ! -f $asset_background ]]; then
	echo "No background"
	wget -q -P $asset_dir/ $base_url$background_file
	mv $asset_dir/$background_file_base.$background_file_ext $asset_dir/$slug-background.$background_file_ext
fi

## Clean up JSON directory (delete files older than a day)
# find $json_dir* -mtime +1 -exec rm {} \;
# #rm $json_dir/*.json

firefox "http://empr.local/admin/games/game/add/?title=$title&sort_title=$sort_title&slug=$slug&genre=$genre&developer=${developer_name_array[*]}&publisher=${publisher_name_array[*]}&release_date=$release_date&path=$path&description=$description" &
