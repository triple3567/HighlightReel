import subprocess
import time, threading, os, ffmpeg

#command = f"/usr/bin/cpulimit --limit=100 -- /usr/bin/ffmpeg -y -i /home/pi/HighlightReel/core/out/converted/2023-04-13-18-25-51.mp4 -i /home/pi/HighlightReel/core/res/watermark.png -filter_complex \"overlay \" /home/pi/HighlightReel/core/out/watermarked/output.mp4"
#command = f"/usr/bin/cpulimit --limit=100 -- /usr/bin/ffmpeg"
command = [
    "/usr/bin/cpulimit" ,
    "-f",
    "--limit=200",
    "--",
    "/usr/bin/ffmpeg",
    "-y",
    "-i",
    "/home/pi/HighlightReel/core/out/converted/2023-04-13-18-25-51.mp4",
    "-i",
    "/home/pi/HighlightReel/core/res/watermark.png",
    "-filter_complex",
    "overlay ",
    "/home/pi/HighlightReel/core/out/watermarked/output.mp4"
    ]
p = subprocess.run(command)

print("end")