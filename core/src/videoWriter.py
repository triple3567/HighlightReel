from videoUploader import videoUploader
from datetime import datetime
import time, threading

class videoWriter(threading.Thread):
    def __init__(self, config, output, supress_upload, triggeredBy):
        # calling parent class constructor
        threading.Thread.__init__(self)

        self.config = config
        self.output = output
        self.supress_upload = supress_upload
        self.triggeredBy = triggeredBy

    # Get filename
    def getOutfile(self, outfolder, fileExtension):
        filename = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        outfile = outfolder + filename + fileExtension
        return outfile

    def uploadVideo(self, outfile):
        uploader = videoUploader(self.config, self.supress_upload) 
        uploader.setVideo(outfile)
        uploader.start()

    def run(self):
        print("Starting output")
        outfile = self.getOutfile(self.config.QUEUE_FOLDER, self.config.FILE_EXTENSION)
        self.output.fileoutput = outfile
        self.output.start()
        time.sleep(self.config.OUTPUT_START_SLEEP_TIME)

        print("Stopping output")
        self.output.stop()
        time.sleep(self.config.OUTPUT_STOP_SLEEP_TIME)

        self.uploadVideo(outfile, self.trigeredBy)