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
This software comes with install and uninstall scripts.
 - Run `install.sh` to install
 - Run `uninstall.sh` to uninstall

## Notice
This software uses ufw, and will screw up your config. Do not use this software is you use ufw for anything else.