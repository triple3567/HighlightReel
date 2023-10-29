from receiverHandler import receiverHandler
from videoUploader import videoUploader
from videoWriter import videoWriter
from logUploader import logUploader
from outputQueueHandler import outputQueueHandler
from configReader import configReader
from picamera2.encoders import H264Encoder
from picamera2.outputs import CircularOutput
from picamera2 import Picamera2
from datetime import datetime
from libcamera import controls, Transform
from libcamera import Transform
import time, json, logging, sys, argparse, copy, logging

# Get filename
def getOutfile(outfolder, fileExtension):
    filename = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    outfile = outfolder + filename + fileExtension
    return outfile

def uploadVideo(outfile, config):
    uploader = videoUploader(config) 
    uploader.setVideo(outfile)
    uploader.start()

def setZoomAndPan(zoom, panX, panY, picam2):
    if zoom == 0:
        return picam2

    sensor_resolution_x, sensor_resolution_y = picam2.sensor_resolution
    offset_x = (sensor_resolution_x - (sensor_resolution_x / zoom)) / 2
    offset_y = (sensor_resolution_y - (sensor_resolution_y / zoom)) / 2
    capture_resolution_x = sensor_resolution_x - offset_x
    capture_resolution_y = sensor_resolution_y - offset_y
    
    offset_x_segments = offset_x / 10
    offset_y_segments = offset_y / 10

    if panX < -10:
        panX = -10
    if panX > 10:
        panX = 10
    if panY < -10:
        panY = -10
    if panY > 10:
        panY = 10

    pan_offset_x = offset_x_segments * panX
    pan_offset_y = offset_y_segments * panY

    x_start = int(offset_x + pan_offset_x)
    y_start = int(offset_y + pan_offset_y)
    x_end = int(capture_resolution_x + pan_offset_x)
    y_end = int(capture_resolution_y + pan_offset_y)

    print(f"{x_start}, {y_start}, {x_end}, {y_end}")

    if x_start < 0:
        x_start = 0
    if y_start < 0:
        y_start = 0
    if x_end > sensor_resolution_x:
        x_end = sensor_resolution_x
    if y_end > sensor_resolution_y:
        y_end = sensor_resolution_y


    picam2.set_controls({"ScalerCrop": (x_start, y_start, x_end, y_end)})

    return picam2

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
            "Brightness": config.BRIGHTNESS,
            "AnalogueGain": config.ANALOGUE_GAIN
        }
    )
    video_config["transform"] = Transform(vflip=1, hflip=1)
    picam2.configure(video_config)
    picam2 = setZoomAndPan(config.ZOOM, config.PAN_X, config.PAN_Y, picam2)

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

def getHardwareID():
        # Extract serial from cpuinfo file
        cpuserial = "0000000000000000"
        try:
            f = open('/proc/cpuinfo','r')
            for line in f:
                if line[0:6]=='Serial':
                    cpuserial = line[10:26]
            f.close()
        except:
            cpuserial = "ERROR000000000"
    
        return cpuserial

def configureLogger():
    logging.Formatter.converter = time.gmtime
    now = time.strftime("%y-%m-%d_%H:%M:%S", time.gmtime())
    logging.basicConfig(format='%(levelname)s - %(asctime)s - %(message)s', 
                        level=logging.DEBUG,
                        filename=f"/home/pi/HighlightReel/core/out/logs/{getHardwareID()}_{now}UTC.log",
                        filemode="a+"
                        )


def main():

    #Parse arguments
    args = parseArgs()

    # READ CONFIG FILE AND INITIALIZE VARIABLES
    config = configReader()
    config.readConfig()

    #Initialize Logging
    lg = logUploader(config)
    configureLogger()
    logging.info("Starting Highlight Reel...")
    lg.start()

    # INITIALIZE CAMERA ENDCODER AND OUTPUT OBJECTS
    picam2, output = configurePicam(config)
    time.sleep(config.OUTPUT_RESET_SLEEP_TIME)

    # INITIALIZE OUTPUT QUEUE
    outputHandler = outputQueueHandler(config, args.supress_upload)
    outputHandler.start()

    # INITIALIZE RF RECIEVER
    input = receiverHandler(config)
    input.start()

    # MAIN LOOP
    logging.info("Listening for codes on reciever")
    sys.stdout.flush()
    while True:

        isInput, triggeredBy = input.isTriggered()
        if isInput:
            logging.info(f"Clip requested by {triggeredBy}")
            output_copy = copy.copy(output)
            output_copy._circular = output._circular.copy()
            outputHandler.push(output_copy, triggeredBy)

        time.sleep(0.01)

if __name__ == '__main__':
    main()
