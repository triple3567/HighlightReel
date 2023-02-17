from receiverHandler import receiverHandler
from videoUploader import videoUploader
from videoWriter import videoWriter
from configReader import configReader
from picamera2.encoders import H264Encoder
from picamera2.outputs import CircularOutput
from picamera2 import Picamera2
from datetime import datetime
from libcamera import controls
from systemd.journal import JournalHandler
import time, json, logging, sys, argparse, copy

# Get filename
def getOutfile(outfolder, fileExtension):
    filename = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    outfile = outfolder + filename + fileExtension
    return outfile

def uploadVideo(outfile, config):
    uploader = videoUploader(config) 
    uploader.setVideo(outfile)
    uploader.start()

def configurePicam(config):
    picam2 = Picamera2()
    video_config = picam2.create_video_configuration(
        main={
            "size": config.MAX_DIMENSIONS, 
            "format": config.ENCODER_CHANNELS
        }, 
        lores={
            "size": config.MIN_DIMENSIONS, 
            "format": "YUV420"
        },
        controls={
            "NoiseReductionMode": 2, 
            "FrameDurationLimits": (
                config.MIN_FRAME_DURATION_LIMIT, 
                config.MAX_FRAME_DURATION_LIMIT
            ),
            "AfMode": controls.AfModeEnum.Continuous,
            "AwbEnable": True,
            "AwbMode": controls.AwbModeEnum.Indoor,
            "AeEnable": True,
            "AeConstraintMode": controls.AeConstraintModeEnum.Normal,
            "AeExposureMode": controls.AeExposureModeEnum.Normal,
            "Brightness": 0.0,
            "AnalogueGain": 10
        }
    )
    picam2.configure(video_config)
    encoder = H264Encoder(bitrate=config.VIDEO_BITRATE)
    output = CircularOutput(
        buffersize=int(config.FRAMES_PER_SECOND*config.VIDEO_LENGTH)
    )
    picam2.start_recording(encoder, output)
    print("Filling camera buffer...")

    return picam2, output

def parseArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument("--supress_upload", help="supresses video upload to the api", action="store_true")
    args = parser.parse_args()
    return args


def main():
    logger = logging.getLogger(__name__)
    logger.addHandler(JournalHandler())
    logger.setLevel(logging.INFO)

    #Parse arguments
    args = parseArgs()

    # READ CONFIG FILE AND INITIALIZE VARIABLES
    config = configReader("/home/pi/HighlightReel/core/config.json")
    config.readConfig()

    outfile = None
    logging.basicConfig(level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S',
                        format='%(asctime)-15s - [%(levelname)s] %(module)s: %(message)s', )

    # INITIALIZE CAMERA ENDCODER AND OUTPUT OBJECTS
    picam2, output = configurePicam(config)
    time.sleep(config.OUTPUT_RESET_SLEEP_TIME)

    # INITIALIZE RF RECIEVER
    input = receiverHandler(config)

    # MAIN LOOP
    print("Listening for codes on reciever")
    sys.stdout.flush()
    while True:

        isInput, triggeredBy = input.isTriggered()
        if isInput:
            output_copy = copy.copy(output)
            output_copy._circular = output._circular.copy()
            writer = videoWriter(config, output_copy, args.supress_upload, triggeredBy)
            writer.start()

            time.sleep(2) #temporary delay between records until multi transmitter support is implimented.
        time.sleep(0.01)

if __name__ == '__main__':
    main()