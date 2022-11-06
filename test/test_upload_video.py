import requests

with open('/home/pi/HighlightReel/out/2022-10-30-19-42-33.h264', 'rb') as f:
    r = requests.post('https://highlight-reel-core.herokuapp.com/api/upload', files={'2022-10-30-19-42-33.h264': f})