#!/bin/bash
source /opt/empr/config/settings.sh

## Update source code
update-src(){
	cd $CMSDIR
	git pull origin
	. $VENV/bin/activate
	python3 -m pip install -r requirements.txt
	python3 manage.py makemigrations
	python3 manage.py migrate
}

## Update server
update-server(){
	update-src
	cd $CMSDIR
	. $VENV/bin/activate
	python3 manage.py collectstatic --noinput
	sudo service nginx restart
	sudo service gunicorn restart
}



help(){
	echo -e "
	Empr CLI Apps
	
	Options
	-------
	
	update-src:		Update source code
	update-server:	Update source code (server)
	"
}

$1

if [[ -z $1 ]]; then
	help
fi