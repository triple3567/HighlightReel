import os, logging, requests, threading, time

class logUploader(threading.Thread):
    def __init__(self, config):
        # calling parent class constructor
        threading.Thread.__init__(self)

        self.createStartupLog()

        self.config = config
        self.httpPostRequestUri = "http://52.20.31.145:5000/api/log_upload"
        self.logDir = "/home/pi/HighlightReel/core/out/logs/"
        self.logFiles = []

        for root, dirs, files in os.walk(os.path.abspath(self.logDir)):
            for file in files:
                self.logFiles.append(file)
    
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

    def createStartupLog(self):
        now = time.strftime("%y-%m-%d_%H:%M:%S", time.gmtime())
        filename = f"/home/pi/HighlightReel/core/out/logs/startup_{self.getHardwareID()}_{now}UTC.log"
        f = open(filename, "w")
        f.close()

    def run(self):
        time.sleep(120)
        logging.info(f"Found past log files: {self.logFiles}")

        while len(self.logFiles) != 0:
            log = self.logFiles[0]
            full_path = self.logDir + log

            logging.info(f"Starting upload of {full_path}")
            with open(full_path, 'rb') as f:
                try:
                    r = requests.post(
                        self.httpPostRequestUri,
                        files={log: f},
                        timeout=900
                    )

                    logging.info(f"Success uploading log {full_path}. Got Response: {r}")
                    
                    os.remove(full_path)
                    self.logFiles.pop(0)

                except requests.exceptions.RequestException as e:
                    logging.error("requests.exceptions.RequestException... Error handling log upload", exc_info=True)
                except:
                    logging.error(f"Error uploading video {basename}", exc_info=True)
            time.sleep(5)

