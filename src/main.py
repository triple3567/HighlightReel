import cv2
import time
import queue
import os
import json
import glob

file = open("config.json")
config = json.loads(file.read())

cameraID = int(config["cameraIDs"][0])
framesPerSecond = float(config["framesPerSecond"])
videoLengthSeconds = float(config["videoLengthSeconds"])
framesPerVideo = framesPerSecond * videoLengthSeconds
videoCapturer = cv2.VideoCapture(cameraID)
videoCapturer.set(cv2.CAP_PROP_FRAME_WIDTH, float(config["dimensions"]["width"]))
videoCapturer.set(cv2.CAP_PROP_FRAME_HEIGHT, float(config["dimensions"]["height"]))
videoCapturer.set(cv2.CAP_PROP_FPS, framesPerSecond)
folderPath = config["frameFolder"]
archivePath = config["archiveFolder"]
maxVideosStored = int(config["maxVideosStored"])
frameQueue = queue.Queue(maxsize=framesPerVideo * maxVideosStored)

def getFrameName():
    return str(time.time()) + ".jpeg"

def recordFrame():
    ret, frame = videoCapturer.read()
    frameName = getFrameName()
    framePath = folderPath + frameName
    cv2.imwrite(framePath, frame)
    frameQueue.put(frameName)

def moveOldestFrame():
    if frameQueue.full():
        fileToMove = frameQueue.get()
        os.rename(folderPath + fileToMove, archivePath + fileToMove)
        print("moved: " + fileToMove)
    else:
        return

def deleteOldestFrame():
    if frameQueue.full():
        fileToMove = frameQueue.get()
        os.remove(folderPath + fileToMove)
        print("deleted: " + fileToMove)
    else:
        return

def clearDatabase():
    videoFiles = glob.glob(folderPath + "*")
    archiveFiles = glob.glob(archivePath + "*")
    for f in videoFiles:
        os.remove(f)
    for f in archiveFiles:
        os.remove(f)

def main():
    previousFrameTime = -1
    clearDatabase()

    print(frameQueue.maxsize)
    while True:
        timeElapesd = time.time() - previousFrameTime
        if timeElapesd > 1.0 / framesPerSecond:
            previousFrameTime = time.time()
            deleteOldestFrame()
            recordFrame()

if __name__ == "__main__":
    main()