#!/bin/bash

BRANCH=$(git branch --show-current)

if [[ "$BRANCH" != "main" ]]; then
    echo "Not on main branch. Skipping auto-updater" 
    exit 0
fi

echo "Auto-updater starting..."

cd /home/pi/HighlightReel && \
git reset --hard origin/main && \
git checkout -f main && \
git pull -f

sudo systemctl enable highlight-reel-wifi-config.service
sudo systemctl enable highlight-reel.service
sudo systemctl enable highlight-reel-controls.service

echo "Auto-updater success."

exit 0