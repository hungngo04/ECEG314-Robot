from machine import Pin
import time

from control.ultrasound_sensor import UltrasoundSensor
from control.drive import RobotDrive
from control.led_controller import LEDController

class BullseyeController:
    def __init__(self, front_sensor, start_sensor, robot_drive, led_controller):
        self.front_sensor = front_sensor
        self.start_sensor = start_sensor
        self.robot = robot_drive
        self.leds = led_controller

    def wait_for_start(self, gate_distance_threshold = 30):
        while True:
            distance = self.start_sensor.get_distance()
            if distance > gate_distance_threshold:
                return True
            
    def drive_to_target(self, target_distance_cm, speed = 50, stop_margin = 2):
        while True:
            current_distance = self.front_sensor.get_distance()

            if (current_distance == -1):
                continue

            if (current_distance <= target_distance_cm + stop_margin):
                self.robot.drive(0, 0)
                self.leds.set_color((0, 255, 0))
                break

            if (current_distance < 10):
                self.leds.set_color((255, 0, 0))

            self.robot.drive(speed, 0)
            time.sleep(0.05)

if __name__ == "__main__":
    front_sensor = UltrasoundSensor(
        trigger_pin = Pin(28, Pin.OUT),
        echo_pin = Pin(7, Pin.IN)
    )

    start_sensor = UltrasoundSensor(
        trigger_pin = Pin(28, Pin.OUT),
        echo_pin = Pin(7, Pin.IN)
    )

    leds = LEDController()
    robot = RobotDrive()

    bullseye = BullseyeController(front_sensor, start_sensor, robot, leds)

    target_distance = 225 # TODO: Adjust this value

    bullseye.wait_for_start()
    bullseye.drive_to_target(target_distance_cm = target_distance, speed = 50)
