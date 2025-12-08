import time
from machine import Pin
from control.line_reader import LineReader
from control.drive import Drive
from control.led_controller import LEDController

class Orienteering:
    def __init__(self):
        self.lr = LineReader()
        self.drive = Drive()
        self.led = LEDController()

    def cleanup(self):
        """Clean up all hardware resources to prevent state persistence"""
        print("Cleaning up hardware...")
        self.drive.cleanup()
        self.lr.cleanup()
        self.led.clear()
        print("Cleanup complete")

    def run(self):
        time.sleep_ms(3000)

        # Station 1 - Search-based return
        print("=== Station 1 Sequence ===")
        self.move_forward_cm(10)
        self.follow_line_to_station(station_number=1, max_line_losses=1)
        self.search_for_line()
        self.follow_line_to_hub()
        print("Station 1 complete - back at hub")

        # Station 3 - Curvy line (allow 1 line loss before station)
        print("=== Station 3 Sequence ===")
        self.move_forward_cm(10)
        self.follow_line_to_station(station_number=3, max_line_losses=2)  # 1st loss = curve, 2nd loss = station
        self.search_for_line()
        self.follow_line_to_hub()

        print("=== Orienteering complete! ===")
        self.drive.drive(0, 0)
        self.cleanup()

    def move_forward_cm(self, distance_cm):
        """Move forward a specific distance in cm"""
        velocity = 10
        time_ms = int((distance_cm / 10) * 1000)

        print(f"Moving forward {distance_cm}cm (velocity={velocity}, time={time_ms}ms)")
        self.drive.drive(velocity, 0)
        time.sleep_ms(time_ms)
        self.drive.drive(0, 0)
        time.sleep_ms(200)

    def follow_line_to_station(self, station_number, max_line_losses=1):
        """Follow line until station reached (allows multiple line losses for curvy paths)"""
        print(f"Following line to station {station_number}")

        # Slalom's line following parameters
        max_velocity = 16
        min_velocity = 6
        max_angular_velocity = 45
        search_angular_velocity = 10

        last_offset = 0.0
        last_time_us = time.ticks_us() - 10000
        Kp = 0.55
        Kd = 0.015

        line_loss_events = 0

        while True:
            current_time_us = time.ticks_us()
            dt_us = time.ticks_diff(current_time_us, last_time_us)
            dt_s = dt_us / 1000000.0
            last_time_us = current_time_us

            error, confidence = self.lr.get_distance()
            darkness, darkness_confidence = self.lr.get_darkness()

            if confidence < 0.2 or darkness < 0.1:
                line_loss_events += 1
                print(f"Line loss event {line_loss_events}/{max_line_losses}")

                if line_loss_events >= max_line_losses:
                    # Station reached!
                    print(f"Station {station_number} colored node reached - line lost")
                    self.drive.drive(0, 0)

                    print(f"Sensor readings - Confidence: {confidence:.3f}, Darkness: {darkness:.3f}")
                    time.sleep_ms(1000)
                    self.led.set_color((0, 255, 0))
                    print("LED on - ready to return")

                    time.sleep_ms(1000)
                    self.led.set_color((0, 0, 0))

                    break
                else:
                    # Temporary loss - search for line
                    print("Searching for line (curve detected)...")
                    # For Station 3, search clockwise (right) first
                    if station_number == 3:
                        search_direction = 1  # Clockwise
                    else:
                        search_direction = -1 if error > 0 else 1

                    # Search for line
                    found = False
                    for _ in range(100):  # Search for up to 100ms
                        self.drive.drive(0, search_direction * search_angular_velocity)
                        time.sleep_ms(1)

                        error, confidence = self.lr.get_distance()
                        darkness, _ = self.lr.get_darkness()

                        if confidence >= 0.3 and darkness >= 0.08:
                            print("Line found! Continuing...")
                            found = True
                            self.drive.drive(0, 0)
                            time.sleep_ms(200)
                            break

                    if not found:
                        print("Warning: Could not find line after search")

                    continue

            derivative = 0
            if dt_s > 0:
                derivative = (error - last_offset) / dt_s

            angular_velocity = (Kp * error) + (Kd * derivative)

            if angular_velocity > max_angular_velocity:
                angular_velocity = max_angular_velocity
            elif angular_velocity < -max_angular_velocity:
                angular_velocity = -max_angular_velocity

            last_offset = error

            adaptive_velocity = min_velocity + (max_velocity - min_velocity) * confidence

            if confidence < 0.25:
                adaptive_velocity *= 0.5

            if darkness < 0.2:
                adaptive_velocity *= 0.7

            error_magnitude = abs(error)
            if error_magnitude > 15:
                adaptive_velocity *= 0.5
            elif error_magnitude > 10:
                adaptive_velocity *= 0.7

            self.drive.drive(adaptive_velocity, angular_velocity)
            time.sleep_ms(1)

    def follow_line_to_hub(self):
        """Follow line back to hub (line lost at colored node)"""
        print("Returning to hub")

        # Slalom's line following parameters
        max_velocity = 16
        min_velocity = 6
        max_angular_velocity = 45

        last_offset = 0.0
        last_time_us = time.ticks_us() - 10000
        Kp = 0.55
        Kd = 0.015

        while True:
            current_time_us = time.ticks_us()
            dt_us = time.ticks_diff(current_time_us, last_time_us)
            dt_s = dt_us / 1000000.0
            last_time_us = current_time_us

            error, confidence = self.lr.get_distance()
            darkness, darkness_confidence = self.lr.get_darkness()

            # Line loss detection - move forward to hub
            # Increased threshold to avoid premature detection
            if confidence < 0.2 or darkness < 0.1:
                print("Line lost - moving forward to hub")
                self.drive.drive(0, 0)
                time.sleep_ms(200)

                # Move forward 8cm to reach hub
                self.drive.drive(10, 0)
                time.sleep_ms(800)  # 8cm at velocity 10
                self.drive.drive(0, 0)
                print("Hub reached!")

                break

            # PD controller
            derivative = 0
            if dt_s > 0:
                derivative = (error - last_offset) / dt_s

            angular_velocity = (Kp * error) + (Kd * derivative)

            # Clamp angular velocity
            if angular_velocity > max_angular_velocity:
                angular_velocity = max_angular_velocity
            elif angular_velocity < -max_angular_velocity:
                angular_velocity = -max_angular_velocity

            last_offset = error

            adaptive_velocity = min_velocity + (max_velocity - min_velocity) * confidence

            if confidence < 0.25:
                adaptive_velocity *= 0.5

            if darkness < 0.2:
                adaptive_velocity *= 0.7

            error_magnitude = abs(error)
            if error_magnitude > 15:
                adaptive_velocity *= 0.5
            elif error_magnitude > 10:
                adaptive_velocity *= 0.7

            self.drive.drive(adaptive_velocity, angular_velocity)
            time.sleep_ms(1)

    def search_for_line(self):
        """Rotate slowly to search for line (from luge.py pattern)"""
        print("Searching for return line...")

        search_angular_velocity = 10
        search_direction = 1

        error, _ = self.lr.get_distance()
        if error < 0:
            search_direction = -1  # Rotate counter-clockwise

        while True:
            error, confidence = self.lr.get_distance()
            darkness, _ = self.lr.get_darkness()

            # Line found!
            if confidence >= 0.2 and darkness >= 0.08:
                print("Return line found!")
                self.drive.drive(0, 0)
                time.sleep_ms(200)

                print("Positioning on line...")
                self.drive.drive(10, 0)
                time.sleep_ms(300)
                self.drive.drive(0, 0)
                time.sleep_ms(200)

                break

            # Keep searching
            self.drive.drive(0, search_direction * search_angular_velocity)
            time.sleep_ms(1)

