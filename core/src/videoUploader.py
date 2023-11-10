from subprocess import call 
import json, threading, requests, os, ffmpeg, pprint, time, logging, sqlite3

class videoUploader(threading.Thread):
    def __init__(self, config, supress_upload):
        # calling parent class constructor
        threading.Thread.__init__(self)

        self.config = config
        self.supress_upload = supress_upload
        self.httpPostRequestUri = "http://52.20.31.145:5000/api/upload"

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

    def getOldestVideo(self):
        con = sqlite3.connect("/home/pi/HighlightReel/core/res/highlightreel.db")
        cur = con.cursor()
        select_newest_video_statement = f"""
        SELECT * FROM upload_queue ORDER BY utc_time ASC LIMIT 1;
        """
        res = cur.execute(select_newest_video_statement)

        return res.fetchone()

    def removeOldestVideo(self, db_res):
        con = sqlite3.connect("/home/pi/HighlightReel/core/res/highlightreel.db")
        cur = con.cursor()
        delete_video_statement = f"""
        DELETE FROM upload_queue WHERE outfile = '{db_res[0]}';
        """
        res = cur.execute(delete_video_statement)
        con.commit()

        os.remove(db_res[0])

    def run(self):

        while True:
            db_res = self.getOldestVideo()

            if db_res is not None:
                outfile = db_res[0]
                triggered_by = db_res[1]
                timestamp = float(db_res[2])

                videoProbe = ffmpeg.probe(outfile)
                videoStream = [stream for stream in videoProbe["streams"] if stream["codec_type"] == "video"][0]

                metadata = {
                "raspberryPiID": str(self.getHardwareID()),
                "wristbandID": str(triggered_by),
                "duration": float(videoStream["duration"]),
                "height": int(videoStream["height"]),
                "width" : int(videoStream["width"]),
                "utcTime": timestamp,
                "poolID": str(self.config.POOL_ID)
                }

                basename = os.path.basename(outfile)
                if not self.supress_upload:
                    with open(outfile, 'rb') as f:

                        logging.info(f"Starting to upload {basename} with metadata:\tf{metadata}")
                        try:
                            r = requests.post(
                            self.httpPostRequestUri, 
                            files={basename: f}, 
                            data=metadata,
                            timeout=900
                            )
                            
                            logging.info(f"Success uploading video {basename}. Got Response {r}")
                            self.removeOldestVideo(db_res)

                        except requests.exceptions.RequestException as e:
                            logging.error(f"Error uploading video {basename}", exc_info=True)
                        except:
                            logging.error(f"Error uploading video {basename}", exc_info=True)

            time.sleep(1)
