#! /bin/bash

console=$1
filename=$2
CORES=$HOME/.config/retroarch/cores

3d0(){
	retroarch -L $CORES/opera_libretro.so "$filename"
}
arcade(){
	mame "$filename" -skip_gameinfo
}
atari-2600(){
	retroarch -L $CORES/stella_libretro.so "$filename"
}
cps-2(){
	retroarch -L $CORES/fbalpha2012_cps2_libretro.so "$filename"
}
dreamcast(){
	retroarch -L $CORES/flycast_libretro.so "$filename"
}
gamecube(){
	dolphin-emu -b -e "$filename"
}
gba(){
	retroarch -L $CORES/mgba_libretro.so "$filename"
}
genesis(){
	retroarch -L $CORES/genesis_plus_gx_libretro.so "$filename"
}
n64(){
	retroarch -L $CORES/mupen64plus_next_libretro.so "$filename"
}
n64-alt(){
	retroarch -L $CORES/parallel_n64_libretro.so "$filename"
}
nes(){
	retroarch -L $CORES/nestopia_libretro.so "$filename"
}
neo-geo(){
	mame "$filename" -bios unibios40 -skip_gameinfo
}
ngp(){
	retroarch -L $CORES/race_libretro.so "$filename"
}
pc(){
	"$filename"
}
ps1(){
	retroarch -L $CORES/pcsx_rearmed_libretro.so "$filename"
}
ps2(){
	PCSX2 --nogui --fullscreen "$filename"
}
psp (){
	retroarch -L $CORES/ppsspp_libretro.so "$filename"
}
saturn(){
	retroarch -L $CORES/mednafen_saturn_libretro.so "$filename"
}
steam(){
	/usr/games/steam -silent -applaunch "$(cat "$filename")"
}
snes(){
	retroarch -L $CORES/snes9x_libretro.so "$filename"
}
turbografx-16(){
	retroarch -L $CORES/mednafen_pce_libretro.so "$filename"
}
wii(){
	dolphin-emu -b -e "$filename"
}
xbox(){
	xemu -full-screen -dvd_path "$filename"
}

$console "$filename"
default-monitor
