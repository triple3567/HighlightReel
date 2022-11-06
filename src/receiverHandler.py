import RPi.GPIO as GPIO

class receiverHandler():
    def __init__(self):
        self.RECEIVER_GPIO_PIN = 23
        self.configurePins()

    def configurePins(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.RECEIVER_GPIO_PIN, GPIO.IN)

    def isTriggered(self):
        return GPIO.input(self.RECEIVER_GPIO_PIN)