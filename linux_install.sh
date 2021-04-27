#!/bin/bash

sudo true

DIRECTORY=/home/"$USER"/.sms
if [ ! -d "$DIRECTORY" ]; then
    sudo mkdir "$DIRECTORY"
fi

sudo pip3 install -q pipenv

pipenv install --ignore-pipfile
pipenv run pyinstaller --onefile --name sms --clean --distpath . --log-level ERROR --hidden-import plyer.platforms.linux.notification system_monitoring_system/__main__.py

sudo mv sms /usr/local/bin

sudo cp Montserrat-Bold.ttf Montserrat-Regular.ttf sms_icon.png /home/"$USER"/.sms

FILE=/home/"$USER"/.sms/settings.json
if [ ! -f "$FILE" ]; then
    sudo echo "{\"email\":{},\"limit\":{\"cpu\":75, \"memory\": 50, \"storage\": 60, \"swap\": 80}}" > settings.json
    sudo mv settings.json "$DIRECTORY"
fi

sudo rm -rf build
sudo rm sms.spec

echo -e "Do you want to add a desktop icon?[Y/n]: "
read desktop_icon
if [[ "$desktop_icon" == "y" || "$desktop_icon" == "Y" || "$desktop_icon" == "yes" || "$desktop_icon" == "Yes" ]]
then
    echo "#!/usr/bin/env xdg-open
[Desktop Entry]
Version=1.0
Type=Application
Terminal=false
Exec=sms --gui
Name=SMS
Icon=/home/$USER/.sms/sms_icon.png
" > /home/"$USER"/Desktop/SMS.desktop
    sudo chmod +x /home/"$USER"/Desktop/SMS.desktop
    echo -e "Do you want to add a menu icon?[Y/n]: "
    read menu_icon
    if [[ "$menu_icon" == "y" || "$menu_icon" == "Y" || "$menu_icon" == "yes" || "$menu_icon" == "Yes" ]]
    then
        MENU_DIRECTORY=/home/"$USER"/.local/share
        if [ ! -d "$MENU_DIRECTORY" ]; then
            sudo mkdir "$MENU_DIRECTORY"
        fi
        MENU_DIRECTORY=/home/"$USER"/.local/share/applications
        if [ ! -d "$MENU_DIRECTORY" ]; then
            sudo mkdir "$MENU_DIRECTORY"
        fi
        sudo cp /home/"$USER"/Desktop/SMS.desktop "$MENU_DIRECTORY"
    fi
fi

echo "Installation Complete"
