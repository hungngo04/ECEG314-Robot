import time
import math
from test.drivetest import RobotDrive

robot = RobotDrive()

# TEST 1 -- straight!
# 20 cm/s, 0 rad/s 
time.sleep_ms(1000)
robot.drive(20, 0)
time.sleep_ms(500)
# stop, robot should have gone 10 cm forward. Check! I got about 12 cm.
robot.drive (0, 0)
time.sleep_ms(500)


# TEST 2 -- reverse
# -20 cm/s, 0 rad/s 
robot.drive (-20, 0)
time.sleep_ms(500)
# stop, robot should have gone 10 cm in reverse. Drive the M1B and M2B pins!
robot.drive (0, 0)
time.sleep_ms(500)

# TEST 3 -- RIGHT
robot.drive (20, math.radians(180))
time.sleep_ms(500)
# stop, robot should have turned about 90 degrees clockwise
robot.drive (0, 0)
time.sleep_ms(500)

# TEST 4 -- LEFT
robot.drive (20, -math.radians(180))
time.sleep_ms(500)
# stop, we should have turned about 180 degrees counter clockwise
robot.drive (0, 0)
time.sleep_ms(500)

# TEST 5 -- ROTATE in PLACE
robot.drive (0, math.radians(360))
time.sleep_ms(1000)
# stop, robot should turn about 360 degrees clockwise
robot.drive (0, 0)
time.sleep_ms(500)
