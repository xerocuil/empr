#!/bin/bash

. /opt/empr/config/settings.sh

. $VENV/bin/activate
cd $CMSDIR
/usr/bin/python3 manage.py import_game_display
