#!/bin/bash
# Check if the user is root
if [ $(id -u) -ne 0 ]; then
    echo "You must be root to run this script"
    exit 1
fi

# check if user has the below packages installed
sudo apt-get install -y alsa-tools alsa-utils
sudo apt-get install -y python3-mutagen
sudo apt-get install -y python3-pygame
sudo apt-get install -y python3-flask-socketio
sudo apt-get install -y gpiod



