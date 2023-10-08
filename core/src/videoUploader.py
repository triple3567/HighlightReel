import json, threading, requests, os, ffmpeg, pprint, time
from subprocess import call 

class videoUploader(threading.Thread):
    def __init__(self, outfile, config, supress_upload, triggeredBy):
        # calling parent class constructor
        threading.Thread.__init__(self)

        self.config = config
        self.supress_upload = supress_upload
        self.outfile = outfile
        self.httpPostRequestUri = "http://52.20.31.145:5000/api/upload"
        self.triggeredBy = triggeredBy

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


    def run(self):

        videoProbe = ffmpeg.probe(self.outfile)
        videoStream = [stream for stream in videoProbe["streams"] if stream["codec_type"] == "video"][0]

        metadata = {
        "raspberryPiID": str(self.getHardwareID()),
        "wristbandID": str(self.getWristbandID()),
        "duration": float(videoStream["duration"]),
        "height": int(videoStream["height"]),
        "width" : int(videoStream["width"]),
        "utcTime": time.time(),
        "poolID": str(self.config.POOL_ID)
        }

        pprint.pprint(metadata)

        basename = os.path.basename(self.outfile)
        if not self.supress_upload:
            with open(self.outfile, 'rb') as f:
                print(f"uploading video[{basename}] to HRCore")
                r = requests.post(
                    self.httpPostRequestUri, 
                    files={basename: f}, 
                    data=metadata,
		    timeout=1800
                )

                print(f"done uploading video[{basename}]")
                os.rename(self.outfile, self.config.SENT_FOLDER + basename)

                #response = r.json()

                #if response["status"] == "error":
                #    print(f"error uploading video[{basename}]")
                #    message = response["message"]
                #    print(f"message: {message}")
                #else:
                #    print(f"success uploading video[{basename}]")
                #    os.rename(self.outfile, self.config.SENT_FOLDER + basename)
