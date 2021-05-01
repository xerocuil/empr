#!/bin/bash
source $HOME/Applications/Empr/config/empr/settings.sh

cd $CMSDIR

dev(){
	tmux new -s $APPNAME -d
	tmux send-keys -t $APPNAME 'source ../venv/bin/activate; python3 manage.py runserver' C-m
	tmux split-window -v -t $APPNAME
	tmux send-keys -t $APPNAME 'sass-watch games/static/css/style.sass' C-m
	tmux select-window -t $APPNAME:1
	tmux attach -t $APPNAME	
}

app(){
	source ../venv/bin/activate
	nohup python3 manage.py runserver &>/dev/null &
	sleep 2
	$APPDIR/browser/browser.sh &>/dev/null &
}

stop(){
	killall python3
}

$1
