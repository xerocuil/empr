#!/bin/bash

. /opt/empr/config/settings.sh

PATH="$1"

/usr/bin/cp $PATH /opt/empr/docs/csv/import_game_data.csv

. $VENV/bin/activate
cd $CMSDIR
/usr/bin/python3 manage.py import_game_data
