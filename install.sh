printf "Please select\n";
printf "1: Install or update Smother\n";
printf "2: Uninstall Smother\n";
printf "> ";

#Repeat only if the user hasn't entered an integer
while ! [[ $selection =~ ^[1-2]+$ ]]; 
do
    read selection;
    #if the entered value was not an integer, show this
    if ! [[ $selection =~ ^[1-2]+$ ]]; then
        sleep 1;
        printf "$(tput setaf 9)Please try again$(tput sgr0)\n";
        printf "1: Install or update Smother\n";
        printf "2: Uninstall Smother\n";
        printf "> ";
    fi
done

case $selection in
    1)
    #Install
	sudo systemctl enable ufw &> /dev/null
	sudo ufw enable &> /dev/null
	mkdir ~/.local/bin &> /dev/null
	mkdir ~/.local/share/applications &> /dev/null
	mkdir ~/.icons &> /dev/null
	cp smother.py ~/.local/bin/smother
	cp Smother.desktop ~/.local/share/applications/Smother.desktop
	cp smother.svg ~/.icons/smother.svg
    ;;

    2)
    #Uninstall
	sudo /usr/bin/ufw --force reset &> /dev/null
	sudo /usr/bin/ufw enable &> /dev/null
	sudo /usr/bin/rm /etc/ufw/*.rules.* &> /dev/null
	sudo /usr/bin/ufw default deny incoming &> /dev/null
	sudo /usr/bin/ufw default allow outgoing &> /dev/null
	rm ~/.local/bin/smother
	rm ~/.local/share/applications/Smother.desktop
	rm /.icons/smother.svg
    ;;
    
    *)
    printf "[$(tput setaf 12 && tput blink)INFO$(tput sgr0)] $(tput setaf 12)Exiting script$(tput sgr0)\n";
    ;;
esac
