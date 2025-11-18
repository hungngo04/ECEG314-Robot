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
        time.sleep_us(10)
        self.trigger.low()

        timeout_start = time.ticks_ms()

        # Wait for echo to go high
        while self.echo.value() == 0:
            if time.ticks_diff(time.ticks_ms(), timeout_start) > 30:
                print("Sensor error: No echo signal received")
                return -1

        signaloff = time.ticks_us()

        # Wait for echo to go low
        while self.echo.value() == 1:
            if time.ticks_diff(time.ticks_ms(), timeout_start) > 30:
                print("Sensor error: Echo signal timeout")
                return -1

        signalon = time.ticks_us()

        timepassed = signalon - signaloff
        distance = (timepassed * 0.0343) / 2

        return distance
