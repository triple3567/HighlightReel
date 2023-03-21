import json, threading, requests, os, ffmpeg, pprint, time
from subprocess import call 

class videoUploader(threading.Thread):
    def __init__(self, config, supress_upload, triggeredBy):
        # calling parent class constructor
        threading.Thread.__init__(self)

        self.config = config
        self.supress_upload = supress_upload
        self.videoPath = ""
        self.videoName = ""
        self.videoNameNoExtention = ""
        self.mp4File = ""
        self.mp4FileName = ""
        self.httpPostRequestUri = "https://highlight-reel-core.herokuapp.com/api/upload"
        self.triggeredBy = triggeredBy

    def setVideo(self, outfile):
        self.videoPath = outfile
        self.videoName = os.path.basename(outfile)
        self.videoNameNoExtention = os.path.splitext(self.videoName)[0]
        self.mp4File = self.config.CONVERTED_FOLDER + self.videoNameNoExtention + ".mp4"
        self.mp4FileName = os.path.basename(self.mp4File)

    def getHardwareID(self):
        # Extract serial from cpuinfo file
        cpuserial = "0000000000000000"
        try:
            f = open('/proc/cpuinfo','r')
            for line in f:
                if line[0:6]=='Serial':
                    cpuserial = line[10:26]
            f.close()
        except:
            cpuserial = "ERROR000000000"
    
        return cpuserial

    def getWristbandID(self):
        return self.triggeredBy
    
    def convertToMP4(self):
        print(self.videoPath)
        print(self.videoName)
        print(self.videoNameNoExtention)
        self.mp4File = self.config.CONVERTED_FOLDER + self.videoNameNoExtention + ".mp4"
        command = f"MP4Box -add {self.videoPath} {self.mp4File}"
        call([command], shell=True)

        os.remove(self.videoPath)


    def run(self):
        self.convertToMP4()

        videoProbe = ffmpeg.probe(self.mp4File)
        videoStream = [stream for stream in videoProbe["streams"] if stream["codec_type"] == "video"][0]

        metadata = {
        "raspberryPiID": str(self.getHardwareID()),
        "wristbandID": str(self.getWristbandID()),
        "duration": float(videoStream["duration"]),
        "height": int(videoStream["height"]),
        "width" : int(videoStream["width"]),
        "utcTime": time.time(),
        }

        pprint.pprint(metadata)

        
        if not self.supress_upload:

            


            with open(self.mp4File, 'rb') as f:
                print(f"uploading video[{self.mp4FileName}] to HRCore")
                r = requests.post(
                    self.httpPostRequestUri, 
                    files={self.mp4FileName: f}, 
                    data=metadata
                )

                response = r.json()

                if response["status"] == "error":
                    print(f"error uploading video[{self.mp4FileName}]")
                    message = response["message"]
                    print(f"message: {message}")
                else:
                    print(f"success uploading video[{self.mp4FileName}]")
                    os.rename(self.mp4File, self.config.SENT_FOLDER + self.mp4FileName)