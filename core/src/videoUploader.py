from subprocess import call 
import json, threading, requests, os, ffmpeg, pprint, time, logging

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

        basename = os.path.basename(self.outfile)
        if not self.supress_upload:
            with open(self.outfile, 'rb') as f:

                logging.info(f"Starting to upload {basename} with metadata:\nf{metadata}")

                try:
                    r = requests.post(
                        self.httpPostRequestUri, 
                        files={basename: f}, 
                        data=metadata,
                        timeout=900
                    )

                    logging.info(f"Success uploading video {basename}")
                    os.rename(self.outfile, self.config.SENT_FOLDER + basename)
                    
                except requests.exceptions.RequestException as e:
                    logging.error("requests.exceptions.RequestException", exc_info=True)
