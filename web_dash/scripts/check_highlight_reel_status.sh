#!/bin/bash

RESPONSE=$(systemctl status highlight-reel | grep Active)
SUB="running"

if [[ $(systemctl status highlight-reel | grep Active) == *$SUB* ]];
then
    echo "running"
else
    echo "dead"
fi

exit 0