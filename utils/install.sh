#!/bin/bash

source ~/Applications/Empr/config/empr/settings.sh

GAMELAUNCHER="/usr/local/bin/game-launcher"
EMULATIONSTATION="$HOME/Applications/EmulationStation"
ESCONFIG=$CONFIGDIR/emulationstation
ESLAUNCHER="/usr/local/bin/emulationstation"

## Install Game Launcher


## Install packages
install_pkgs(){
	echo -e "## Installing system dependencies. ##"
	sudo apt-get install \
		csvkit \
		git \
		mono-runtime \
		python3 \
		python3-dev \
		python3-django \
		python3-pip \
		python3-venv \
		python3-wheel \
		tmux \
		vim
}

## Install Empr
install_empr(){
	if [[ ! -d $HOME/Applications/Empr ]]; then
		echo -e "\nEmpr not found.\n"
		mkdir -p $HOME/Applications
		cd $HOME/Applications
		git clone ssh://pi@192.168.0.144/home/pi/Git/empr Empr
		cd Empr/config/empr
		cp settings.default.sh settings.sh
		sudo rm -rf $GAMELAUNCHER
		sudo ln -s $UTILSDIR/game-launcher.sh $GAMELAUNCHER
	fi
}

## Install EmulationStation (Debian/Ubuntu)
install_es(){
	## Install Dependencies
	sudo apt-get install -y libsdl2-dev libfreeimage-dev \
	libfreetype6-dev libcurl4-openssl-dev rapidjson-dev \
	libasound2-dev libgles2-mesa-dev build-essential cmake \
	fonts-droid-fallback libvlc-dev libvlccore-dev vlc-bin

	## Download/Build/Install
	mkdir -p ~/Applications
	cd ~/Applications
	git clone --recursive https://github.com/RetroPie/EmulationStation.git
	cd EmulationStation
	cmake .
	make
	ln -s $CONFIGDIR/emulationstation ~/.emulationstation
	ln -s $CMSDIR/media ~/.empr
	if [[ ! -f $ESLAUNCHER ]]; then
		echo -e "\nEmulationStation Launcher not found.\n"
		sudo cp "$ESCONFIG/launcher.sh" "$ESLAUNCHER"
		cp "$ESCONFIG/EmulationStation.desktop" "$HOME/.local/share/applications/"
		mkdir -p "$HOME/.icons"
		cp "$ESCONFIG/emulationstation.svg" "$HOME/.icons/"
	else
		echo -e "\nEmulationStation Launcher found.\n"
	fi
}

## Create Python Environment
install_python_env(){
	cd $APPDIR
	python3 -m venv $VENV
	cd $CMSDIR
	source $VENV/bin/activate
	python3 -m pip install -r requirements.txt
}


## Install Production Environment
install_prod_env(){
	sudo apt-get install -y \
		curl \
		libpq-dev \
		nginx \
		postgresql \
		postgresql-contrib \
		python3-dev \
		python3-pip
}

sudo apt-get update ; sudo apt-get upgrade -y
install_empr

$1
