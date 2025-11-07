from machine import Pin
import neopixel

class LEDController:
    def __init__(self, pin_num, num_pixels):
        self.pixels = neopixel.NeoPixel(Pin(pin_num), num_pixels)
        self.num_pixels = num_pixels

    def set_color(self, rgb):
        self.pixels.fill(rgb)
        self.pixels.write()

    def clear(self):
        self.pixels.fill((0, 0, 0))
        self.pixels.write()