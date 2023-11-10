from datetime import datetime
import subprocess
import time, threading, os, logging, sqlite3

class videoWriter(threading.Thread):
    def __init__(self, config, output, supress_upload, triggeredBy):
        # calling parent class constructor
        threading.Thread.__init__(self)

        self.config = config
        self.output = output
        self.supress_upload = supress_upload
        self.triggeredBy = triggeredBy

    def addVideoToUploadQueue(self, outfile):
        con = sqlite3.connect("/home/pi/HighlightReel/core/res/highlightreel.db")
        cur = con.cursor()
        add_video_statement = f"""
        INSERT INTO upload_queue (outfile, triggered_by, utc_time)
        VALUES
        ('{outfile}','{self.triggeredBy}',{time.time()});
        """
        cur.execute(add_video_statement)
        con.commit()

    # Get filename
    def getOutfile(self, outfolder, fileExtension):
        filename = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        outfile = outfolder + filename + fileExtension
        return outfile

    def setVideoNames(self, outfile):
        self.videoPath = outfile
        self.videoName = os.path.basename(outfile)
        self.videoNameNoExtention = os.path.splitext(self.videoName)[0]
        self.mp4File = self.config.CONVERTED_FOLDER + self.videoNameNoExtention + ".mp4"
        self.mp4FileName = os.path.basename(self.mp4File)

    def convertToMP4(self):
        self.mp4File = self.config.CONVERTED_FOLDER + self.videoNameNoExtention + ".mp4"
        command = [
            "MP4Box",
            "-add",
            f"{self.videoPath}",
            f"{self.mp4File}"
        ]
        subprocess.run(command)

        os.remove(self.videoPath)

    def run(self):
        outfile = self.getOutfile(self.config.QUEUE_FOLDER, self.config.FILE_EXTENSION)
        logging.info(f"Writing {outfile}, triggered by {self.triggeredBy}")

        self.output.fileoutput = outfile
        self.output.start()
        time.sleep(self.config.OUTPUT_START_SLEEP_TIME)

        self.output.stop()
        time.sleep(self.config.OUTPUT_STOP_SLEEP_TIME)

        # set video names
        self.setVideoNames(outfile)

        # convert to mp4
        self.convertToMP4()

        logging.info(f"converted {self.videoPath} to {self.videoNameNoExtention} triggered by {self.triggeredBy}")

        self.addVideoToUploadQueue(self.mp4File)