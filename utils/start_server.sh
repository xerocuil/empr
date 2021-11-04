#!/bin/bash

source /opt/empr/config/settings.sh

cd $CMSDIR

dev(){
	tmux new -s $APPNAME -d
	tmux send-keys -t $APPNAME 'source ../venv/bin/activate; python3 manage.py runserver 0.0.0.0:8000' C-m
	tmux split-window -v -t $APPNAME
	tmux send-keys -t $APPNAME 'sass-watch games/static/css/style.sass' C-m
	tmux select-window -t $APPNAME:1
	tmux attach -t $APPNAME	
}

stop(){
	killall python3
}

$1
