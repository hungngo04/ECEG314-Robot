import time
import math
from drive import RobotDrive

robot = RobotDrive(bias=-0.05, speed_to_duty_factor=1192, wheelbase=13.0)

# TEST 1 - straight!
robot.drive(20, 0)
time.sleep_ms(500)
robot.stop()
time.sleep_ms(500)

# TEST 2 - reverse
robot.drive(-20, 0)
time.sleep_ms(500)
robot.stop()
time.sleep_ms(500)

# TEST 3 - right
robot.drive(20, math.radians(180))
time.sleep_ms(500)
robot.stop()
time.sleep_ms(500)

# TEST 4 - left
robot.drive(20, -math.radians(180))
time.sleep_ms(500)
robot.stop()
time.sleep_ms(500)

# TEST 5 - rotate in place
robot.drive(0, math.radians(360))
time.sleep_ms(1000)
robot.stop()
time.sleep_ms(500)