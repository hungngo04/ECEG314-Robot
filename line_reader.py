from machine import Pin
import time
import math

class LineReader:
    def __init__(self):
        self.min_brightness_decay = [135, 150, 135, 165, 120, 120]
        self.max_brightness_decay = [600, 600, 600, 600, 600, 600]
        self.scaling_factor = 0.001

    def get_distance(self):
        while True:        
            distance, darkness, confidence = self.reflectance_sample(pin = [Pin(0), Pin(1), Pin(2), Pin(3), Pin(4), Pin(5)], 
                                        samples = 40, 
                                        delay_us = 15)
            
            distance *= -1
            
            print(f"Position: {distance} mm")
            time.sleep(0.5)

    def get_darkness(self):
        while True:
            distance, darkness, confidence = self.reflectance_sample(pin = [Pin(0), Pin(1), Pin(2), Pin(3), Pin(4), Pin(5)], 
                                        samples = 40, 
                                        delay_us = 15)
            
            print(f"Darkness: {darkness}, Confidence: {confidence}")
            time.sleep(0.5)

    def reflectance_sample(self, pin, samples, delay_us):
        decay_list = []

        for p in pin:
            p.init(Pin.OUT, value=1)

        time.sleep_us(10)

        for p in pin:
            p.init(Pin.IN, pull = None)
            count = 0

            for i in range(samples):
                time.sleep_us(delay_us)
                count += p.value()    

            count = count * delay_us
            decay_list.append(count)
        
        # Calculate darkness
        darkness_decay_list = list(map(lambda x,y: x - y, decay_list, self.min_brightness_decay))
        darkness = sum(darkness_decay_list) / sum(list(map(lambda x, y: x - y, self.max_brightness_decay, self.min_brightness_decay)))

        # Calculate variance
        decay_list_variance = self.population_variance(decay_list)
        confidence = 1 - pow(math.e, -self.scaling_factor * decay_list_variance)

        subtracted_decay = []
        subtracted_decay = list(map(lambda x: x - min(decay_list), decay_list))
        sum_subtracted = sum(subtracted_decay)
        normalized = []

        if sum_subtracted != 0:
            normalized = list(map(lambda x: x/sum_subtracted, subtracted_decay))
        else:
            normalized = [0] * 6

        return self.calc_position(normalized), darkness, confidence

    def calc_position(self, normalized):
        positions = [-20, -12, -4, 4, 12, 20]
        position = sum(list(map(lambda x, y: x*y, normalized, positions)))
        return position
    
    def population_variance(self, data):
        n = len(data)
        mean = sum(data) / n
        return sum((x - mean) ** 2 for x in data) / n

if __name__=="__main__":    
    line_reader = LineReader()
    line_reader.get_darkness()