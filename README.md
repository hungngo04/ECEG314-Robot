# eceg341_robot

- LEFT motor (M1): M1A forward, M1B reverse
- RIGHT motor (M2): M2B forward, M2A reverse

python3 -m mpremote fs cp line_reader.py :line_reader.py
python3 -m mpremote fs cp drive.py :drive.py

Delete everything on the robot:
    python3 -m mpremote fs rm -r :

Copy everything to the robot:
python3 -m mpremote fs rm -r : + \
  fs mkdir :control + \
  fs mkdir :robot_olympics + \
  fs mkdir :test + \
  fs cp main.py :main.py + \
  fs cp simple_reader.py :simple_reader.py + \
  fs cp control/drive.py :control/drive.py + \
  fs cp control/led_controller.py :control/led_controller.py + \
  fs cp control/line_reader.py :control/line_reader.py + \
  fs cp control/piano_controller.py :control/piano_controller.py + \
  fs cp control/speaker_controller.py :control/speaker_controller.py + \
  fs cp control/ultrasound_sensor.py :control/ultrasound_sensor.py + \
  fs cp robot_olympics/1m_dash.py :robot_olympics/1m_dash.py + \
  fs cp robot_olympics/curling.py :robot_olympics/curling.py + \
  fs cp robot_olympics/line_following.py :robot_olympics/line_following.py + \
  fs cp robot_olympics/slalom.py :robot_olympics/slalom.py
  
min: [135, 150, 135, 165, 120, 120]
max: [600, 600, 600, 600, 600, 600]