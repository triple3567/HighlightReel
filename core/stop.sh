#!/bin/bash

services=("highlight-reel.service")

for s in ${services[@]}; do
    echo "Stopping" $s 
    sudo systemctl stop $s
done