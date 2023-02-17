import RPi.GPIO as GPIO
from rpi_rf import RFDevice
import threading, json, time


class receiverHandler(threading.Thread):
    def __init__(self, config):
        self.config = config
        self.RECEIVER_DATA_PIN = config.RECEIVER_GPIO_PIN
        self.rfdevice = RFDevice(self.RECEIVER_DATA_PIN)
        self.file = self.config.WRISTBAND_CONFIG
        self.validCodes = self.readWristbandCodes(self.file)
        self.timestamp = None
        self.recent_triggers = []
        self.queued_triggers = []
        self.TRIGGER_DELAY_TIME = 5

        rfdevice.enable_rx()

    def readWristbandCodes(self, file):
        f = open(file)
        wristbandCodes = json.load(f)
        for i in wristbandCodes:
            print(i)

    def isTriggerExpired(self, trigger, time):
        if trigger[1] + self.TRIGGER_DELAY_TIME < time:
            return True

    def expireRecentTriggers(self):
        time = time.time()

        self.recent_triggers = [x for x in self.recent_triggers if not self.isTriggerExpired(x)]



    def run(self):
        while True:
            time.sleep(0.01)
            self.expireRecentTriggers()



            if self.rfdevice.rx_code_timestamp != self.timestamp:
                code = rfdevice.rx_code
                doIgnore = False

                if code not in self.validCodes:
                    continue

                for i in len(self.recent_triggers):
                    if self.recent_triggers[i][0] == code
                        doIgnore = True
                        break
                if not doIgnore:
                    self.timestamp = self.rfdevice.rx_code_timestamp
                    self.queued_triggers.append(code)
            
            
        return

    def isTriggered(self):
        if len(self.queued_triggers) != 0:
            trigger = self.queued_triggers.pop(0)
            self.recent_triggers.append((trigger, time.time()))
            return True, trigger
        return False, -1