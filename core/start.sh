#!/bin/bash

services=("highlight-reel.service")

for s in ${services[@]}; do
    echo "Restarting" $s 
    sudo systemctl restart $s
done