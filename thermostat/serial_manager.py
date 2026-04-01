import serial
import config


class SerialManager:

    def __init__(self):
        self.serial = serial.Serial(
            config.SERIAL_PORT,
            config.BAUD_RATE,
            timeout=1
        )

    def send(self, message):
        self.serial.write((message.encode())