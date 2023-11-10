#!/bin/bash

BRANCH=$(git branch --show-current)

if [[ "$BRANCH" != "main" ]]; then
    echo "Not on main branch. Skipping auto-updater" 
    exit 0
fi

echo "Waiting for internet connection..."

((count = 30))                           # Maximum number to try.
while [[ $count -ne 0 ]] ; do
    ping -c 1 8.8.8.8                    # Try once.
    rc=$?
    if [[ $rc -eq 0 ]] ; then
        ((count = 1))                    # If okay, flag loop exit.
    else
        sleep 1                          # Minimise network storm.
    fi
    ((count = count - 1))                # So we don't go forever.
done

if [[ $rc -eq 0 ]] ; then                # Make final determination.
    echo "Auto-updater starting..."
else
    echo "No internet connection. Skipping auto-updater."
    exit 0
fi

chmod -R 777 /home/pi/HighlightReel && \
cd /home/pi/HighlightReel && \
git fetch --all && \
git reset --hard origin/main && \
git checkout -f main && \
git pull -f

chown -R highlightreel:highlightreel /home/pi/HighlightReel

# sudo systemctl enable highlight-reel-wifi-config.service
# sudo systemctl enable highlight-reel.service
# sudo systemctl enable highlight-reel-controls.service

echo "Auto-updater success."

exit 0