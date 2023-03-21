#!/bin/bash

rm -f /home/pi/HighlightReel/web_dash/res/capture.jpg

libcamera-still \
-o /home/pi/HighlightReel/web_dash/res/capture.jpg \
--width 1920 \
--height 1080 \
--autofocus-on-capture