from picamera2.encoders import H264Encoder
from picamera2.outputs import CircularOutput
from picamera2 import Picamera2
import time

#
# INITIALIZE CAMERA ENDCODER AND OUTPUT OBJECTS
#
picam2 = Picamera2()
video_config = picam2.create_video_configuration(main={"size": (1920,1080), "format": "RGB888"}, lores={"size": (640,480), "format": "YUV420"}, controls={"NoiseReductionMode": 2, "FrameDurationLimits": (33333, 33333)})
picam2.configure(video_config)
encoder = H264Encoder(bitrate=10000000)
output = CircularOutput(buffersize=int(150), pts="timestamps.txt")


picam2.start_recording(encoder, output)
time.sleep(10)

output.fileoutput = "/home/pi/HighlightReel/out/recording.h264"
output.start()
time.sleep(10)
output.stop()