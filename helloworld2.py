import numpy as np
import os
import cv2
import time

# Standard Video Dimensions Sizes
STD_DIMENSIONS =  {
    "480p": (640, 480),
    "720p": (1280, 720),
    "1080p": (1920, 1080),
    "4k": (3840, 2160),
}

# Video Encoding, might require additional installs
# Types of Codes: http://www.fourcc.org/codecs.php
VIDEO_TYPE = {
    'avi': cv2.VideoWriter_fourcc(*'XVID'),
    #'mp4': cv2.VideoWriter_fourcc(*'H264'),
    'mp4': cv2.VideoWriter_fourcc(*'XVID'),
    'mjepg': cv2.VideoWriter_fourcc(*'mjpg'),
}

# Set resolution for the video capture
# Function adapted from https://kirr.co/0l6qmh
def change_res(cap, width, height):
    cap.set(3, width)
    cap.set(4, height)

# grab resolution dimensions and set video capture to it.
def get_dims(cap, res='1080p'):
    width, height = STD_DIMENSIONS["480p"]
    if res in STD_DIMENSIONS:
        width,height = STD_DIMENSIONS[res]
    ## change the current caputre device
    ## to the resulting resolution
    change_res(cap, width, height)
    return width, height

def get_video_type(filename):
    filename, ext = os.path.splitext(filename)
    if ext in VIDEO_TYPE:
      return  VIDEO_TYPE[ext]
    return VIDEO_TYPE['avi']

def main():
    filename = 'video.mjepg'
    frames_per_second = 24.0
    res = '720p'

    cap = cv2.VideoCapture(0)
    out = cv2.VideoWriter(filename, get_video_type(filename), 25, get_dims(cap, res))

    start_time = time.time()

    while True:
        ret, frame = cap.read()
        out.write(frame)
        if start_time + 5 <= time.time():
            break
        

    cap.release()
    out.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()