#!/bin/bash

services=("highlight-reel-updater.service" "highlight-reel-wifi-config.service" "highlight-reel-controls.service" "highlight-reel.service")

for s in ${services[@]}; do
    echo "Starting" $s 
    sudo systemctl restart $s
done