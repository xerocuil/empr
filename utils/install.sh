#!/bin/bash

sudo apt-get update ; sudo apt-get install -y git

if [[ ! -d $HOME/Applications/Empr ]]; then
	echo -e "\nEmpr not found.\n"
	mkdir -p $HOME/Applications
	cd $HOME/Applications
	git clone ssh://pi@192.168.0.144/home/pi/Git/empr Empr
	cd Empr/config/empr
	cp settings.default.sh settings.sh
fi

source ~/Applications/Empr/config/empr/settings.sh

GAMELAUNCHER="/usr/local/bin/game-launcher"
EMULATIONSTATION="$HOME/Applications/EmulationStation"
ESCONFIG=$CONFIGDIR/emulationstation
ESLAUNCHER="/usr/local/bin/emulationstation"

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
	echo -e "\nVirtual Environment not found.\n"
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

if [[ ! -f $ESLAUNCHER ]]; then
	echo -e "\nEmulationStation Launcher not found.\n"
	sudo cp "$ESCONFIG/launcher.sh" "$ESLAUNCHER"
	cp "$ESCONFIG/EmulationStation.desktop" "$HOME/.local/share/applications/"
	mkdir -p "$HOME/.icons"
	cp "$ESCONFIG/emulationstation.svg" "$HOME/.icons/"
else
	echo -e "\nEmulationStation Launcher found.\n"
fi
