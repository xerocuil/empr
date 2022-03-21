#!/bin/bash

source /opt/empr/config/settings.sh

LOCALGAMESDIR=/home/xerocuil/Games/roms
REMOTEGAMESDIR=/home/player1/Games/roms
PLATFORM=$1

mkdir -p $LOCALGAMESDIR/$PLATFORM
cd $LOCALGAMESDIR/$PLATFORM

for game in $(ssh arcade "ls $REMOTEGAMESDIR/$PLATFORM")
do
	touch "$game"
done
