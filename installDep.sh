#!/bin/bash
# Check if the user is root
if [ $(id -u) -ne 0 ]; then
    echo "You must be root to run this script"
    exit 1
fi

# check if user has the below packages installed
sudo apt-get install -y alsa-tools alsa-utils python3-mutagen python3-pygame python3-flask-socketio tmux gpiod



