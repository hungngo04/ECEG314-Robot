import sys
import time
import math
from machine import Pin, ADC

M1A = machine.PWM(machine.Pin(8))
M1B = machine.PWM(machine.Pin(9))
M2A = machine.PWM(machine.Pin(10))
M2B = machine.PWM(machine.Pin(11))
M1A.freq(8_000)
M1B.freq(8_000)
M2A.freq(8_000)
M2B.freq(8_000)
def drive(speed, omega):
    omega = omega*-1
    v_right = ((2*speed)+(omega*13/2))/2
    v_left = 2*speed-v_right
    print(v_left, v_right)
    #convert to duty cycle from here

    if (speed ==0 and omega==0):
        M1A.duty_u16(0)
        M1B.duty_u16(0)
        M2A.duty_u16(0)
        M2B.duty_u16(0)
    elif (speed == 0 and omega != 0):
        #1/2 * pi*13
        #vl = -vr
        if v_left >= 0:
            M1A.duty_u16(int(1176*abs(v_left) + 1274))
            M1B.duty_u16(0)
            M2A.duty_u16(0)
            M2B.duty_u16(-1*int(1176*abs(v_left) + 1274))
        else:
            M1A.duty_u16(0)
            M1B.duty_u16(int(1176*abs(v_right) + 1274))
            M2A.duty_u16(-1*int(1176*abs(v_right) + 1274))
            M2B.duty_u16(0)
        
        
    else:
        if v_left >= 0:
            M1A.duty_u16(int(1176*abs(v_left) + 1274))
            M1B.duty_u16(0)
        else:
            M1B.duty_u16(int(1176*abs(v_left) + 1274))
            M1A.duty_u16(0)
        if v_right >= 0:
            M2A.duty_u16(int(1176*abs(v_right) + 1274))
            M2B.duty_u16(0)
        else:
            M2B.duty_u16(int(1176*abs(v_right) + 1274))
            M2A.duty_u16(0)

    


# TEST 1 -- straight!
# 20 cm/s, 0 rad/s 
time.sleep_ms(1000)
drive (20, 0)
time.sleep_ms(500)
# stop, robot should have gone 10 cm forward. Check! I got about 12 cm.
drive (0, 0)
time.sleep_ms(500)


# TEST 2 -- reverse
# -20 cm/s, 0 rad/s 
drive (-20, 0)
time.sleep_ms(500)
# stop, robot should have gone 10 cm in reverse. Drive the M1B and M2B pins!
drive (0, 0)
time.sleep_ms(500)

# TEST 3 -- RIGHT
drive (20, math.radians(180))
time.sleep_ms(500)
# stop, robot should have turned about 90 degrees clockwise
drive (0, 0)
time.sleep_ms(500)

# TEST 4 -- LEFT
drive (20, -math.radians(180))
time.sleep_ms(500)
# stop, we should have turned about 180 degrees counter clockwise
drive (0, 0)
time.sleep_ms(500)

# TEST 5 -- ROTATE in PLACE
drive (0, math.radians(360))
time.sleep_ms(1000)
# stop, robot should turn about 360 degrees clockwise
drive (0, 0)
time.sleep_ms(500)
