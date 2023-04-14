from videoUploader import videoUploader
from datetime import datetime
import subprocess
import time, threading, os

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
        uploader = videoUploader(outfile, self.config, self.supress_upload, self.triggeredBy) 
        uploader.start()
        uploader.join()

    def setVideoNames(self, outfile):
        self.videoPath = outfile
        self.videoName = os.path.basename(outfile)
        self.videoNameNoExtention = os.path.splitext(self.videoName)[0]
        self.mp4File = self.config.CONVERTED_FOLDER + self.videoNameNoExtention + ".mp4"
        self.mp4FileName = os.path.basename(self.mp4File)

    def convertToMP4(self):
        print(self.videoPath)
        print(self.videoName)
        print(self.videoNameNoExtention)
        self.mp4File = self.config.CONVERTED_FOLDER + self.videoNameNoExtention + ".mp4"
        command = [
            "MP4Box",
            "-add",
            f"{self.videoPath}",
            f"{self.mp4File}"
        ]
        subprocess.run(command)

        os.remove(self.videoPath)
    
    def addWatermark(self):
        self.watermarkedFile = self.config.WATERMARKED_FOLDER + self.mp4FileName 
        command = f"cpulimit --limit=100 -- /usr/bin/ffmpeg -y -i {self.mp4File} -i {self.config.WATERMARK} -filter_complex \"overlay \" {self.watermarkedFile}"
        command = [
            "/usr/bin/cpulimit" ,
            "-f",
            "--limit=200",
            "--",
            "/usr/bin/ffmpeg",
            "-y",
            "-i",
            f"{self.mp4File}",
            "-i",
            f"{self.config.WATERMARK}",
            "-filter_complex",
            "overlay ",
            f"{self.watermarkedFile}"
        ]
        subprocess.run(command)

        os.remove(self.mp4File)

    def run(self):
        print("Starting output")
        outfile = self.getOutfile(self.config.QUEUE_FOLDER, self.config.FILE_EXTENSION)
        self.output.fileoutput = outfile
        self.output.start()
        time.sleep(self.config.OUTPUT_START_SLEEP_TIME)

        print("Stopping output")
        self.output.stop()
        time.sleep(self.config.OUTPUT_STOP_SLEEP_TIME)

        # set video names
        self.setVideoNames(outfile)

        # convert to mp4
        self.convertToMP4()

        # add watermark
        self.addWatermark()

        self.uploadVideo(self.watermarkedFile)