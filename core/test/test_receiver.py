import time, sys
sys.path.insert(1, "/home/pi/HighlightReel/core/src")
from receiverHandler import receiverHandler
rh = receiverHandler()

print("Waiting for input on receiver")

while not rh.isTriggered():
    time.sleep(0.01)

print("Receiver success")