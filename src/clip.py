import sys
import glob
import os
import json
import sqlite3
import cv2

cameraToClip = int(sys.argv[1])
startTimestamp = float(sys.argv[2])
file = open("config.json")
config = json.loads(file.read())
frameFolder = config["cameras"][cameraToClip]["frameFolder"]
outFolder = config["outFolder"]
clipLength = float(config["videoLengthSeconds"])
endTimestamp = startTimestamp + clipLength
databasePath = config["databasePath"]
dbConnection = sqlite3.connect(databasePath)
cursor = dbConnection.cursor()
framesPerSecond = float(config["framesPerSecond"])
width = int(config["dimensions"]["width"])
height = int(config["dimensions"]["height"])

def getFrames(startTimestamp, endTimestamp):
    selectStatement = f"SELECT filename FROM frames WHERE cameraID == {cameraToClip} and timestamp between {startTimestamp} and {endTimestamp};"
    result = cursor.execute(selectStatement)
    return result.fetchall()

def framesToVideo(frames):

    """
    clipName = f"{startTimestamp}.avi" 
    clipPath = outFolder + clipName
    out = cv2.VideoWriter(clipPath, cv2.VideoWriter_fourcc(*'XVID'), framesPerSecond, (width, height))

    i = 0
    for frame in frames:
        img = cv2.imread(frameFolder + frame[0])
        print(i)
        out.write(img)
        i += 1
    out.release()
    """
    clipName = f"test5.avi" 
    clipPath = outFolder + clipName
    out = cv2.VideoWriter(clipPath, 0 , 1, (640, 480))
    print(frameFolder + frames[0][0])
    
    img = cv2.imread(frameFolder + frames[0][0])
    print(img.shape)
    out.write(img)
    img = cv2.imread(frameFolder + frames[1][0])
    out.write(img)
    img = cv2.imread(frameFolder + frames[2][0])
    out.write(img)

    out.release()

def main():
    frames = getFrames(startTimestamp, endTimestamp)
    framesToVideo(frames)


if __name__ == "__main__":
    main()