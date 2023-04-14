#!/bin/bash

services=("highlight-reel.service")

for s in ${services[@]}; do
    echo "Starting" $s 
    sudo systemctl restart $s
done