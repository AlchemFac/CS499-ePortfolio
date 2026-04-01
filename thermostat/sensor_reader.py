import board
import adafruit_ahtx0


class SensorReader:
    def __init__(self):
        i2c = board.I2C()
        self.sensor = adafruit_ahtx0.AHTx0(i2c)

    def read(self):
        temp_c = self.sensor.temperature
        humidity = self.sensor.relative_humidity

        temp_f = (temp_c * 9/5) + 32

        return {
            "temp_c": temp_c,
            "temp_f": temp_f,
            "humidity": humidity
        }