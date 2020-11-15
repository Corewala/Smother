sudo /usr/bin/ufw --force reset &> /dev/null
sudo /usr/bin/ufw enable &> /dev/null
sudo /usr/bin/rm /etc/ufw/*.rules.* &> /dev/null
sudo /usr/bin/ufw default deny incoming &> /dev/null
sudo /usr/bin/ufw default allow outgoing &> /dev/null
rm ~/.local/bin/smother
rm ~/.local/share/applications/Smother.desktop