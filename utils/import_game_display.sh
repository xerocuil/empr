#!/bin/bash

. /opt/empr/config/settings.sh

# FILE="$1"
# game_data=$APPDIR/docs/csv/import_data.csv
# cp "$FILE" "$game_data"

. $VENV/bin/activate
cd $CMSDIR
python3 manage.py import_game_display
