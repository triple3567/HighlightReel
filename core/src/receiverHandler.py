import RPi.GPIO as GPIO

class receiverHandler():
    def __init__(self, RECEIVER_GPIO_PIN):
        self.RECEIVER_GPIO_PIN = RECEIVER_GPIO_PIN
        self.configurePins()

    def configurePins(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.RECEIVER_GPIO_PIN, GPIO.IN)

    def isTriggered(self):
        return GPIO.input(self.RECEIVER_GPIO_PIN)