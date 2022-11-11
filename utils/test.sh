UTILS="$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
source $UTILS/utils.sh

for platform in $(ls -1 $ARCHIVEDIR/roms/)
do
  mkdir -p "$ROMSDIR/$platform"
  for g in $(ls -1 $ARCHIVEDIR/roms/$platform)
  do
    touch "$ROMSDIR/$platform/$g"
  done
done