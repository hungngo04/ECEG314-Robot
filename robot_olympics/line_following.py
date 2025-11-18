import time

from machine import Pin
from control.line_reader import LineReader
from control.drive import Drive
from control.ultrasound_sensor import UltrasoundSensor

class LineFollowing:
    def __init__(self):
        self.lr = LineReader()
        self.drive = Drive()
        self.ultrasound_sensor = UltrasoundSensor(
            trigger_pin=Pin(28, Pin.OUT),
            echo_pin=Pin(7, Pin.IN)
        )

    def follow_line(self):
        velocity = 25

        time.sleep_ms(3000)
        last_offset = 0.0
        last_time_us = time.ticks_us() - 10000
        Kp = 0.35
        Kd = 0.01

        while (True):
            distance = self.ultrasound_sensor.get_distance()
            # print(f"Distance: {distance}")

            current_time_us = time.ticks_us()
            dt_us = time.ticks_diff(current_time_us, last_time_us)
            dt_s = dt_us / 1000000.0
            last_time_us = current_time_us

            error, confidence = self.lr.get_distance()
            darkness, darkness_confidence = self.lr.get_darkness()

            derivative = 0
            if dt_s > 0:
                derivative = (error - last_offset) / dt_s

            angular_velocity = (Kp * error) + (Kd * derivative)
            # print(f"Error: {error} - Confidence: {confidence} - Darkness: {darkness}")
            last_offset = error

            if (distance <= 10):
                print("Obstacle detected - stopping")
                self.drive.drive(0, 0)
            elif (confidence < 0.4):
                print("Low confidence - stopping")
                self.drive.drive(0, 0)
            elif (darkness < 0.1):
                print("Not dark enough - stopping")
                self.drive.drive(0, 0)
            else:
                self.drive.drive(velocity, angular_velocity)

            time.sleep_ms(1)
