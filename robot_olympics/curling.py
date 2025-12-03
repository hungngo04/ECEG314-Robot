import time
from machine import Pin
from control.line_reader import LineReader
from control.drive import Drive
from control.ultrasound_sensor import UltrasoundSensor

class Curling:
    def __init__(self):
        self.lr = LineReader()
        self.drive = Drive()
        self.front_sensor = UltrasoundSensor(
            trigger_pin=Pin(28, Pin.OUT),
            echo_pin=Pin(7, Pin.IN)
        )
        self.led_distance = Pin(20, Pin.OUT)
        self.led_complete = Pin(21, Pin.OUT)
        # self.drive.straight_bias = -1.2

    def run(self):
        target_distance = 45
        velocity = 20

        time.sleep_ms(3000)

        self.follow_line_phase(velocity)
        self.straight_to_target(target_distance, velocity)

        self.led_complete.high()
        print("Curling complete!")

    def follow_line_phase(self, velocity):
        print("Phase 1: Following line")
        last_offset = 0.0
        last_time_us = time.ticks_us() - 10000
        Kp = 0.35
        Kd = 0.01

        while True:
            current_time_us = time.ticks_us()
            dt_us = time.ticks_diff(current_time_us, last_time_us)
            dt_s = dt_us / 1000000.0
            last_time_us = current_time_us

            error, confidence = self.lr.get_distance()
            darkness, darkness_confidence = self.lr.get_darkness()

            if confidence < 0.2 or darkness < 0.1:
                print("End of line detected")
                self.drive.drive(0, 0)
                time.sleep_ms(500)
                break

            derivative = 0
            if dt_s > 0:
                derivative = (error - last_offset) / dt_s

            angular_velocity = (Kp * error) + (Kd * derivative)
            last_offset = error

            self.drive.drive(velocity, angular_velocity)
            time.sleep_ms(1)

    def straight_to_target(self, target_distance, velocity):
        print("Phase 2: Going straight to target")

        while True:
            distance = self.front_sensor.get_distance()

            if distance < 90:
                self.led_distance.high()

            print(f"Distance: {distance} cm")

            if distance <= target_distance:
                self.drive.drive(0, 0)
                print(f"Target reached at {distance} cm")
                break

            adjusted_velocity = velocity
            if distance < 60:
                adjusted_velocity = velocity * 0.5
            if distance < 50:
                adjusted_velocity = velocity * 0.3

            self.drive.drive(adjusted_velocity, 0)
            time.sleep_ms(10)

        self.drive.drive(0, 0)
