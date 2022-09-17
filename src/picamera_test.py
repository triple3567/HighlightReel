from picamera2.encoders import H264Encoder, MJPEGEncoder
from picamera2.outputs import CircularOutput
from picamera2 import Picamera2
import io

import time
import json


file = open("config.json")
config = json.loads(file.read())
framesPerSecond = float(config["framesPerSecond"])
minFrameDurationLimit = int(1000000 / framesPerSecond) - 1
maxFrameDurationLimit = int(1000000 / framesPerSecond) + 1
videoLengthSeconds = float(config["videoLengthSeconds"])
videoBitrate = int(config["bitrate"])
maxDimensions = (int(config["maxDimensions"]["width"]), int(config["maxDimensions"]["height"]))
minDimensions = (int(config["minDimensions"]["width"]), int(config["minDimensions"]["height"]))
encoderChannels = config["encoderChannels"]
outFolder = config["outFolder"]
outfile = outFolder + "newVideo.h264"

picam2 = Picamera2()
video_config = picam2.create_video_configuration(main={"size": maxDimensions, "format": encoderChannels}, lores={"size": minDimensions, "format": "YUV420"}, controls={"NoiseReductionMode": 2, "FrameDurationLimits": (minFrameDurationLimit, maxFrameDurationLimit)})
picam2.configure(video_config)
encoder = H264Encoder(bitrate=videoBitrate, repeat=False)
# encoder = MJPEGEncoder(bitrate=videoBitrate)
output = CircularOutput(buffersize=int(framesPerSecond*videoLengthSeconds), pts="timestamps.txt")
encoder.output = output
picam2.encoder = encoder

#bf = io.BufferedWriter()

def main():
    output.fileoutput = outfile
    picam2.start()
    picam2.start_encoder()
    temp = 0

    time.sleep(10)
    
    output.start()
    time.sleep(10)
    picam2.stop()
    print(output.fileoutput)

if __name__ == '__main__':
    main()