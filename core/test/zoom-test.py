from picamera2.encoders import H264Encoder
from picamera2.outputs import CircularOutput
from picamera2 import Picamera2
from libcamera import controls, Transform
from libcamera import Transform, Rectangle
import sys, time

sys.path.insert(0, '/home/pi/HighlightReel/core/src')
from configReader import configReader

config = configReader()
config.readConfig()
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
        "AnalogueGain": config.ANALOGUE_GAIN,
    }
)

video_config["transform"] = Transform(vflip=1, hflip=1)
picam2.configure(video_config)
encoder = H264Encoder(bitrate=config.VIDEO_BITRATE)

x, y = picam2.sensor_resolution
print(x)

picam2.set_controls({"ScalerCrop": (0, 0, 9152, 6944)})
picam2.start_recording(encoder, 'test-control.h264')
time.sleep(5)
picam2.stop_recording()


picam2.set_controls({"ScalerCrop": (2288, 1736, 6864, 5208)})
picam2.start_recording(encoder, 'test-2x.h264')
time.sleep(5)
picam2.stop_recording()

picam2.set_controls({"ScalerCrop": (3432, 2604, 5720, 4340)})
picam2.start_recording(encoder, 'test-4x.h264')
time.sleep(5)
picam2.stop_recording()


