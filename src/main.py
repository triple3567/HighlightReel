import cv2
import time
import queue
import os
import json
import glob
import sys
import sqlite3

cameraID = int(sys.argv[1])
file = open("config.json")
config = json.loads(file.read())

deviceID = int(config["cameras"][cameraID]["deviceID"])
framesPerSecond = float(config["framesPerSecond"])
videoLengthSeconds = float(config["videoLengthSeconds"])
framesPerVideo = framesPerSecond * videoLengthSeconds
videoCapturer = cv2.VideoCapture(deviceID,cv2.CAP_V4L)
videoCapturer.set(cv2.CAP_PROP_FRAME_WIDTH, float(config["dimensions"]["width"]))
#videoCapturer.set(cv2.CAP_PROP_FRAME_HEIGHT, float(config["dimensions"]["height"]))
#videoCapturer.set(cv2.CAP_PROP_FPS, framesPerSecond)

print(videoCapturer.get(cv2.CAP_PROP_FRAME_WIDTH))

folderPath = config["cameras"][cameraID]["frameFolder"]
archivePath = config["cameras"][cameraID]["archiveFolder"]
maxVideosStored = int(config["maxVideosStored"])
frameQueue = queue.Queue(maxsize=framesPerVideo * maxVideosStored)
databasePath = config["databasePath"]
dbConnection = sqlite3.connect(databasePath)
cursor = dbConnection.cursor()

def insertFrameInDB(frameName, timestamp):
    insertStatement = f"INSERT INTO frames VALUES (\"{frameName}\", {timestamp}, {cameraID});"
    #print(insertStatement)
    cursor.execute(insertStatement)
    dbConnection.commit()


def makeDatabase():
    cursor.execute("CREATE TABLE IF NOT EXISTS frames(filename TEXT, timestamp REAL, cameraID INT);")
    dbConnection.commit()

def makeFoldersIfNotExist():
    isFolderExist = os.path.exists(folderPath)
    isArchiveExist = os.path.exists(archivePath)

    if not isFolderExist:
        os.makedirs(folderPath)

    if not isArchiveExist:
        os.makedirs(archivePath)

def getFrameName():
    timestamp = time.time()
    return timestamp, str(timestamp) + ".jpeg"

def recordFrame():
    ret, frame = videoCapturer.read()
    timestamp, frameName = getFrameName()
    framePath = folderPath + frameName
    cv2.imwrite(framePath, frame)
    frameQueue.put(frameName)
    insertFrameInDB(frameName, timestamp)

def moveOldestFrame():
    if frameQueue.full():
        fileToMove = frameQueue.get()
        os.rename(folderPath + fileToMove, archivePath + fileToMove)
        #print("moved: " + fileToMove)
    else:
        return

def deleteOldestFrame():
    if frameQueue.full():
        fileToMove = frameQueue.get()
        os.remove(folderPath + fileToMove)
        #print("deleted: " + fileToMove)
    else:
        return

def clearDatabaseAndFrames():
    videoFiles = glob.glob(folderPath + "*")
    archiveFiles = glob.glob(archivePath + "*")
    for f in videoFiles:
        os.remove(f)
    for f in archiveFiles:
        os.remove(f)

def main():
    makeFoldersIfNotExist()
    makeDatabase()
    clearDatabaseAndFrames()
    previousFrameTime = -1

    while True:
        timeElapesd = time.time() - previousFrameTime
        if timeElapesd > 1.0 / framesPerSecond:
            previousFrameTime = time.time()
            deleteOldestFrame()
            recordFrame()

if __name__ == "__main__":
    main()