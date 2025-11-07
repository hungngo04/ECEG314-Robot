from machine import Pin
import time

class UltrasoundSensor:
    def __init__(self, trigger_pin, echo_pin):
        self.trigger = trigger_pin
        self.echo = echo_pin

    def get_distance(self):
        self.trigger.low()
        time.sleep_us(2)
        self.trigger.high()
        time.sleep_us(15)
        self.trigger.low()

        start_time = time.ticks_ms()

        while self.echo.value() == 0:
            if time.ticks_ms() - start_time >= 1000:
                print("Sensor error: No echo signal received")
                return -1
            signaloff = time.ticks_us()

        while self.echo.value() == 1:
            if time.ticks_ms() - start_time >= 1000:
                print("Sensor error: Echo signal timeout")
                return -1
            signalon = time.ticks_us()

        timepassed = signalon - signaloff
        distance = timepassed / 1000 * 21.1 - 1.3

        return distance
