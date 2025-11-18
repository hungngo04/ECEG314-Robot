import machine

class Drive():
    def __init__(self):
        self.M1A = machine.PWM(machine.Pin(8))
        self.M1B = machine.PWM(machine.Pin(9))
        self.M2A = machine.PWM(machine.Pin(10))
        self.M2B = machine.PWM(machine.Pin(11))

        self.M1A.freq(8_000)
        self.M1B.freq(8_000)
        self.M2A.freq(8_000)
        self.M2B.freq(8_000)
    
    def drive(self, speed, omega):
        omega = omega*-1
        v_right = ((2*speed)+(omega*13/2))/2
        v_left = 2*speed-v_right

        duty_cycle_left = int(1176*abs(v_left) + 1274)
        duty_cycle_right = int(1176*abs(v_right) + 1274)

        if (speed == 0 and omega == 0):
            self.M1A.duty_u16(0)
            self.M1B.duty_u16(0)
            self.M2A.duty_u16(0)
            self.M2B.duty_u16(0)
        elif (speed == 0 and omega != 0):
            if v_left >= 0:
                self.M1A.duty_u16(duty_cycle_left)
                self.M1B.duty_u16(0)
                self.M2A.duty_u16(0)
                self.M2B.duty_u16(-duty_cycle_left)
            else:
                self.M1A.duty_u16(0)
                self.M1B.duty_u16(duty_cycle_right)
                self.M2A.duty_u16(-duty_cycle_right)
                self.M2B.duty_u16(0)
        else:
            if v_left >= 0:
                self.M1A.duty_u16(duty_cycle_left)
                self.M1B.duty_u16(0)
            else:
                self.M1B.duty_u16(duty_cycle_left)
                self.M1A.duty_u16(0)
            if v_right >= 0:
                self.M2A.duty_u16(duty_cycle_right)
                self.M2B.duty_u16(0)
            else:
                self.M2B.duty_u16(duty_cycle_right)
                self.M2A.duty_u16(0)
