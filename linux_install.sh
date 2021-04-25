#!/bin/bash

sudo true

DIRECTORY=/home/"$USER"/.sms
if [ ! -d "$DIRECTORY" ]; then
    sudo mkdir /home/"$USER"/.sms
fi

pip3 install -q pipenv

pipenv install --ignore-pipfile
pipenv run pyinstaller --onefile --name sms --clean --distpath . --log-level ERROR --hidden-import plyer.platforms.linux.notification system_monitoring_system/__main__.py

sudo mv sms /usr/local/bin

sudo cp Montserrat-Bold.ttf Montserrat-Regular.ttf /home/"$USER"/.sms

FILE=/home/"$USER"/.sms/settings.json
if [ ! -f "$FILE" ]; then
    sudo echo "{\"email\":{},\"limit\":{\"cpu\":75, \"memory\": 50, \"storage\": 60, \"swap\": 80}}" > settings.json
    sudo mv settings.json "$DIRECTORY"
fi

sudo rm -rf build
sudo rm sms.spec

echo "Installation Complete"
