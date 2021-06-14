#!/bin/bash

source $HOME/Applications/Empr/config/empr/settings.sh
FILE="$1"
BASENAME="$(basename $FILE)"
DIRNAME="$(dirname $FILE)"
PLATFORM="$(basename $DIRNAME)"
GAME="${BASENAME%.*}"
ARCHIVEDIR="/mnt/games/$PLATFORM"
PKGDIR="$CACHEDIR/pkg"

echo -e "
## DEBUGGING
------------
APPDB: $APPDB
APPDIR: $APPDIR
ARCHIVEDIR: $ARCHIVEDIR
BASENAME: $BASENAME
CACHEDIR: $CACHEDIR
DIRNAME: $DIRNAME
FILE: $FILE
GAME: $GAME
PKGDIR: $PKGDIR
PLATFORM: $PLATFORM
SQLITE: $SQLITE
UTILSDIR: $UTILSDIR
"

if [[ -z $FILE ]]; then
	echo "Please enter a file name."
	exit
else
	echo "Archiving $FILE"
fi

if [[ -d $ARCHIVEDIR ]]; then
	echo "$ARCHIVEDIR found."
else
	echo -e "$ARCHIVEDIR not found\n mounting..."
	sudo library mnt
	if [[ -d $ARCHIVEDIR ]]; then
		echo "Diretory mounted."
	else
		echo "Unable to mount directory."
		exit
	fi
fi

mkdir -p $PKGDIR
cd $DIRNAME
tar cvzf $PKGDIR/$GAME.tar.gz $(ls $GAME*)
cp -v $PKGDIR/$GAME.tar.gz $ARCHIVEDIR/
echo -e "\nArchive Complete!\n"
rm -rf $PKGDIR/*
