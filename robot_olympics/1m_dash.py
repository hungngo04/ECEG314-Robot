from machine import Pin
import time
from control.ultrasound_sensor import UltrasoundSensor
from control.line_reader import LineReader
from control.drive import RobotDrive

class RaceController:
    def __init__(self, ultrasound_sensor, line_reader, robot_drive):
        self.sensor = ultrasound_sensor
        self.line_reader = line_reader
        self.robot = robot_drive

    def wait_for_start(self, gate_distance_threshold=30):
        while True: # loop as fast as possible
            distance = self.sensor.get_distance()
            if distance > gate_distance_threshold:
                return True

    def race(self, speed=100, darkness_threshold=0.4, max_time=10):
        start_time = time.ticks_ms()

        while True:
            self.robot.drive(speed, 0)

            _, darkness, _ = self.line_reader.reflectance_sample(
                pin=[Pin(0), Pin(1), Pin(2), Pin(3), Pin(4), Pin(5)],
                samples=5,
                delay_us=15
            )

            if darkness < darkness_threshold:
                self.robot.drive(-80, 0)
                time.sleep(0.1)
                self.robot.drive(0,0)
                break

            # TODO - Hung: Check to see if the robot can stop properly

            time.sleep(0.01)

if __name__ == "__main__":
    sensor = UltrasoundSensor(
        trigger_pin=Pin(28, Pin.OUT),
        echo_pin=(7, Pin.IN)
    )

    line_reader = LineReader()
    robot = RobotDrive()

    race = RaceController(sensor, line_reader, robot)

    race.wait_for_start(gate_distance_threshold=30)

    # TODO: Adjust speed
    race.race(speed=120, darkness_threshold=0.4)
