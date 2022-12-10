import json

class configReader():
    def __init__(self, file):
        self.filename = file

    def readConfig(self):
        self.CONFIG_FILE = open("config.json")
        self.CONFIG = json.loads(self.CONFIG_FILE.read())
        self.FRAMES_PER_SECOND = float(self.CONFIG["framesPerSecond"])
        self.MIN_FRAME_DURATION_LIMIT = int(1000000 / self.FRAMES_PER_SECOND)
        self.MAX_FRAME_DURATION_LIMIT = int(1000000 / self.FRAMES_PER_SECOND)
        self.VIDEO_LENGTH = float(self.CONFIG["videoLengthSeconds"])
        self.VIDEO_BITRATE = int(self.CONFIG["bitrate"])
        self.MAX_DIMENSIONS = (int(self.CONFIG["maxDimensions"]["width"]), int(self.CONFIG["maxDimensions"]["height"]))
        self.MIN_DIMENSIONS = (int(self.CONFIG["minDimensions"]["width"]), int(self.CONFIG["minDimensions"]["height"]))
        self.ENCODER_CHANNELS = self.CONFIG["encoderChannels"]
        self.OUT_FOLDER = self.CONFIG["outFolder"]
        self.FILE_EXTENSION = self.CONFIG["fileExtension"]
        self.OUTPUT_START_SLEEP_TIME = 10
        self.OUTPUT_STOP_SLEEP_TIME = 2
        self.OUTPUT_RESET_SLEEP_TIME = 30