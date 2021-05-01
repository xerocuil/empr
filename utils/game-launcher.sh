#! /bin/bash

source ~/Applications/Empr/config/empr/settings.sh
console=$1
filename=$2


arcade(){
	retroarch -L ~/.rcores/mame2016_libretro.so $filename
}
cps-2(){
	retroarch -L ~/.rcores/fbalpha2012_cps2_libretro.so $filename
}
dreamcast(){
	retroarch -L ~/.rcores/reicast_libretro.so $filename
}
gamecube(){
	dolphin-emu -b -e $filename
}
genesis(){
	retroarch -L ~/.rcores/picodrive_libretro.so $filename
}
n64(){
	retroarch -L ~/.rcores/mupen64plus_libretro.so $filename
}
nes(){
	retroarch -L ~/.rcores/nestopia_libretro.so $filename
}
neo-geo(){
	retroarch -L ~/.rcores/fbalpha2012_neogeo_libretro.so $filename
}
pc(){
	$APPDIR/launchers/pc/$filename
}
ps1(){
	retroarch -L ~/.rcores/pcsx_rearmed_libretro.so $filename
}
psp (){
	ppsspp $filename
}
saturn(){
	retroarch -L ~/.rcores/mednafen_saturn_libretro.so $filename
}
steam(){
	/usr/games/steam -silent -applaunch "$filename"
}
snes(){
	retroarch -L ~/.rcores/snes9x_libretro.so $filename
}
wii(){
	dolphin-emu -b -e $filename
}
$console $filename
default-monitor
