UTILS="$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
source $UTILS/utils.sh

cd $CMS/media/games

> $HOME/Downloads/list.txt

for i in $(ls -1 title); do
  if [[ ! -z $(sqlite3 $CMS/db.sqlite3 "select title from games_game where title = 'games/title/$i';") ]]; then
    echo "Found: $i"
  else
    echo "NOT FOUND: $i"
    echo "$i" >> $HOME/Downloads/list.txt

  fi
done
