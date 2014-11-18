#!/bin/bash
user=`whoami`
path="/home/"$user"/qrdp"
mkdir $path
touch /home/$user/.local/share/applications/qrdp.desktop
printf "[Desktop Entry]\nName=qrdp\nComment=qt5 gui for rdesktop\nExec="$path"/qrdp.py\nIcon="$path"/icon.png\nTerminal=false\nType=Application\nEncoding=UTF-8\nCategories=Network;Application;" > /home/$user/.local/share/applications/qrdp.desktop
cp qrdp.py icon.png $path
chmod +x $path/qrdp.py
