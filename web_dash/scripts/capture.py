import argparse
from picamera2 import Picamera2
from libcamera import Transform

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


parser = argparse.ArgumentParser()
parser.add_argument('zoom')
parser.add_argument('panX')
parser.add_argument('panY')

args = parser.parse_args()

picam2 = Picamera2()

camera_config = picam2.create_still_configuration(main={"size": (1920, 1080)}, lores={"size": (640, 480)}, display="lores")
camera_config["transform"] = Transform(vflip=1, hflip=1)
picam2.configure(camera_config)
picam2 = setZoomAndPan(float(args.zoom), int(args.panX), int(args.panY), picam2)
picam2.start()
picam2.capture_file("/home/pi/HighlightReel/web_dash/res/capture.jpg")


