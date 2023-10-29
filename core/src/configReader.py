import json, os, stat, shutil, logging

class configReader():
    def __init__(self):
        self.filename = "/home/pi/HighlightReel/core/res/config-custom.json"
        if not self.hasCustomConfig():
            self.createCustomConfig()

        self.updateCustomConfig()

    def updateCustomConfig(self):
        default_config = json.loads(open("/home/pi/HighlightReel/core/res/config.json").read())
        custom_config = json.loads(open(self.filename).read())

        for key in default_config:
            if key not in custom_config:
                custom_config.update({key: default_config[key]})

        remove_list = []
        for key in custom_config:
            if key not in default_config:
                remove_list.append(key)
        
        for key in remove_list:
            custom_config.pop(key)

        with open(self.filename, "w") as out:
            json.dump(custom_config, out, indent = 4)


    def createCustomConfig(self):
        shutil.copyfile("/home/pi/HighlightReel/core/res/config.json", "/home/pi/HighlightReel/core/res/config-custom.json")
        os.chmod("/home/pi/HighlightReel/core/res/config-custom.json", stat.S_IRWXG | stat.S_IRWXU | stat.S_IRWXO)

    def hasCustomConfig(self):
        return os.path.isfile("/home/pi/HighlightReel/core/res/config-custom.json")

    def logConfig(self):
        logging.info(f"Config is: {self.CONFIG}")

    def readConfig(self):
        self.CONFIG_FILE = open(self.filename)
        self.CONFIG = json.loads(self.CONFIG_FILE.read())
        self.FRAMES_PER_SECOND = float(self.CONFIG["framesPerSecond"])
        self.MIN_FRAME_DURATION_LIMIT = int(1000000 / self.FRAMES_PER_SECOND)
        self.MAX_FRAME_DURATION_LIMIT = int(1000000 / self.FRAMES_PER_SECOND)
        self.VIDEO_LENGTH = float(self.CONFIG["videoLengthSeconds"])
        self.VIDEO_BITRATE = int(self.CONFIG["bitrate"])
        self.MAX_DIMENSIONS = (int(self.CONFIG["maxDimensions"]["width"]), int(self.CONFIG["maxDimensions"]["height"]))
        self.MIN_DIMENSIONS = (int(self.CONFIG["minDimensions"]["width"]), int(self.CONFIG["minDimensions"]["height"]))
        self.ENCODER_CHANNELS = self.CONFIG["encoderChannels"]
        self.QUEUE_FOLDER = self.CONFIG["queueFolder"]
        self.SENT_FOLDER = self.CONFIG["sentFolder"]
        self.CONVERTED_FOLDER = self.CONFIG["convertedFolder"]
        self.WATERMARKED_FOLDER = self.CONFIG["watermarkedFolder"]
        self.FILE_EXTENSION = self.CONFIG["fileExtension"]
        self.OUTPUT_START_SLEEP_TIME = int(self.CONFIG["outputStartSleepTime"])
        self.OUTPUT_STOP_SLEEP_TIME = int(self.CONFIG["outputStopSleepTime"])
        self.OUTPUT_RESET_SLEEP_TIME = self.VIDEO_LENGTH
        self.RECEIVER_GPIO_PIN = (int(self.CONFIG["recieverGPIO"]))
        self.WRISTBAND_CONFIG = self.CONFIG["wristbandCodesFile"]
        self.POOL_ID = self.CONFIG["poolID"]
        self.WATERMARK = self.CONFIG["watermarkFile"]
        self.THUMBNAILS_FOLDER = self.CONFIG["thumbnailsFolder"]
        self.BRIGHTNESS = float(self.CONFIG["brightness"])
        self.ANALOGUE_GAIN = int(self.CONFIG["analogueGain"])
        self.ZOOM = float(self.CONFIG["zoom"])
        self.PAN_X = int(self.CONFIG["panX"])
        self.PAN_Y = int(self.CONFIG["panY"])