#!/bin/bash

source /opt/empr/config/settings.sh

RUNNERS_DIR=$APPDIR/plugins/lutris/runners

LUTRIS_LOCAL_SHARE="$HOME/.local/share/lutris"
LUTRIS_USER_SHARE="/usr/share/lutris"

sudo cp -v $RUNNERS_DIR/json/empr.* $LUTRIS_USER_SHARE/json/
cp -rv $RUNNERS_DIR/empr $LUTRIS_LOCAL_SHARE/runners/
