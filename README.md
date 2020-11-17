# Smother
A simple gtk application for managing a VPN killswitch using ufw.

## Build Smother
**Required:** `nuitka3`, `python3`, `gtk3` , `ufw`, `gksu`

```sh
git clone https://github.com/Corewala/Smother.git
cd Smother
sh build.sh
```

## Install or uninstall Smother
Run `install.sh` after building, or run the latest self-extracting archive available [here](https://github.com/Corewala/Smother/releases/latest) to access installation options.

## Notice
This software uses ufw, and will screw up your config. Do not use this software if you use ufw for anything else.