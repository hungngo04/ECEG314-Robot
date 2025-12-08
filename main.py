from robot_olympics.line_following import LineFollowing
from robot_olympics.luge import Luge
from robot_olympics.slalom import Slalom
from robot_olympics.curling import Curling
from robot_olympics.orienteering import Orienteering

program = Orienteering()
try:
    program.run()
finally:
    program.cleanup()