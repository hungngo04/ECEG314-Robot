from machine import ADC, Pin
import time
import neopixel
import math
import random
from control.line_reader import LineReader
from control.drive import Drive
from robot_olympics.line_following import LineFollowing

note_data = [
    {"note": "C4", "frequency": 261.63, "color_name": "Red", "rgb": (255, 0, 0), "distance_cm": 40},
    {"note": "C#4/Db4", "frequency": 277.18, "color_name": "Orange-Red", "rgb": (255, 69, 0), "distance_cm": 35},
    {"note": "D4", "frequency": 293.66, "color_name": "Orange", "rgb": (255, 140, 0), "distance_cm": 30},
    {"note": "D#4/Eb4", "frequency": 311.13, "color_name": "Yellow", "rgb": (255, 255, 0), "distance_cm": 25},
    {"note": "E4", "frequency": 329.63, "color_name": "Chartreuse", "rgb": (127, 255, 0), "distance_cm": 20},
    {"note": "F4", "frequency": 349.23, "color_name": "Green", "rgb": (0, 255, 0), "distance_cm": 15},
    {"note": "F#4/Gb4", "frequency": 369.99, "color_name": "Spring Green", "rgb": (0, 255, 127), "distance_cm": 10},
    {"note": "G4", "frequency": 392.00, "color_name": "Cyan", "rgb": (0, 255, 255), "distance_cm": 8},
    {"note": "G#4/Ab4", "frequency": 415.30, "color_name": "Azure", "rgb": (0, 127, 255), "distance_cm": 6},
    {"note": "A4", "frequency": 440.00, "color_name": "Blue", "rgb": (0, 0, 255), "distance_cm": 5},
    {"note": "A#4/Bb4", "frequency": 466.16, "color_name": "Violet", "rgb": (139, 0, 255), "distance_cm": 4},
    {"note": "B4", "frequency": 493.88, "color_name": "Magenta", "rgb": (255, 0, 255), "distance_cm": 3}
]

speaker = machine.PWM(machine.Pin(22))

start_time = time.time()
current_time = time.time()
line_spotted = False
notes_to_play = [
    {"id": 1, "freq": 440.00, "time": 1}, # 1s
    {"id": 2, "freq": 392.00, "time": 0.45},
    {"id": 3, "freq": 00.00, "time": 0.55}, #2s
    {"id": 4, "freq": 329.63, "time": 0.45},
    {"id": 5, "freq": 00.00, "time": 0.05},
    {"id": 6, "freq": 392.00, "time": 0.45},
    {"id": 7, "freq": 00.00, "time": 0.05}, #3s
    {"id": 8, "freq": 392.00, "time": 0.5},
    {"id": 9, "freq": 00.00, "time": 0.5}, #4s
    {"id": 10, "freq": 392.00, "time": 0.45},
    {"id": 11, "freq": 00.00, "time": 0.05},
    {"id": 12, "freq": 392.00, "time": 0.45},
    {"id": 13, "freq": 00.00, "time": 0.05}, #5s
    {"id": 14, "freq": 392.00, "time": 0.45},
    {"id": 15, "freq": 00.00, "time": 0.05}, 
    {"id": 16, "freq": 392.00, "time": 0.45},
    {"id": 17, "freq": 00.00, "time": 0.05}, #6s
    {"id": 18, "freq": 392.00, "time": 0.45},
    {"id": 19, "freq": 00.00, "time": 0.05}, 
    {"id": 20, "freq": 392.00, "time": 0.45},
    {"id": 21, "freq": 00.00, "time": 0.05}, #7s
    {"id": 22, "freq": 392.00, "time": 0.45},
    {"id": 23, "freq": 00.00, "time": 0.55}, #8s
    {"id": 24, "freq": 440.00, "time": 1}, #9s
    {"id": 25, "freq": 392.00, "time": 0.5},
    {"id": 26, "freq": 00.00, "time": 0.05}, #10s
    {"id": 27, "freq": 392.00, "time": 0.45},
    {"id": 28, "freq": 00.00, "time": 0.05}, 
    {"id": 29, "freq": 392.00, "time": 0.45},
    {"id": 30, "freq": 00.00, "time": 0.05}, #11s
    {"id": 31, "freq": 392.00, "time": 0.45},
    {"id": 32, "freq": 00.00, "time": 0.55}, #12s
    {"id": 33, "freq": 392.00, "time": 0.45},
    {"id": 34, "freq": 00.00, "time": 0.05},
    {"id": 35, "freq": 392.00, "time": 0.45}, 
    {"id": 36, "freq": 00.00, "time": 0.05}, #13s
    {"id": 37, "freq": 392.00, "time": 0.45},
    {"id": 38, "freq": 00.00, "time": 0.05},
    {"id": 39, "freq": 369.99, "time": 0.45},
    {"id": 40, "freq": 00.00, "time": 0.05}, #14s
    {"id": 41, "freq": 369.99, "time": 0.95},
    {"id": 42, "freq": 00.00, "time": 0.05}, #15
    {"id": 43, "freq": 329.63, "time": 0.5},
    {"id": 44, "freq": 0.00, "time": 0.5}, #16
    {"id": 45, "freq": 440.00, "time": 1}, # 17s
    {"id": 46, "freq": 392.00, "time": 0.45},
    {"id": 47, "freq": 00.00, "time": 0.55}, #18s
    {"id": 48, "freq": 392.00, "time": 0.45},
    {"id": 49, "freq": 00.00, "time": 0.05},
    {"id": 50, "freq": 392.00, "time": 0.45},
    {"id": 51, "freq": 00.00, "time": 0.05}, #19s
    {"id": 52, "freq": 392.00, "time": 0.5},
    {"id": 53, "freq": 00.00, "time": 0.5}, #20s
    {"id": 54, "freq": 392.00, "time": 0.45},
    {"id": 55, "freq": 00.00, "time": 0.05},
    {"id": 56, "freq": 392.00, "time": 0.45},
    {"id": 57, "freq": 00.00, "time": 0.05}, #21s
    {"id": 58, "freq": 392.00, "time": 0.45},
    {"id": 59, "freq": 00.00, "time": 0.05},
    {"id": 60, "freq": 392.00, "time": 0.45},
    {"id": 61, "freq": 00.00, "time": 0.05}, #22s
    {"id": 62, "freq": 392.00, "time": 0.45},
    {"id": 63, "freq": 00.00, "time": 0.55}, #23s
    {"id": 64, "freq": 392.00, "time": 0.45},
    {"id": 65, "freq": 00.00, "time": 0.55}, #24s
    {"id": 66, "freq": 329.63, "time": 0.45},
    {"id": 67, "freq": 00.00, "time": 0.55}, #25s
    {"id": 68, "freq": 329.63, "time": 0.5},
    {"id": 69, "freq": 440.00, "time": 0.25},
    {"id": 70, "freq": 329.63, "time": 0.5}, #26.25s
    {"id": 71, "freq": 440.00, "time": 0.25},
    {"id": 72, "freq": 329.63, "time": 0.25},
    {"id": 73, "freq": 440.00, "time": 0.25}, #27s
    {"id": 74, "freq": 329.63, "time": 1}, #28s
    {"id": 75, "freq": 164.81, "time": 0.5}
]

def main():
    for note in notes_to_play:
        dance(note)
        current_time = time.time()

def dance(note):
    line_reader = LineReader()
    robot_drive = Drive()

    if note['freq'] > 0:
        speaker.freq(int(note['freq']))
        speaker.duty_u16(32768)
    else:
        speaker.duty_u16(0)

    note_start = time.time()

    if line_spotted == False:
        i = random.randint(0,1)
    else:
        i = 2
    if i==0:
        while((time.time() - note_start) < note['time']):
            robot_drive.drive(0, random.randint(-180, 180))
            time.sleep_ms(10)
    if i==1:
        while((time.time() - note_start) < note['time']):
            robot_drive.drive(random.randint(10, 65), random.randint(-180, 180))
            darkness, darkness_confidence = line_reader.get_darkness()
            if darkness > 0.3:
                i = 2
                robot_drive.drive(35, 180)
            time.sleep_ms(10)
    if i==2:
        while((time.time() - note_start) < note['time']):
            robot_drive.drive(0, random.randint(-180, 180))
            time.sleep_ms(10)

    speaker.duty_u16(0)
            
    # if i == 0:
    #     while(time.tick_diff(current_time, start_time)<(random.randint(1,5)/2)):
    #         robot_drive(random.randint(10000,65535),random.randint(0,math.radians(360)))
    #         # add line following logic
    # elif i == 1:
    #     while(time.time()-current_time<(random.randint(1,5)/2)):
    #         robot_drive(0,random.randint(0,math.radians(360)))

    # elif i == 2:
    #     while(time.time()-current_time<(random.randint(1,5)/2)):
    #         robot_drive(-random.randint(10000,65535),random.randint(0,math.radians(360)))
        



main()