from receiverHandler import receiverHandler
from videoUploader import videoUploader
from picamera2.encoders import H264Encoder
from picamera2.outputs import CircularOutput
from picamera2 import Picamera2
from datetime import datetime
import time, json, logging, sys

#
# READ CONFIG FILE AND INITIALIZE VARIABLES
#
CONFIG_FILE = open("config.json")
CONFIG = json.loads(CONFIG_FILE.read())
FRAMES_PER_SECOND = float(CONFIG["framesPerSecond"])
MIN_FRAME_DURATION_LIMIT = int(1000000 / FRAMES_PER_SECOND)
MAX_FRAME_DURATION_LIMIT = int(1000000 / FRAMES_PER_SECOND)
VIDEO_LENGTH = float(CONFIG["videoLengthSeconds"])
VIDEO_BITRATE = int(CONFIG["bitrate"])
MAX_DIMENSIONS = (int(CONFIG["maxDimensions"]["width"]), int(CONFIG["maxDimensions"]["height"]))
MIN_DIMENSIONS = (int(CONFIG["minDimensions"]["width"]), int(CONFIG["minDimensions"]["height"]))
ENCODER_CHANNELS = CONFIG["encoderChannels"]
OUT_FOLDER = CONFIG["outFolder"]
FILE_EXTENSION = CONFIG["fileExtension"]
OUTPUT_START_SLEEP_TIME = 10
OUTPUT_STOP_SLEEP_TIME = 2
OUTPUT_RESET_SLEEP_TIME = 30
outfile = None
logging.basicConfig(level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S',
                    format='%(asctime)-15s - [%(levelname)s] %(module)s: %(message)s', )


# Get filename
def getOutfile():
    filename = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    outfile = OUT_FOLDER + filename + FILE_EXTENSION
    return outfile

def exithandler(signal, frame):
    sys.exit(0)

def uploadVideo(outfile):
    uploader = videoUploader() 
    uploader.setVideo(outfile)
    uploader.start()

def main():
    #
    # INITIALIZE CAMERA ENDCODER AND OUTPUT OBJECTS
    #  
    picam2 = Picamera2()
    video_config = picam2.create_video_configuration(main={"size": MAX_DIMENSIONS, "format": ENCODER_CHANNELS}, lores={"size": MIN_DIMENSIONS, "format": "YUV420"}, controls={"NoiseReductionMode": 2, "FrameDurationLimits": (MIN_FRAME_DURATION_LIMIT, MAX_FRAME_DURATION_LIMIT)})
    picam2.configure(video_config)
    encoder = H264Encoder(bitrate=VIDEO_BITRATE)
    output = CircularOutput(buffersize=int(FRAMES_PER_SECOND*VIDEO_LENGTH))
    picam2.start_recording(encoder, output)

    print("Filling camera buffer...")
    time.sleep(OUTPUT_RESET_SLEEP_TIME)

    #
    # INITIALIZE RF RECIEVER
    #
    input = receiverHandler()


    print("Listening for codes on reciever")
    while True:
        

        if input.isTriggered():
            print("Starting output")
            outfile = getOutfile()
            output.fileoutput = outfile
            output.start()
            time.sleep(OUTPUT_START_SLEEP_TIME)
            print("Stopping output")
            output.stop()
            time.sleep(OUTPUT_STOP_SLEEP_TIME)
            uploadVideo(outfile)
            print("Resetting output")
            outfile = ""
            output.fileoutput = None
            time.sleep(OUTPUT_RESET_SLEEP_TIME)
            print("Ready to record again.")
        time.sleep(0.01)

if __name__ == '__main__':
    main()