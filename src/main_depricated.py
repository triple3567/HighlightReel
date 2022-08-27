from VideoHandler import VideoHandler
from VideoWriter import VideoWriter
import cv2
import time

def main():
    """
    videoHandler = VideoHandler()
    videoHandler.startAndBlock()

    """
    cameraID = 0
    videoCapturer = cv2.VideoCapture(cameraID)
    startTime = time.time()
    endTime = startTime + 60
    bufferTime = 5
    videoLength = 30
    videoWriter0 = VideoWriter(videoCapturer, videoLength)
    videoWriter1 = None

    currentTime = time.time()
    while currentTime < endTime:
        if videoWriter0 is not None and videoWriter0.isWriting:
            videoWriter0.write(currentTime)
            print("[0] remaining time: " + str(videoWriter0.getRemainingRecordingTime()))
            if videoWriter0.getRemainingRecordingTime() < bufferTime and (videoWriter1 is None or not videoWriter1.isWriting):
                videoWriter1 = VideoWriter(videoCapturer, videoLength)
        if videoWriter1 is not None and videoWriter1.isWriting:
            videoWriter1.write(currentTime)
            print("[1] remaining time: " + str(videoWriter1.getRemainingRecordingTime()))
            if videoWriter1.getRemainingRecordingTime() < bufferTime and (videoWriter0 is None or not videoWriter0.isWriting):
                videoWriter0 = VideoWriter(videoCapturer, videoLength)
        currentTime = time.time()

    videoWriter0.release()
    videoWriter1.release()
    videoCapturer.release()

if __name__=='__main__':
    main()