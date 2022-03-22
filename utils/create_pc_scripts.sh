#!/bin/bash

source /opt/empr/config/settings.sh

LUTRIS_CACHE=$APPFILES/cache/lutris
LUTRIS_LIST=$LUTRIS_CACHE/lutris_list.txt
PC_LIST="$LUTRIS_CACHE/pc_list.txt"
PC_DIR=$ROMSDIR/pc

mkdir -p $LUTRIS_CACHE
cd $PC_DIR

lutris -l >$LUTRIS_LIST
IFS=$'\n'

LINES=$(cat $LUTRIS_LIST)

for LINE in $LINES
do
  slug="$(echo "$LINE" | cut -d "|" -f 3 | xargs)"
  echo -e "#!/bin/bash\nlutris lutris:rungame/$slug" >"$slug.sh"
  chmod +x "$slug.sh"
done
