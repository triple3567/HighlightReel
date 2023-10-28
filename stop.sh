#!/bin/bash

services=("highlight-reel-updater.service" "highlight-reel-wifi-config.service" "highlight-reel-controls.service" "highlight-reel.service")

for s in ${services[@]}; do
    echo "Stopping" $s 
    sudo systemctl stop $s
done