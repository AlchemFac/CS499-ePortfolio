import time
from sensor_reader import SensorReader
from led_manager import LEDManager
from serial_manager import SerialManager
from display_manager import ManagedDisplay
from database_manager import DatabaseManager   
from thermostat_controller import ThermostatController


def main():
    sensor = SensorReader()
    leds = LEDManager()
    serial = SerialManager()
    display = ManagedDisplay()
    database = DatabaseManager()

    thermostat = ThermostatController(
        sensor,
        leds,
        display,
        serial,
        database
    )

    while True:
        thermostat.update()
        time.sleep(2)


if __name__ == "__main__":
    main()