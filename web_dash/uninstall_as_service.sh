#!/bin/bash

if [[ $(/usr/bin/id -u) -ne 0 ]]; then
    echo "Please run as root"
    exit
fi

DIR="/home/pi/HighlightReel/web_dash/services"
services=("highlight-reel-controls.service")

for s in ${services[@]}; do
    echo "Stopping" $s 
    systemctl stop $s
done

echo "Reloading Daemon"
systemctl daemon-reload

for s in ${services[@]}; do
    FILE="/etc/systemd/system/$s"

    echo "Disabling" $s
    systemctl disable $s

    echo "Removing" $FILE "from /etc/systemd/system"
    sudo rm $FILE 
done
