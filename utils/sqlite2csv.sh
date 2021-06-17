#!/bin/bash

source $HOME/Applications/Empr/config/empr/settings.sh

EXPORTDIR="$APPDIR/docs/export"

echo -e "
## DEBUGGING
------------
APPDB: $APPDB
APPDIR: $APPDIR
CACHEDIR: $CACHEDIR
SQLITE: $SQLITE
UTILSDIR: $UTILSDIR
EXPORTDIR: $EXPORTDIR
"

cd $EXPORTDIR

sqlite3 $APPDB <<EOF
.headers on
.mode csv
.once games.csv
select * from games_game;
.exit
EOF

sqlite3 $APPDB <<EOF
.headers on
.mode csv
.once genres.csv
select * from games_genre;
.exit
EOF

sqlite3 $APPDB <<EOF
.headers on
.mode csv
.once platforms.csv
select * from games_platform;
.exit
EOF

sqlite3 $APPDB <<EOF
.headers on
.mode csv
.once game_tags.csv
select * from games_game_tags;
.exit
EOF

sqlite3 $APPDB <<EOF
.headers on
.mode csv
.once tags.csv
select * from games_tag;
.exit
EOF