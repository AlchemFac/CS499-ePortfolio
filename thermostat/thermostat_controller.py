import time
from data_processor import CircularBuffer, SensorReading

class ThermostatController:

    def __init__(self, sensor, leds, display, serial, database):
        self.sensor = sensor
        self.leds = leds
        self.display = display
        self.serial = serial
        self.database = database

        self.set_point = 72
        self.buffer = CircularBuffer(size=5)

    def moving_average_temp(self):
        readings = self.buffer.get_all()
        if not readings:
            return 0
        return sum(r.temp for r in readings) / len(readings)

    def moving_average_humidity(self):
        readings = self.buffer.get_all()
        if not readings:
            return 0
        return sum(r.humidity for r in readings) / len(readings)

    def rate_of_change(self):
        readings = self.buffer.get_all()

        if len(readings) < 2:
            return 0

        first = readings[0]
        last = readings[-1]

        delta_temp = last.temp - first.temp
        delta_time = last.timestamp - first.timestamp

        if delta_time == 0:
            return 0

        return delta_temp / delta_time

    def update(self):
        reading = self.sensor.read()

        temp = reading["temp_f"]
        humidity = reading["humidity"]
        now = time.time()

        self.buffer.add(SensorReading(temp, humidity, now))

        avg_temp = self.moving_average_temp()
        avg_humidity = self.moving_average_humidity()
        rate = self.rate_of_change()

        if avg_temp < self.set_point:
            self.leds.heat_on()
            status = "HEATING"
        elif avg_temp > self.set_point:
            self.leds.cool_on()
            status = "COOLING"
        else:
            self.leds.off()
            status = "IDLE"

        alert = "NORMAL"
        alert_message = "System operating within expected range"

        if abs(rate) > 0.5:
            alert = "RAPID CHANGE"
            alert_message = "Temperature changing rapidly"

        if avg_temp > 85:
            alert = "CRITICAL HIGH TEMP"
            alert_message = "Average temperature exceeded safe upper threshold"

        elif avg_temp < 60:
            alert = "LOW TEMP WARNING"
            alert_message = "Average temperature dropped below lower threshold"

        elif avg_humidity > 70:
            alert = "HIGH HUMIDITY WARNING"
            alert_message = "Average humidity exceeded recommended threshold"

        # Display output
        line1 = f"T:{avg_temp:.1f} H:{int(avg_humidity)}"
        line2 = f"{status} SP:{self.set_point}"
        display_message = line1 + "\n" + line2

        self.display.write(display_message)

        # Serial output
        message = f"{status},{round(avg_temp,1)},{round(avg_humidity,1)},{self.set_point},{round(rate,2)},{alert}"
        self.serial.send(message)

        # Save reading to database
        self.database.insert_reading(
            temperature_f=round(avg_temp, 1),
            humidity=round(avg_humidity, 1),
            mode=status,
            set_point=self.set_point,
            status=alert
        )

        # Save alert to database only when not normal
        if alert != "NORMAL":
            self.database.insert_alert(
                alert_level=alert,
                message=alert_message,
                temperature_f=round(avg_temp, 1),
                humidity=round(avg_humidity, 1),
                mode=status
            )