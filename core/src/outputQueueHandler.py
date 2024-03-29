from videoWriter import videoWriter
import time, threading, logging

class outputQueueHandler(threading.Thread):
    def __init__(self, config, supress_upload):
        # calling parent class constructor
        threading.Thread.__init__(self)
        self.config = config
        self.supress_upload = supress_upload
        self.queue = []

    def push(self, output, triggeredBy):
        self.queue.append((output, triggeredBy))
        logging.info(f"Added output to queue triggered by {triggeredBy}")

    def run(self):
        while True:
            if self.queue:
                element = self.queue.pop()
                output = element[0]
                triggeredBy = element[1]

                logging.info(f"Popping element triggered by {triggeredBy} from the output queue")

                writer = videoWriter(self.config, output, self.supress_upload, triggeredBy)
                writer.start()
                writer.join()
            time.sleep(0.1)