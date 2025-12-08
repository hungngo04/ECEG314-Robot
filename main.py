from robot_olympics.line_following import LineFollowing
from robot_olympics.luge import Luge
from robot_olympics.slalom import Slalom
from robot_olympics.curling import Curling
from robot_olympics.orienteering import Orienteering

# ===== CALIBRATION CODE =====
# Uncomment the section below to calibrate straight driving
# Measure the actual distance traveled and calculate cm_per_second
#
from control.drive import Drive
import time

# drive = Drive()
# try:
#     print("=== Straight Driving Calibration ===")
#     print("Robot will drive straight for 2 seconds at velocity 10")
#     print("Measure the distance traveled in cm")
#     time.sleep(3)  # Time to get ready

#     velocity = 10
#     duration_ms = 2000

#     print(f"Starting: velocity={velocity}, duration={duration_ms}ms")
#     drive.drive(velocity, 0)
#     time.sleep_ms(duration_ms)
#     drive.drive(0, 0)
#     print("Stopped. Measure the distance traveled.")
#     print(f"If traveled X cm, then cm_per_second = X / {duration_ms/1000}")

#     time.sleep(2)
# finally:
#     drive.cleanup()

program = Orienteering()
try:
    program.run()
finally:
    # Ensure cleanup happens even if program crashes or is interrupted
    program.cleanup()