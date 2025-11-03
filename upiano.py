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

from machine import ADC, Pin
import time
import neopixel
import math
speaker = machine.PWM(machine.Pin(22))

GP_NUM = 18
NUM_PIXELS = 2

class Ultrasound():
   def __init__(self, trigger, echo):
       self.t = trigger
       self.e = echo
   def measure(self):
    # create trigger pulse
       self.t.low()
       time.sleep_us(2)
       self.t.high()
       time.sleep_us(15)
       self.t.low()


       start_time = time.ticks_ms()
    # wait for start of echo
       while self.e.value() == 0:


           if time.ticks_ms() - start_time == 1000:
               print("wiring is broken (signal off)")
               return -1
           signaloff = time.ticks_us()
    # measure echo width
       while self.e.value() == 1:
           if time.ticks_ms() - start_time == 1000:
               print("wiring is broken (signal on)")
               return -1
           signalon = time.ticks_us()
       # compute width
       timepassed = signalon - signaloff
       # return distance
       return timepassed/1000 * 21.1  -1.3




if __name__ == "__main__":
   ultrasound = Ultrasound(trigger = Pin(28, Pin.OUT), echo = Pin(7, Pin.IN))
   while ultrasound.measure() != -1:


       # handle new logic
       for note in reversed(note_data):
        if ultrasound.measure>=note['distance_cm']:
            pixels.fill(note['rgb'])
            pixels.write
            speaker.freq(note['frequency'])


       time.sleep(0.5)
