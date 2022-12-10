from receiverHandler import receiverHandler
from videoUploader import videoUploader
from picamera2.encoders import H264Encoder
from picamera2.outputs import CircularOutput
from configReader import configReader
from picamera2 import Picamera2
from datetime import datetime
import time, json, logging, sys

# Get filename
def getOutfile(outfolder, fileExtension):
    filename = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    outfile = outfolder + filename + fileExtension
    return outfile

def exithandler(signal, frame):
    sys.exit(0)

def uploadVideo(outfile):
    uploader = videoUploader() 
    uploader.setVideo(outfile)
    uploader.start()

def main():
    # READ CONFIG FILE AND INITIALIZE VARIABLES
    config = configReader("config.json")
    config.readConfig()
    outfile = None
    logging.basicConfig(level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S',
                        format='%(asctime)-15s - [%(levelname)s] %(module)s: %(message)s', )

    # INITIALIZE CAMERA ENDCODER AND OUTPUT OBJECTS
    picam2 = Picamera2()
    video_config = picam2.create_video_configuration(main={"size": config.MAX_DIMENSIONS, "format": config.ENCODER_CHANNELS}, lores={"size": config.MIN_DIMENSIONS, "format": "YUV420"}, controls={"NoiseReductionMode": 2, "FrameDurationLimits": (config.MIN_FRAME_DURATION_LIMIT, config.MAX_FRAME_DURATION_LIMIT)})
    picam2.configure(video_config)
    encoder = H264Encoder(bitrate=config.VIDEO_BITRATE)
    output = CircularOutput(buffersize=int(config.FRAMES_PER_SECOND*config.VIDEO_LENGTH))
    picam2.start_recording(encoder, output)
    print("Filling camera buffer...")
    time.sleep(config.OUTPUT_RESET_SLEEP_TIME)

    # INITIALIZE RF RECIEVER
    input = receiverHandler()

    # MAIN LOOP
    print("Listening for codes on reciever")
    while True:
        if input.isTriggered():
            print("Starting output")
            outfile = getOutfile(config.OUT_FOLDER, config.FILE_EXTENSION)
            output.fileoutput = outfile
            output.start()
            time.sleep(config.OUTPUT_START_SLEEP_TIME)
            print("Stopping output")
            output.stop()
            time.sleep(config.OUTPUT_STOP_SLEEP_TIME)
            uploadVideo(outfile)
            print("Resetting output")
            outfile = ""
            output.fileoutput = None
            time.sleep(config.OUTPUT_RESET_SLEEP_TIME)
            print("Ready to record again.")
        time.sleep(0.01)

if __name__ == '__main__':
    main()