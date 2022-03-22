#!/bin/bash

## Empr Settings
APPDIR="/opt/empr"
APPFILES="$HOME/.empr"
APPNAME="$(/usr/bin/basename $APPDIR)"
CMSDIR="$APPDIR/cms"
CACHEDIR="$APPFILES/cache"
APPDB="$CMSDIR/db.sqlite3"
CONFIGDIR="$APPDIR/config"
UTILSDIR="$APPDIR/utils"
VENV="$APPDIR/venv"

## Game Settings
GAMESDIR="$HOME/Games"
ROMSDIR="$GAMESDIR/roms"

## System Settings
SQLITE="/usr/bin/sqlite3"
