import time

from machine import Pin
from control.line_reader import LineReader
from control.drive import Drive

class Luge:
    def __init__(self):
        self.lr = LineReader()
        self.drive = Drive()

    def run(self):
        max_velocity = 25
        min_velocity = 10
        max_angular_velocity = 35
        search_angular_velocity = 10

        last_offset = 0.0
        last_time_us = time.ticks_us() - 10000
        search_direction = 1

        Kp = 0.6
        Kd = 0.04

        try:
            while (True):
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

                if angular_velocity > max_angular_velocity:
                    angular_velocity = max_angular_velocity
                elif angular_velocity < -max_angular_velocity:
                    angular_velocity = -max_angular_velocity

                last_offset = error

                adaptive_velocity = min_velocity + (max_velocity - min_velocity) * confidence

                if confidence > 0.85:
                    adaptive_velocity *= 1.05

                if confidence < 0.4:
                    adaptive_velocity *= 0.5

                if darkness < 0.15:
                    adaptive_velocity *= 0.65

                if (confidence < 0.15 or darkness < 0.08):
                    print("Searching for line...")
                    if error > 0:
                        search_direction = 1
                    elif error < 0:
                        search_direction = -1
                    self.drive.drive(0, search_direction * search_angular_velocity)
                else:
                    self.drive.drive(adaptive_velocity, angular_velocity)

                time.sleep_ms(1)
        finally:
            self.drive.drive(0, 0)
