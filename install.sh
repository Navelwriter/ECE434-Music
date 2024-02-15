#!/bin/bash
# Check if the user is root
if [ $(id -u) -ne 0 ]; then
    echo "You must be root to run this script"
    exit 1
fi

cp player.service /etc/systemd/system

systemctl daemon-reload

systemctl enable player.service
systemctl start player.service

