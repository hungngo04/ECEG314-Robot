from machine import Pin
import time

def reflectance_sample(pin, samples, delay_us):
    decay_list = []

    # charge capacitance
    for p in pin:
        p.init(Pin.OUT, value=1)

    time.sleep_us(10)
        # change to input
    for p in pin:
        p.init(Pin.IN, pull = None)
        count = 0
        for i in range(samples):
            # wait one sample period
            time.sleep_us(delay_us)
            # count the number of 1's
            count += p.value()    
        # the pulse width is the number of 1's 
        # detected times the delay
        count = count * delay_us
        decay_list.append(count)
    
    lowest = min(decay_list)
    subtracted_decay = []
    subtracted_decay = list(map(lambda x: x - lowest, decay_list))
    sum_subtracted = sum(subtracted_decay)
    normalized = []
    if sum_subtracted != 0:
        normalized = list(map(lambda x: x/sum_subtracted, subtracted_decay))
    else:
        normalized = [0]*6
    return calc_position(normalized)

def calc_position(normalized):
    positions = [-20, -12, -4, 4, 12, 20]
    position = sum(list(map(lambda x, y: x*y, normalized, positions)))
    return position


if __name__=="__main__":    
    while True:        
        d = reflectance_sample(pin = [Pin(0), Pin(1), Pin(2), Pin(3), Pin(4), Pin(5)], 
                samples = 40, delay_us = 15)
        print(f"Position: {d}.")
        time.sleep(0.5)