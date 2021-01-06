if ! command -v ufw &> /dev/null; then
  printf "Please make sure that ufw is properly installed\n"
  exit
fi
printf "Please select\n";
if command -v smother &> /dev/null; then
  printf "1: Update Smother\n"
else
  printf "1: Install Smother\n"
fi
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
        if command -v smother &> /dev/null; then
          printf "1: Update Smother\n"
        else
          printf "1: Install Smother\n"
        fi
        printf "2: Uninstall Smother\n";
        printf "> ";
    fi
done

case $selection in
    1)
    #Install
	sudo systemctl enable ufw &> /dev/null
	sudo ufw enable &> /dev/null
	rm ~/.local/bin/smother &> /dev/null
	rm ~/.local/share/applications/Smother.desktop &> /dev/null
	rm ~/.icons/smother.svg &> /dev/null
	cp smother.py ~/.local/bin/smother &> /dev/null
	cp smother.desktop ~/.local/share/applications/smother.desktop &> /dev/null
	cp smother.svg ~/.icons/smother.svg &> /dev/null
	if command -v smother &> /dev/null; then
	  printf "Successfully installed Smother\n"
	elif test -f ~/.local/bin/smother; then
	  printf "Successfully installed Smother\nPlease make sure that ~/.local/bin is in your PATH\n"
	else
	  printf "Smother was not installed\n"
	fi
    ;;

    2)
    #Uninstall
	sudo /usr/bin/ufw --force reset &> /dev/null
	sudo /usr/bin/ufw enable &> /dev/null
	sudo /usr/bin/rm /etc/ufw/*.rules.* &> /dev/null
	sudo /usr/bin/ufw default deny incoming &> /dev/null
	sudo /usr/bin/ufw default allow outgoing &> /dev/null
	rm ~/.local/bin/smother &> /dev/null
	rm ~/.local/share/applications/smother.desktop &> /dev/null
	rm ~/.icons/smother.svg &> /dev/null
	if ! test -f ~/.local/bin/smother; then
	  printf "Successfully uninstalled Smother\n"
	else
	  printf "Smother was not uninstalled\n"
	fi
    ;;

    *)
    ;;
esac