mkdir build
nuitka3 ./smother.py -o build/smother &> /dev/null
echo '[Desktop Entry]
Type=Application
Name=Smother
Exec=smother
Terminal=false
Icon=smother
Categories=GNOME;Network;
StartupNotify=false' > build/Smother.desktop
