#!/bin/bash

sudo mkdir /home/$USER/.sms

pip3 install -q pipenv

pipenv install --ignore-pipfile
pipenv run pyinstaller --onefile --name sms --clean --distpath . --log-level ERROR system_monitoring_system/__main__.py

sudo mv sms /usr/local/bin

sudo rm -rf build
sudo rm sms.spec

sudo cp Montserrat-Bold.ttf Montserrat-Regular.ttf /home/$USER/.sms

echo "Installation Complete"
