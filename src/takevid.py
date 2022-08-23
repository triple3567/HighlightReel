import cv2
import time
import math

def main():
    startTime = time.time()
    cameraID = 0
    videoCapturer = cv2.VideoCapture(cameraID)
    fourCC = cv2.VideoWriter_fourcc(*'XVID')
    outFileExtension = "avi"
    outFilename = str(math.floor(startTime)) + "." + outFileExtension
    frameRate = 10.0
    videoDimensions = (640,480)
    videoWriter = cv2.VideoWriter("../videos/" + outFilename, fourCC, frameRate, videoDimensions)
    
    #videoWriter2 = cv2.VideoWriter("../videos/2-" + outFilename, fourCC, frameRate, videoDimensions)

    recordingLength = 15
    endTime = startTime + recordingLength

    while videoCapturer.isOpened():
        isFrameCaptured, frame = videoCapturer.read()

        if isFrameCaptured:
            videoWriter.write(frame)
            #videoWriter2.write(frame)
    
        currentTime = time.time()
        if endTime < currentTime:
            break
    
    videoCapturer.release()
    videoWriter.release()
    #videoWriter2.release()



if __name__=='__main__':
    main()