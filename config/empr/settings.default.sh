#!/bin/bash

## Empr Settings
APPDIR="$HOME/Applications/Empr"
APPNAME="$(basename $APPDIR)"
CMSDIR="$APPDIR/cms"
CACHEDIR="$HOME/.cache/empr"
APPDB="$CMSDIR/db.sqlite3"
CONFIGDIR="$APPDIR/config"
UTILSDIR="$APPDIR/utils"
VENV="$APPDIR/venv"

## System Settings
SQLITE="/usr/bin/sqlite3"
