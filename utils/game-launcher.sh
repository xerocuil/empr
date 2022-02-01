#! /bin/bash

CONSOLE=$1
FILE=$2
CORES=$HOME/.config/retroarch/cores

3d0(){
	retroarch -L $CORES/opera_libretro.so "$FILE"
}
arcade(){
	mame "$FILE" -skip_gameinfo
}
atari-2600(){
	retroarch -L $CORES/stella_libretro.so "$FILE"
}
cps-2(){
	retroarch -L $CORES/fbalpha2012_cps2_libretro.so "$FILE"
}
dreamcast(){
	retroarch -L $CORES/flycast_libretro.so "$FILE"
}
gamecube(){
	dolphin-emu -b -e "$FILE"
}
gba(){
	retroarch -L $CORES/mgba_libretro.so "$FILE"
}
gbc(){
	retroarch -L $CORES/sameboy_libretro.so "$FILE"
}
genesis(){
	retroarch -L $CORES/genesis_plus_gx_libretro.so "$FILE"
}
n64(){
	retroarch -L $CORES/parallel64_libretro.so "$FILE"
}
neo-geo(){
	mame "$FILE" -bios unibios40 -skip_gameinfo
}
nes(){
	retroarch -L $CORES/nestopia_libretro.so "$FILE"
}
ngp(){
	retroarch -L $CORES/race_libretro.so "$FILE"
}
pc(){
	"$FILE"
}
ps1(){
	retroarch -L $CORES/pcsx_rearmed_libretro.so "$FILE"
}
ps2(){
	PCSX2 --nogui --fullscreen "$FILE"
}
psp (){
	retroarch -L $CORES/ppsspp_libretro.so "$FILE"
}
saturn(){
	retroarch -L $CORES/mednafen_saturn_libretro.so "$FILE"
}
snes(){
	retroarch -L $CORES/snes9x_libretro.so "$FILE"
}
steam(){
	/usr/games/steam -silent -applaunch "$(cat "$FILE")"
}
turbografx-16(){
	retroarch -L $CORES/mednafen_pce_libretro.so "$FILE"
}
wii(){
	dolphin-emu -b -e "$FILE"
}
xbox(){
	xemu -full-screen -dvd_path "$FILE"
}

$CONSOLE "$FILE"
