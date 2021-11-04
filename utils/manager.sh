#!/bin/bash
source /opt/empr/config/settings.sh

PHOTODB=$HOME/.empr/digikam

## Organize/Edit CMS photos
photos(){
	digikam --config $PHOTODB/photodb.ini --database-directory $PHOTODB
}

## Update source code
update-src(){
	cd $CMSDIR
	git pull origin main
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
	
	photos:    		Open CMS photo gallery in Digikam
	update-src:		Update source code
	update-server:	Update source code (server)
	"
}

$1

if [[ -z $1 ]]; then
	help
fi