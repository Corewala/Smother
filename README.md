<img width="180" src="https://raw.githubusercontent.com/Corewala/Smother/c4b2f5b87048a58b6f9fa70552a331d8a71ce6f4/smother.svg" />

# Smother
A simple gtk application for managing an OpenVPN killswitch using ufw.

## Build Smother
**Required:**
 - **Build:** `python3`, `nuitka3`, `PyYAML`
 
 - **Runtime:** `gtk3` , `ufw`

```sh
git clone https://github.com/Corewala/Smother.git
cd Smother
sh build.sh
```

## Install or uninstall Smother
Run `install.sh` after building, or run the latest self-extracting archive available [here](https://github.com/Corewala/Smother/releases/latest) to access installation options.

## Notice
This software uses ufw, and will screw up your config. Do not use this software if you use ufw for anything else.

## Credits
"[Mask](https://thenounproject.com/ayub12/collection/jumpicon-pest-control-glyph/?i=2278085)" icon by Ayub Irawan from the [Noun Project](https://thenounproject.com/).