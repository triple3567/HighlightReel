from rpi_rf import RFDevice
import logging, time

rfdevice = None

logging.basicConfig(level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S',
                    format='%(asctime)-15s - [%(levelname)s] %(module)s: %(message)s', )

rfdevice = RFDevice(27)
rfdevice.enable_rx()
timestamp = None
logging.info("Listening for codes on GPIO 27")


while True:
    if rfdevice.rx_code_timestamp != timestamp:
        timestamp = rfdevice.rx_code_timestamp
        logging.info(str(rfdevice.rx_code) +
                     " [pulselength " + str(rfdevice.rx_pulselength) +
                     ", protocol " + str(rfdevice.rx_proto) + "]")
        timestamp = rfdevice.rx_code_timestamp
        logging.info(rfdevice)
    time.sleep(0.01)
rfdevice.cleanup()