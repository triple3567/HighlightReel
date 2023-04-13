#!/bin/bash

services=("highlight-reel-controls.service")

for s in ${services[@]}; do
    echo "Stopping" $s 
    systemctl stop $s
done