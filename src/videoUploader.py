import threading
import requests
import os

class videoUploader(threading.Thread):
    def __init__(self):
        # calling parent class constructor
        threading.Thread.__init__(self)
        self.videoPath = ""
        self.videoName = ""
        self.httpPostRequestUri = "https://highlight-reel-core.herokuapp.com/api/upload"

    def setVideo(self, outfile):
        self.videoPath = outfile
        self.videoName = os.path.basename(outfile)
    
    def run(self):
        with open(self.videoPath, 'rb') as f:
            r = requests.post(self.httpPostRequestUri, files={self.videoName: f})