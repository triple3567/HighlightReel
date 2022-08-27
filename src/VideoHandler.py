import cv2
import time
from VideoWriter import VideoWriter

class VideoHandler:
    def __init__(self):
        self.startTime = -1
        self.endTime = -1
        self.cameraID = 0
        self.bufferTime = 5
        self.videoLength = 60
        self.recordingLength = 600
        self.videoCapturer = cv2.VideoCapture(self.cameraID)
        self.videoWriter0 = VideoWriter(self.videoCapturer, self.videoLength)
        self.videoWriter1 = None

    def startAndBlock(self):
        self.startTime = time.time()
        self.endTime = self.startTime + self.recordingLength
        currentTime = time.time()
        while currentTime < self.endTime:

            if self.videoWriter0 is not None and self.videoWriter0.isWriting:
                self.videoWriter0.write(currentTime)
                print("[0] remaining time: " + str(self.videoWriter0.getRemainingRecordingTime()))
                if self.videoWriter0.getRemainingRecordingTime() < self.bufferTime and (self.videoWriter1 is None or not self.videoWriter1.isWriting):
                    videoWriter1 = VideoWriter(self.videoCapturer, self.videoLength)
            if self.videoWriter1 is not None and self.videoWriter1.isWriting:
                self.videoWriter1.write(currentTime)
                print("[1] remaining time: " + str(self.videoWriter1.getRemainingRecordingTime()))
                if self.videoWriter1.getRemainingRecordingTime() < self.bufferTime and (self.videoWriter0 is None or not self.videoWriter0.isWriting):
                    self.videoWriter0 = VideoWriter(self.videoCapturer, self.videoLength)
            
            currentTime = time.time()

        self.videoWriter0.release()
        self.videoWriter1.release()
        self.videoCapturer.release()

        