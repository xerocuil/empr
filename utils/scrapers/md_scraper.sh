#! /bin/bash

source $HOME/apps/empr/config/config.sh

browserDir=$emprAppDir/browser
db=$HOME/apps/empr/web/db.sqlite3
markdownpath=$1

#database=/home/xerocuil/dev/htdocs/empr-gui/db/test.sqlite3

echo "
markdown path: $markdownpath
"

echo "
Markdown file found.
"
getfield(){
	fieldname=$2
	markdownpath=$1
	if [[ $fieldname = "title" ]]; then
		cat $markdownpath | grep -w -m 1 "#" | cut -d "#" -f 2 | awk '{$1=$1};1';
	else
		cat $markdownpath | grep -w "$fieldname" | cut -d "|" -f 3 | awk '{$1=$1};1';
	fi
}

### Title
title=$(getfield $markdownpath Title)
echo "Title:" $title

### Collection
collection=$(getfield $markdownpath Collection)
echo "Collection:" $collection

### Controller Support
controller=$(getfield $markdownpath "Controller Support")
echo "Controller Support:" $controller

### Description
description=$(getfield $markdownpath Description)
echo "Description:" $description

### Developer
developer=$(getfield $markdownpath "Developer(s)")
echo "Developer:" $developer

### Genre
genre=$(getfield $markdownpath Genre)
echo "Genre:" $genre

### ESRB
esrb=$(getfield $markdownpath ESRB)
echo "ESRB:" $esrb

### Path
path=$(getfield $markdownpath Path)
echo "Path:" $path

### Platform
platform=$(getfield $markdownpath Platform)
echo "Platform:" $platform

### Player(s)
players=$(getfield $markdownpath "Player(s)")
echo "Player(s):" $players

### Publisher
publisher=$(getfield $markdownpath Publisher)
echo "Publisher:" $publisher

### Release Date
release_date=$(getfield $markdownpath "Release Date")
echo "Release Date:" $release_date
xml_date=$(date -d"$release_date" +%Y%m%d)
echo "XML Date:" $xml_date

### Sort Title
sort_title=$(getfield $markdownpath "Sort Title")
echo "Sort Title:" $sort_title

### Source
source=$(getfield $markdownpath Source)
echo "Source:" $source

### Slug
slug=$(getfield $markdownpath Slug)
echo "Slug:" $slug

### System
system=$(getfield $markdownpath System)
echo "Slug:" $system

### Tags
tags=$(getfield $markdownpath Tags)
echo "Tags:" $tags

### XML Report
echo "
XML Report ...
"

echo "
	<game>
		<path>./$path</path>
		<name>$title</name>
		<desc>$description</desc>
		<image>~/.assets/$system/$slug/boxart.jpg</image>
		<releasedate>$xml_date</releasedate>
		<developer>$developer</developer>
		<publisher>$publisher</publisher>
		<genre>$genre</genre>
		<players>$players</players>
	</game>
"

url="http://127.0.0.1:8088/scrape_game/?title=$title&sort_title=$sort_title&slug=$slug&system=$system&path=$path&description=$description&tag=$tag&esrb=$esrb&players=$players&release_date=$release_date&developer=$developer&publisher=$publisher"

check_db(){
	sqlite3 $db <<EOF
select title from royal_game where system_id=17
EOF
}

check_db2(){
	sqlite3 ${db} <<EOF
select * from royal_game where system_id=17;
EOF
}
#check_db
for g in "$(check_db2)"; do echo "$g"; done
#if [[ -z $(check_db) ]]; then echo "no variable!"; else echo "variable found!"; exit; fi

#$browserDir/add_to_db.sh "$url"

# sqlite3 $database <<EOF
# insert into games (slug, title, genre, publisher, developer, release_date, description) values ("$slug", "$title", "$genre", "$publisher", "$developer", "$release_date", "$description");
# EOF

# gamedata=$(zenity --forms \
# --text="Add Game to Database"  \
# --add-entry="Title" --entry-text="Type" \
# --add-entry="Slug" \
# --add-entry="Release Date (YMD)"  \
# --add-entry="Developer"  \
# --add-combo="Platform" --combo-values=$(cat config |grep platforms|cut -f2- -d"=") \
# --forms-date-format=%Y%m%d)
#zenity --entry --title "Window title" --text "Insert your choice." a b c d e