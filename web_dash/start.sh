#!/bin/bash

services=("highlight-reel-controls.service")

for s in ${services[@]}; do
    echo "Starting" $s 
    systemctl restart $s
done