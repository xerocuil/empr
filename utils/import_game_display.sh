#!/bin/bash

. /opt/empr/config/settings.sh

. $VENV/bin/activate
cd $CMSDIR
python3 manage.py import_game_display
