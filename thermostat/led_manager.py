from gpiozero import LED


class LEDManager:

    def __init__(self):
        self.red = LED(17)
        self.blue = LED(27)

    def heat_on(self):
        self.red.on()
        self.blue.off()

    def cool_on(self):
        self.blue.on()
        self.red.off()

    def off(self):
        self.red.off()
        self.blue.off()