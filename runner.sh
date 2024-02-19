#!/bin/bash
# Check if the user is root
if [ $(id -u) -ne 0 ]; then
    echo "You must be root to run this script"
    exit 1
fi

sleep 10
config-pin P8_11 eqep
config-pin P8_12 eqep
export DISPLAY=:0
cd /home/debian/ECE434-Music
chmod +x eqep.sh
./eqep.sh
python3 player.py
