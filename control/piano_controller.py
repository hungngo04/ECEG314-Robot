class PianoController:
    def __init__(self, ultrasound_sensor, led_controller, speaker_controller, note_data):
        self.sensor = ultrasound_sensor
        self.leds = led_controller
        self.speaker = speaker_controller
        self.note_data = note_data

    def find_note_for_distance(self, distance):
        for note in reversed(self.note_data):
            if distance >= note['distance_cm']:
                return note
        return None

    def update(self):
        distance = self.sensor.get_distance()

        if distance == -1:
            self.leds.clear()
            self.speaker.stop()
            return False

        note = self.find_note_for_distance(distance)

        if note:
            self.leds.set_color(note['rgb'])
            self.speaker.play_frequency(note['frequency'])
            print(f"Distance: {distance:.1f}cm - Playing {note['note']} ({note['frequency']}Hz)")
        else:
            self.leds.clear()
            self.speaker.stop()

        return True