#!/bin/bash
user=`whoami`
path="/home/"$user"/qrdp"
mkdir $path
touch /home/$user/.local/share/applications/qrdp.desktop
printf "[Desktop Entry]\nVersion=1.0\nName=qrdp\nComment=qt5 gui for rdesktop\nExec="$path"/qrdp.py\nIcon="$path"/icon.png\nPath=/h    ome/qtheya/.qrdp/\nTerminal=false\nType=Application\nEncoding=UTF-8\nCategories=Utility;Network;Application;" > /home/$user/.local/    share/applications/qrdp.desktop
cp qrdp.py icon.png $path
chmod +x $path/qrdp.py
