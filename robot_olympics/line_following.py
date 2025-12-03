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

    def run(self):
        velocity = 100

        BASE_VELOCITY = 25
        BASE_KP = 0.15
        BASE_KD = 0.025
        BASE_KI = 0.005

        velocity_scale = velocity / BASE_VELOCITY
        Kp = BASE_KP * velocity_scale
        Kd = BASE_KD * velocity_scale * 2.0
        Ki = BASE_KI * (velocity_scale ** 0.5)

        max_integral = 50

        last_error = 0.0
        integral_error = 0.0
        last_time_us = time.ticks_us() - 10000

        while (True):
            distance = self.ultrasound_sensor.get_distance()
            # print(f"Distance: {distance}")

            current_time_us = time.ticks_us()
            dt_us = time.ticks_diff(current_time_us, last_time_us)
            dt_s = dt_us / 1000000.0
            last_time_us = current_time_us

            error, confidence = self.lr.get_distance()
            darkness, darkness_confidence = self.lr.get_darkness()

            # PID calculations
            # Proportional term
            proportional = Kp * error

            # Integral term (with anti-windup)
            integral_error += error * dt_s
            integral_error = max(-max_integral, min(max_integral, integral_error))  # Clamp
            integral = Ki * integral_error

            # Derivative term
            derivative = 0
            if dt_s > 0:
                derivative = (error - last_error) / dt_s
            derivative_term = Kd * derivative

            # Combined PID output
            angular_velocity = proportional + integral + derivative_term

            # print(f"Error: {error} - P: {proportional:.2f} - I: {integral:.2f} - D: {derivative_term:.2f}")
            last_error = error

            if (distance <= 20):
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
