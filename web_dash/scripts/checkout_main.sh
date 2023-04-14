#!/bin/bash
cd /home/pi/HighlightReel && \
git reset --hard origin/main && \
git checkout -f main && \
git pull -f