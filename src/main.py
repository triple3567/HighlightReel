from picamera2.encoders import H264Encoder
from picamera2.outputs import CircularOutput
from picamera2 import Picamera2
from datetime import datetime
from rpi_rf import RFDevice
import time
import json
import logging
import signal
import sys

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
TEMP_SLEEP_TIME = 2
RX_GPIO_PIN = int(CONFIG["recieverGPIO"])
outfile = None
rfdevice = RFDevice(RX_GPIO_PIN)
logging.basicConfig(level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S',
                    format='%(asctime)-15s - [%(levelname)s] %(module)s: %(message)s', )


# Get filename
def getOutfile():
    filename = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    outfile = OUT_FOLDER + filename + FILE_EXTENSION
    return outfile

def exithandler(signal, frame):
    rfdevice.cleanup()
    sys.exit(0)


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
    time.sleep(10)

    #
    # INITIALIZE RF RECIEVER
    #
    rfdevice.enable_rx()
    transmission_timestamp = None


    print("Listening for codes on reciever")
    while True:
        

        if rfdevice.rx_code_timestamp != transmission_timestamp and int(rfdevice.rx_code) == 123:
            transmission_timestamp = rfdevice.rx_code_timestamp
            logging.info(str(rfdevice.rx_code) +
                        " [pulselength " + str(rfdevice.rx_pulselength) +
                        ", protocol " + str(rfdevice.rx_proto) + "]")
            print("Starting output")
            output.fileoutput = getOutfile()
            output.start()
            time.sleep(TEMP_SLEEP_TIME)
            print("Stopping output")
            output.stop()
            time.sleep(TEMP_SLEEP_TIME)
            print("Resetting output")
            output.fileoutput = None
            time.sleep(TEMP_SLEEP_TIME)
            print("HERE2")
        elif rfdevice.rx_code_timestamp != transmission_timestamp and int(rfdevice.rx_code) == 321:
            sys.exit(0)
        time.sleep(0.01)

if __name__ == '__main__':
    main()