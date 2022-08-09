# Empr functions

## Organize/Edit CMS photos in digikam
empr.gallery(){
  digikam --config $PHOTODB/photodb.ini --database-directory $PHOTODB
}

## Game launchers
empr.3d0(){
  retroarch -L $CORES/opera_libretro.so "$1"
}
empr.arcade(){
  mame "$1" -skip_gameinfo
}
empr.atari-2600(){
  retroarch -L $CORES/stella_libretro.so "$1"
}
empr.cps-2(){
  retroarch -L $CORES/fbalpha2012_cps2_libretro.so "$1"
}
empr.dreamcast(){
  retroarch -L $CORES/flycast_libretro.so "$1"
}
empr.gamecube(){
  dolphin-emu -b -e "$1"
}
empr.gba(){
  retroarch -L $CORES/mgba_libretro.so "$1"
}
empr.genesis(){
  retroarch -L $CORES/genesis_plus_gx_libretro.so "$1"
}
empr.jaguar(){
  retroarch -L $CORES/virtualjaguar_libretro.so "$1"
}
empr.love(){
  love "$1"
}
empr.n64(){
  retroarch -L $CORES/mupen64plus_next_libretro.so "$1"
}
empr.n64-alt(){
  retroarch -L $CORES/parallel_n64_libretro.so "$1"
}
empr.nes(){
  retroarch -L $CORES/nestopia_libretro.so "$1"
}
empr.neo-geo(){
  mame "$1" -bios unibios40 -skip_gameinfo
}
empr.ngp(){
  retroarch -L $CORES/race_libretro.so "$1"
}
empr.pc(){
  "$1"
}
empr.ps1(){
  retroarch -L $CORES/pcsx_rearmed_libretro.so "$1"
}
empr.ps2(){
  PCSX2 --nogui --fullscreen "$1"
}
empr.psp (){
  retroarch -L $CORES/ppsspp_libretro.so "$1"
}
empr.saturn(){
  retroarch -L $CORES/mednafen_saturn_libretro.so "$1"
}
empr.steam(){
  /usr/games/steam -silent -applaunch "$(cat "$1")"
}
empr.snes(){
  retroarch -L $CORES/snes9x_libretro.so "$1"
}
empr.turbografx-16(){
  retroarch -L $CORES/mednafen_pce_libretro.so "$1"
}
empr.wii(){
  dolphin-emu -b -e "$1"
}
empr.xbox(){
  xemu -full-screen -dvd_path "$1"
}