from rpi_rf import RFDevice
import logging, time, json


def readWristbandCodes(file):
    valid_codes = []
    f = open(file)
    wristbandCodes = json.load(f)
    for i in wristbandCodes:
        valid_codes.append(i)
    return valid_codes

wristband_file = "/home/pi/HighlightReel/core/res/wristband_codes.json"
current_wristbands = readWristbandCodes(wristband_file)

rfdevice = None
rfdevice = RFDevice(27)
rfdevice.enable_rx()
timestamp = None

while True:
    if rfdevice.rx_code_timestamp != timestamp:
        if rfdevice.rx_code not in current_wristbands:

            current_wristbands.append(rfdevice.rx_code)
            json_object = json.dumps(current_wristbands)
            with open(wristband_file, "w") as outfile:
                outfile.write(json_object)

            print(rfdevice.rx_code)
            exit()
    time.sleep(0.01)
rfdevice.cleanup()