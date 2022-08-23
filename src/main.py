import cv2
import time
import math

class VideoWriter(cv2.VideoWriter):

    def __init__(self, videoCapturer):
        self.videoCapturer = videoCapturer
        self.startTime = time.time()
        self.outFileFolder = "../videos/"
        self.outFileExtension = ".avi"
        self.outFilename = str(math.floor(self.startTime))
        self.outFileRelativePath = self.outFileFolder + self.outFilename + self.outFileExtension
        self.frameRate = 10.0
        self.recordingLengthInSeconds = 60.0
        self.videoDimensions = (640, 480)
        self.fourCC = cv2.VideoWriter_fourcc(*'XVID')
        self.isWriting = True
        self.endTime = self.startTime + self.recordingLengthInSeconds
        super().__init__(self.outFileRelativePath, self.fourCC, self.frameRate, self.videoDimensions)

    def setFileName(self):
        self.startTime = time.time()
        self.endTime = self.startTime + self.recordingLengthInSeconds
        self.outFilename = str(math.floor(self.startTime))
        self.outFileRelativePath = self.outFileFolder + self.outFilename + self.outFileExtension
    
    def release(self):
        self.isWriting = False
        super().release()

    def write(self):
        currentTime = time.time()
        
        if self.isWriting and currentTime <= self.endTime:
            isFrameCaptured, frame = self.videoCapturer.read()
            super().write(frame)
        elif self.isWriting and currentTime > self.endTime:
            self.isWriting = False
            self.release()

    def getRemainingRecordingTime(self):
        return self.endTime - time.time()

def main():
    cameraID = 0
    videoCapturer = cv2.VideoCapture(cameraID)
    startTime = time.time()
    endTime = startTime + 600
    bufferTime = 10
    videoWriter0 = VideoWriter(videoCapturer)
    videoWriter1 = None

    while time.time() < endTime:
        if videoWriter0 is not None and videoWriter0.isWriting:
            videoWriter0.write()
            print("[0] remaining time: " + str(videoWriter0.getRemainingRecordingTime()))
            if videoWriter0.getRemainingRecordingTime() < bufferTime and (videoWriter1 is None or not videoWriter1.isWriting):
                videoWriter1 = VideoWriter(videoCapturer)
        if videoWriter1 is not None and videoWriter1.isWriting:
            videoWriter1.write()
            print("[1] remaining time: " + str(videoWriter1.getRemainingRecordingTime()))
            if videoWriter1.getRemainingRecordingTime() < bufferTime and (videoWriter0 is None or not videoWriter0.isWriting):
                videoWriter0 = VideoWriter(videoCapturer)

    videoWriter0.release()
    videoWriter1.release()
    videoCapturer.release()

if __name__=='__main__':
    main()