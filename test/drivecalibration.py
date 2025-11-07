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

#time.sleep_ms(5000)

# 0 = even, >0 = bias right, <0 = bias left
bias = 0.0

# split bias to left/right motors
left_bias = 1.0 - bias/2
right_bias = 1.0 + bias/2 

M1A.duty_u16(int(0x7fff * left_bias))
M1B.duty_u16(0)

M2A.duty_u16(int(0x7fff * right_bias))
M2B.duty_u16(0)

time.sleep_ms(3600)
M1A.duty_u16(0)
M2A.duty_u16(0)