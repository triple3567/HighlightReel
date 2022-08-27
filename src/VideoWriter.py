import math
import cv2
import time
import copy
import shutil
import os

class VideoWriter(cv2.VideoWriter):

    def __init__(self, videoCapturer, videoLength):
        self.videoCapturer = videoCapturer
        self.startTime = time.time()
        self.outFileFolder = "/home/pi/HighlightReel/videos/"
        self.outFileProcessingFolder = "/home/pi/HighlightReel/videos_being_processed/"
        self.outFileExtension = ".avi"
        self.outFilename = str(math.floor(self.startTime))
        self.outFileRelativePath = self.outFileFolder + self.outFilename + self.outFileExtension
        self.outFileProcessingRelativePath = self.outFileProcessingFolder + self.outFilename + self.outFileExtension
        self.frameRate = 10.0
        self.recordingLengthInSeconds = copy.copy(videoLength)
        self.videoDimensions = (640, 480)
        self.fourCC = cv2.VideoWriter_fourcc(*'XVID')
        self.isWriting = True
        self.endTime = self.startTime + self.recordingLengthInSeconds
        super().__init__(self.outFileProcessingRelativePath, self.fourCC, self.frameRate, self.videoDimensions)

    def setFileName(self):
        self.startTime = time.time()
        self.endTime = self.startTime + self.recordingLengthInSeconds
        self.outFilename = str(math.floor(self.startTime))
        self.outFileRelativePath = self.outFileFolder + self.outFilename + self.outFileExtension
        self.outFileProcessingRelativePath = self.outFileProcessingFolder + self.outFilename + self.outFileExtension
    
    def release(self):            
        super().release()
        self.isWriting = False  
        os.rename(self.outFileProcessingRelativePath, self.outFileRelativePath)

    def write(self, currentTime):
        
        if self.isWriting and currentTime <= self.endTime:
            isFrameCaptured, frame = self.videoCapturer.read()
            super().write(frame)
        elif self.isWriting:
            self.isWriting = False
            self.release()

    def getRemainingRecordingTime(self):
        return self.endTime - time.time()
        
