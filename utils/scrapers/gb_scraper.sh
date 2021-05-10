#! /bin/bash

source $HOME/apps/empr/config/config.sh

# Set Variables
#################

system="$1"
file="$2"
path=$(basename $file)
slug=$(echo $path | cut -d "." -f 1)
appdir="$emprAppDir/scraper"
asset_dir="$emprAssetsDir/$system/$slug"
cache_dir="$appdir/.cache"
gb_json_file="$cache_dir/gb_$slug.json"
gb_json_search_file="$cache_dir/gb_search_$slug.json"
tgdb_json_file="$cache_dir/tgdb_$slug.json"
tgdb_json_search_file="$cache_dir/tgdb_search_$slug.json"
tgdb_image_file="$cache_dir/tgdb_image_$slug.json"
readme=$asset_dir/readme.md

## Images
asset_icon=$asset_dir/icon.png
asset_boxart=$asset_dir/boxart.jpg
asset_background=$asset_dir/background.jpg

gb_asset_icon=$asset_dir/gb_icon.png
gb_asset_boxart=$asset_dir/gb_boxart.jpg
gb_asset_background=$asset_dir/gb_background.jpg

tgdb_asset_icon=$asset_dir/tgdb_icon.png
tgdb_asset_boxart=$asset_dir/tgdb_boxart.jpg
tgdb_asset_background=$asset_dir/tgdb_background.jpg
tgdb_asset_screenshot=$asset_dir/tgdb_screenshot.jpg

## API configuration
gb_api=56990bb9836a296be511b22236a52a6c6aca5dda
tgdb_apikey=fc021a8b97fe3d3e5977d7d403f1ca6cc50148ee4bbae951a47296eeb6970183
tgdb_apiurl="https://api.thegamesdb.net"

tgdb_developer_list=$appdir/tgdb/developers.json
tgdb_genre_list=$appdir/tgdb/genres.json
tgdb_platform_list=$appdir/tgdb/platforms.json
tgdb_publisher_list=$appdir/tgdb/publishers.json


# Set Functions
################

## Get GUID for Giant Bomb scraper
get_guid(){
	
	guid=$(zenity --list \
	--title="Choose the correct selection for $file | GiantBomb" --width=1080 --height=640 --column="Name" --column="Release_Date" --column="Description" --column="GUID" --print-column=4 \
${result_array[*]})
	
	## Verify GUID
	if [[ -z $guid ]]; then
			echo "No GiantBomb GUID Found"
			guid=$(zenity --entry \
				--title="Manually add GiantBomb GUID" \
				--text="Enter GiantBomb GUID:")
		else
			echo "GUID Found"
		fi
}

## If no GUID is entered, the program will exit
exit_scraper(){
	if [[ -z $guid ]]; then rm $cache_dir/*; rm $cache_dir/* ; exit; fi
}

## Get Game ID for TGDB
get_tgdb_id(){
	tgdb_id=$(zenity --list \
	--title="Choose the correct selection for $file | TGDB" --width=1080 --height=640 --column="Name" --column="Release Date" --column "Platform" --column="ID" --print-column=4 \
${tgdb_result_array[*]})

	### Enter TGDB ID manually if game not shown in results
	if [[ -z $tgdb_id ]]; then
		echo "### No TGDB ID Found"
		tgdb_id=$(zenity --entry \
			--title="Manually add TGDB ID" \
			--text="Enter TGDB ID:")
	fi
}

# Giant Bomb Scraper
#####################

gb_scraper(){
	## Create JSON file of search results if one does not exists
	if [[ ! -f $gb_json_search_file ]]; then
		curl -o $gb_json_search_file "https://www.giantbomb.com/api/search/?api_key=$gb_api&format=json&query='$slug'&resources=game&resource_type&field_list=deck,guid,name,original_release_date,platforms"
	fi

	## Get number of page results (max 10)
	page_results=$(cat $gb_json_search_file | jq '.number_of_page_results')
	result_cap=$(($page_results-1))

	## Get selected fields from search results in JSON format
	search_results_json=$(cat $gb_json_search_file | jq '.results[] | {name: .name, release_date: .original_release_date, description: .deck, platforms: [.platforms[].name], guid: .guid}')

	## Get search result fields
	IFS=$'\n'
	result_array=()
	for result in $(seq 0 $result_cap);
	do
		result_name=$(cat $gb_json_search_file | jq -r ".results[$result].name")
		result_date=$(cat $gb_json_search_file | jq -r ".results[$result].original_release_date")
		result_description=$(cat $gb_json_search_file | jq -r ".results[$result].deck")
		result_guid=$(cat $gb_json_search_file | jq -r ".results[$result].guid")
		#echo -e "$result_name $result_date $result_description $result_guid \\"
		result_array+=($result_name $result_date $result_description $result_guid)
	done

	echo -e "### Check for GUID"
	gb_guid=$cache_dir/$slug.guid
	check_gui_id=$(cat $gb_guid)
	if [[ -z $check_gui_id ]]; then get_guid; fi
	if [[ -z $guid ]]; then exit_scraper; else echo "$guid" >$gb_guid; fi

	## Get JSON data from giantbomb.com
	if [[ ! -f $gb_json_file ]]; then
		curl "https://www.giantbomb.com/api/game/$guid/?api_key=$gb_api&format=json&field_list=deck,developers,franchises,image,genres,name,original_game_rating,original_release_date,publishers,themes" | jq . >$gb_json_file
	fi


	## Scrape JSON file

	### Set delimiter to carriage return for JSON values.
	IFS=$'\n'

	### Get Giant Bomb Fields

	### Title
	gb_title=$(cat $gb_json_file | jq -r '.results.name')

	### Developer(s)
	gb_developer_array=$(cat $gb_json_file |jq -r '.results.developers[].name')
	gb_developers=()
	for gb_dev in $gb_developer_array; do gb_developers+=($gb_dev); done

	### Description
	gb_description=$(cat $gb_json_file |jq -r '.results.deck')

	### ESRB Rating
	gb_esrb=$(cat $gb_json_file | jq -r '.results.original_game_rating[].name'|cut -d ' ' -f 2|head -n 1)

	### Genre(s)/Tags
	gb_genre_array=$(cat $gb_json_file |jq -r '.results.genres[].name')
	gb_tag_array=$(cat $gb_json_file |jq -r '.results.themes[].name')

	gb_tags=()
	for gb_tag in $gb_tag_array; do gb_tags+=($gb_tag);  done
	for gb_gen in $gb_genre_array; do gb_tags+=($gb_gen); done

	### Publisher(s)
	gb_publisher_array=$(cat $gb_json_file |jq -r '.results.publishers[].name')
	gb_publishers=(); for gb_pub in $gb_publisher_array; do gb_publishers+=($gb_pub); done

	### Release Date
	gb_release_date=$(cat $gb_json_file |jq -r '.results.original_release_date')

	### Sort Title
	if [[ $title == A\ * ]]; then
		sort_title="$(echo $title | cut -d " " -f 2-), A"
	elif [[ $title == The\ * ]]; then
		sort_title="$(echo $title | cut -d " " -f 2-), The"
	else
		sort_title="$title"
	fi

	#if [[ ! -z $gb_title ]] ;then echo "No data found."; exit_scraper; fi

	## Get images

	### Create Asset Directory if it does not exist
	if [[ ! -d $asset_dir ]]; then
		mkdir -p $asset_dir
	fi

	## Boxart
	gb_boxart=$(cat $gb_json_file |jq -r '.results.image.original_url')
	if [[ ! -f $asset_dir/boxart.jpg ]]; then
		echo "No Boxart"
		boxart=0
		boxart_hr=False
		if [[ ! -f $asset_dir/boxart.jpg ]]; then
			wget -O $asset_dir/ $gb_boxart
		fi
	fi

	## Icon
	gb_icon=$(cat $gb_json_file |jq -r '.results.image.icon_url')
	if [[ ! -f $asset_dir/icon.png ]]; then
		echo "No Icon"
		icon=0
		icon_hr=False
		if [[ ! -f $asset_dir/icon.png ]]; then
			wget -O $asset_dir/ $gb_icon
		fi
	fi

	## Background
	gb_background=$(cat $gb_json_file |jq -r '.results.image.original_url')
	if [[ ! -f $asset_dir/background.jpg ]]; then
		echo "No Background"
		background=0
		background_hr=False
		if [[ ! -f $asset_dir/background.jpg ]]; then
			wget -O $asset_dir/background.jpg $gb_background
		fi
	fi
} ## /GiantBomb Scraper

# TGDB Scraper
###############
tgdb_scraper(){
	echo "$tgdb_apiurl"
	## Search for TGDB ID
	if [[ ! -f $tgdb_json_search_file ]]; then
		curl -o "$tgdb_json_search_file" "$tgdb_apiurl/v1.1/Games/ByGameName?apikey=$tgdb_apikey&name='$slug'&fields='genres,platform,release_date'"
	fi

	### Get remaining API allowance
	echo -e "\n ### API Allowance
	API calls left: $(cat $tgdb_json_search_file | jq .remaining_monthly_allowance)"
	allowance_refresh_timer=$(cat $tgdb_json_search_file | jq .allowance_refresh_timer)
	refresh_days=$(($allowance_refresh_timer/60/60/24))
	echo -e "Days until refresh: $refresh_days\n"

	### Get number of results
	tgdb_total_results=$(cat $tgdb_json_search_file | jq .data.count)
	tgdb_total_results_cap=$(($tgdb_total_results-1))

	### Get search result fields
	IFS=$'\n'

	echo -e "### tgdb_result_array"
	tgdb_result_array=()
	for tgdb_result in $(seq 0 $tgdb_total_results_cap);
	do
		tgdb_result_name=$(cat $tgdb_json_search_file | jq -r ".data.games[$tgdb_result].game_title")
		tgdb_result_release_date=$(cat $tgdb_json_search_file | jq -r ".data.games[$tgdb_result].release_date")
		tgdb_result_platform_id=$(cat $tgdb_json_search_file | jq -r ".data.games[$tgdb_result].platform")
		platform_name=$(cat $tgdb_platform_list | jq -r ". | select(.id==$tgdb_result_platform_id).name")
		tgdb_result_id=$(cat $tgdb_json_search_file | jq -r ".data.games[$tgdb_result].id")

		tgdb_result_array+=("$tgdb_result_name" "$tgdb_result_release_date" "$platform_name" "$tgdb_result_id")
	done

	echo -e "### Check for TGDB ID"
	tgdb_id=$(cat $tgdb_json_file | jq -r '.data.games[].id')
	if [[ -z $tgdb_id ]]; then get_tgdb_id; fi

	echo -e "### Get JSON data with TGDB ID"
	if [[ ! -f $tgdb_json_file ]]; then
		curl -o $tgdb_json_file "$tgdb_apiurl/v1/Games/ByGameID?apikey=$tgdb_apikey&id=$tgdb_id&fields=players,publishers,genres,overview,rating,platform"
	fi

	echo -e "## Get images\n"

	if [[ ! -f $tgdb_image_file ]]; then
		curl -o $tgdb_image_file "$tgdb_apiurl/v1/Games/Images?apikey=$tgdb_apikey&games_id=$tgdb_id"
	fi

	base_url=$(cat $tgdb_image_file | jq -r ".data.base_url.original")


	boxart_file=$(cat $tgdb_image_file | jq -r '.data.images[][] | select(.side == "front").filename')
	boxart_file_base=$(basename $boxart_file | cut -d '.' -f 1)
	boxart_file_ext=$(basename $boxart_file | cut -d '.' -f 2)
	if [[ ! -f $asset_boxart ]]; then
		echo "No Boxart"
		wget -q -P $asset_dir/ $base_url$boxart_file
		mv $asset_dir/$boxart_file_base.$boxart_file_ext $asset_dir/tgdb_boxart.$boxart_file_ext
	fi

	### Icon
	icon_file=$(cat $tgdb_image_file | jq -r '.data.images[][] | select(.type == "clearlogo" ).filename')
	icon_file_base=$(basename $icon_file | cut -d '.' -f 1)
	icon_file_ext=$(basename $icon_file | cut -d '.' -f 2)
	if [[ ! -f $asset_icon ]]; then
		echo "No Icon"
		wget -q -P $asset_dir/ $base_url$icon_file
		mv $asset_dir/$icon_file_base.$icon_file_ext $asset_dir/tgdb_icon.$icon_file_ext
	fi

	### Background
	background_file=$(cat $tgdb_image_file | jq -r '.data.images[][] | select(.type == "fanart").filename' | sed '1q;d')
	background_file_base=$(basename $background_file | cut -d '.' -f 1)
	background_file_ext=$(basename $background_file | cut -d '.' -f 2)
	if [[ ! -f $asset_background ]]; then
		echo "No background"
		wget -q -P $asset_dir/ $base_url$background_file
		mv $asset_dir/$background_file_base.$background_file_ext $asset_dir/tgdb_background.$background_file_ext
	fi

	### Screenshot
	screenshot_file=$(cat $tgdb_image_file | jq -r '.data.images[][] | select(.type == "screenshot").filename' | sed '1q;d')
	screenshot_file_base=$(basename $screenshot_file | cut -d '.' -f 1)
	screenshot_file_ext=$(basename $screenshot_file | cut -d '.' -f 2)
	if [[ ! -f $asset_screenshot ]]; then
		echo "No screenshot"
		wget -q -P $asset_dir/ $base_url$screenshot_file
		mv $asset_dir/$screenshot_file_base.$screenshot_file_ext $asset_dir/tgdb_screenshot.$screenshot_file_ext
	fi
} ## /TGDB Scraper

echo "
Looking up data for $file...
"

gb_scraper
tgdb_scraper

### Set delimiter to carriage return for JSON values.
IFS=$'\n'

## Title
tgdb_title=$(cat $tgdb_json_file | jq -r '.data.games[].game_title')

## Description
tgdb_description=$(cat $tgdb_json_file | jq -r '.data.games[].overview')

## Developer
tgdb_developer_id_array=()
tgdb_developer_name_array=()
tgdb_developer_id_array=$(cat $tgdb_json_file | jq -r '.data.games[].developers[]')
for dev_id in ${tgdb_developer_id_array}
do
 	tgdb_developer_name=$(cat $tgdb_developer_list | jq -r ". | select(.id==$dev_id).name")
 	tgdb_developer+=($tgdb_developer_name)
done

## Genre
tgdb_genre_id_array=()
tgdb_genre_name_array=()
tgdb_genre_id_array=$(cat $tgdb_json_file | jq -r '.data.games[].genres[]')
for tgdb_genre_id in ${tgdb_genre_id_array}
do
 	tgdb_genre_name=$(cat $tgdb_genre_list | jq -r ". | select(.id==$tgdb_genre_id).name")
 	tgdb_genre+=($tgdb_genre_name)
done

## Players
tgdb_players=$(cat $tgdb_json_file | jq -r ".data.games[].players")

echo -e "

# GiantBomb Report
###################

gb_guid:
$guid

gb_title:
$gb_title

gb_developers:
$gb_developers

gb_description:
$gb_description

gb_esrb:
$gb_esrb

gb_tags:
$gb_tags

gb_publishers:
$gb_publishers

gb_release_date:
$gb_release_date

# TGDB Report
##############

tgdb_id:
$tgdb_id

tgdb_title:
$tgdb_title

tgdb_description:
$tgdb_description

tgdb_developer:
$tgdb_developer

tgdb_genre:
${tgdb_genre[*]}

tgdb_players:
$tgdb_players
"

# Display Report
################

IFS=$', '

generate_readme(){
echo -e "# $gb_title\n
## Database Info

| Field | Value |
|:--- |:--- |
| Description | $gb_description |
| Alt. Description | $tgdb_description |
| Developer(s) | $gb_developers |
| Alt. Developer(s) | $tgdb_developer |
| ESRB Rating | $gb_esrb |
| Path | $path |
| System | $system |
| Genre | ${tgdb_genre[*]} |
| Player(s) | $tgdb_players |
| Publisher(s) | $gb_publishers |
| Release Date | $gb_release_date |
| Slug | $slug |
| Sort Title | $sort_title |
| Tag(s) | $gb_tags |

" >$readme
}

generate_readme

if [[ ! -f $readme ]]; then
	echo "No readme file."
	generate_readme
else
	echo "Readme file found."
fi

## Edit review in text editor
subl $readme
