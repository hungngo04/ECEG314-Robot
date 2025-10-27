import machine
import math

class RobotDrive:
    def __init__(self, bias=0.0, speed_to_duty_factor=1192, wheelbase=13.0):
        """
        Initialize the robot drive system.
        
        Args:
            bias: Directional bias correction (0 = even, >0 = bias right, <0 = bias left)
            speed_to_duty_factor: Calibration factor to convert cm/s to PWM duty cycle
            wheelbase: Distance between wheels in cm (default 13 cm)
        """

        self.M1A = machine.PWM(machine.Pin(8))
        self.M1B = machine.PWM(machine.Pin(9))

        self.M2A = machine.PWM(machine.Pin(10))
        self.M2B = machine.PWN(machine.Pin(11))

        # Set PWM frequency
        self.M1A.freq(8_000)
        self.M1B.freq(8_000)
        self.M2A.freq(8_000)
        self.M2B.freq(8_000)

        # Initialize motors to stopped state
        self.M1A.duty_u16(0)
        self.M1B.duty_u16(0)
        self.M2A.duty_u16(0)
        self.M2B.duty_u16(0)

        # Calibration params
        self.bias = bias
        self.speed_to_duty_factor = speed_to_duty_factor
        self.wheelbase = wheelbase

        # Bias adjustment to left and right motors
        self.left_bias = 1.0 - bias / 2
        self.right_bias = 1.0 + bias / 2

    def drive(self, speed, omega):
        """
        Drive the robot with specified linear and angular velocities.
        
        Args:
            speed: Linear velocity in cm/s (positive = forward, negative = reverse)
            omega: Angular velocity in rad/s (positive = clockwise, negative = counter-clockwise)
        """

        v_left = speed - (omega * self.wheelbase / 2)
        v_right = speed + (omega * self.wheelbase / 2)

        self.set_motor_speed(v_left, v_right)

    def set_motor_speed(self, v_left, v_right):
        """
        Set individual motor speeds based on wheel velocities.
        
        Args:
            v_left: Left wheel velocity in cm/s
            v_right: Right wheel velocity in cm/s
        """

        v_left_corrected = v_left * self.left_bias
        v_right_corrected = v_right * self.right_bias

        duty_left = int(abs(v_left_corrected) * self.speed_to_duty_factor)
        duty_right = int(abs(v_right_corrected) * self.speed_to_duty_factor)

        # Motor directions and speeds
        if v_left_corrected >= 0:
            self.M1A.duty_u16(duty_left)
            self.M1B.duty_u16(0)
        else:
            self.M1A.duty_u16(0)
            self.M1B.duty_u16(duty_left)

        if v_right_corrected >= 0:
            self.M2B.duty_u16(duty_right)
            self.M2A.duty_u16(0)
        else:
            self.M2B.duty_u16(0)
            self.M2A.duty_u16(duty_right)

    def stop(self):
        """
        Stop all motors
        """

        self.drive(0, 0)

    def set_bias(self, bias):
        """
        Update the directional bias correction.
        
        Args:
            bias: New bias value (0 = even, >0 = bias right, <0 = bias left)
        """

        self.bias = bias
        self.left_bias = 1.0 - bias / 2
        self.right_bias = 1.0 + bias / 2

    def set_speed_calibration(self, speed_to_duty_factor):
        """
        Update the speed to duty cycle calibration factor.
        
        Args:
            speed_to_duty_factor: Factor to convert cm/s to PWM duty cycle
        """

        self.speed_to_duty_factor = speed_to_duty_factor
        