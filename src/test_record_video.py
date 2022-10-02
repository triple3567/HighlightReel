from picamera2.encoders import H264Encoder
from picamera2.outputs import CircularOutput
from picamera2 import Picamera2
from datetime import datetime
import time
import json

#
# READ CONFIG FILE AND INITIALIZE VARIABLES
#
file = open("config.json")
config = json.loads(file.read())
framesPerSecond = float(config["framesPerSecond"])
minFrameDurationLimit = int(1000000 / framesPerSecond)
maxFrameDurationLimit = int(1000000 / framesPerSecond)
videoLengthSeconds = float(config["videoLengthSeconds"])
videoBitrate = int(config["bitrate"])
maxDimensions = (int(config["maxDimensions"]["width"]), int(config["maxDimensions"]["height"]))
minDimensions = (int(config["minDimensions"]["width"]), int(config["minDimensions"]["height"]))
encoderChannels = config["encoderChannels"]
outFolder = config["outFolder"]
filename = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
fileExtension = config["fileExtension"]
outfile = outFolder + filename + fileExtension
TEMP_SLEEP_TIME = 10

#
# INITIALIZE CAMERA ENDCODER AND OUTPUT OBJECTS
#
picam2 = Picamera2()
video_config = picam2.create_video_configuration(main={"size": maxDimensions, "format": encoderChannels}, lores={"size": minDimensions, "format": "YUV420"}, controls={"NoiseReductionMode": 2, "FrameDurationLimits": (minFrameDurationLimit, maxFrameDurationLimit)})
picam2.configure(video_config)
encoder = H264Encoder(bitrate=videoBitrate, repeat=False)
output = CircularOutput(buffersize=int(framesPerSecond*videoLengthSeconds), pts="timestamps.txt")
encoder.output = output
picam2.encoder = encoder

def main():
    
    picam2.start()
    picam2.start_encoder()
    time.sleep(TEMP_SLEEP_TIME)

    output.fileoutput = outfile
    output.start()
    time.sleep(TEMP_SLEEP_TIME)
    picam2.stop()
    print(output.fileoutput)

if __name__ == '__main__':
    main()