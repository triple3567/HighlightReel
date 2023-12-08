from picamera2 import Picamera2, Preview
from libcamera import controls
import time
picam2 = Picamera2()
camera_config = picam2.create_preview_configuration()
video_config = picam2.create_video_configuration()
video_config['main']['size'] = (1920, 1080)
video_config['controls']['FrameRate'] = 40.0
print(video_config)
picam2.configure(camera_config)
picam2.configure(video_config)
picam2.start()
picam2.set_controls({"AfMode": controls.AfModeEnum.Continuous})
time.sleep(2)
picam2.capture_file("test.jpg")
picam2.start_and_record_video("test.mp4", duration=15)
