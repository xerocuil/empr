#!/bin/bash

source /opt/empr/config/settings.sh

LUTRIS_CACHE=$APPFILES/cache/lutris
LUTRIS_LIST=$LUTRIS_CACHE/lutris_list.txt
PC_LIST="$LUTRIS_CACHE/pc_list.txt"
PC_DIR=$ROMSDIR/pc

mkdir -p $LUTRIS_CACHE

if [[ ! -d $PC_DIR ]]; then
  mkdir -p $PC_DIR
else
  rm -f $PC_DIR/*
fi

cd $PC_DIR

lutris -lo >$LUTRIS_LIST
IFS=$'\n'

LINES=$(cat $LUTRIS_LIST)

for LINE in $LINES
do
  slug="$(echo "$LINE" | cut -d "|" -f 3 | xargs)"
  echo -e "#!/bin/bash\nlutris lutris:rungame/$slug" >"$slug.sh"
  chmod +x "$slug.sh"
done
