import os, logging, requests, threading, time

class logUploader(threading.Thread):
    def __init__(self, config):
        # calling parent class constructor
        threading.Thread.__init__(self)

        self.config = config
        self.httpPostRequestUri = "http://52.20.31.145:5000/api/log_upload"
        self.logDir = "/home/pi/HighlightReel/core/out/logs/"
        self.logFiles = []

        for root, dirs, files in os.walk(os.path.abspath(self.logDir)):
            for file in files:
                self.logFiles.append(file)

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

