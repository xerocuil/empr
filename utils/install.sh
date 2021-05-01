#!/bin/bash
source ~/Applications/Empr/config/empr/settings.sh
GAMELAUNCHER="/usr/local/bin/game-launcher"
EMULATIONSTATION="$HOME/Applications/EmulationStation"

## Install Game Launcher
if [[ -f $GAMELAUNCHER ]]; then
	sudo rm -rf $GAMELAUNCHER
fi

sudo ln -s $UTILSDIR/game-launcher.sh $GAMELAUNCHER


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
}

if [[ ! -d $EMULATIONSTATION ]]; then
	echo -e "\nEmulationStation not found.\n"
	install_es
	ln -s $APPDIR/config/emulationstation ~/.emulationstation
else
	echo -e "\nEmulationStation found.\n"
fi

## Install Python Environment
install_python_env(){
	sudo apt-get install -y git htop jq python3 \
	python3-pip python3-venv tmux vim
	echo "\nVirtual Environment not found.\n"
	cd $APPDIR
	python3 -m venv $VENV

	cd $CMSDIR
	source $VENV/bin/activate
	python3 -m pip install -r requirements.txt
}

if [[ ! -d $VENV ]]; then
	echo -e "\nPython Environment not found.\n"
	install_python_env
else
	echo -e "\nPython Environment found.\n"
fi
