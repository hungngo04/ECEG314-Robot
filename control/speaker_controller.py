from machine import Pin, PWM

class SpeakerController:
    def __init__(self, pin_num, duty_cycle=512):
        self.speaker = PWM(Pin(pin_num))
        self.duty_cycle = duty_cycle
        self.speaker.duty_u16(0)

    def play_frequency(self, frequency):
        self.speaker.freq(int(frequency))
        self.speaker.duty_u16(self.duty_cycle * 64)

    def stop(self):
        self.speaker.duty_u16(0)