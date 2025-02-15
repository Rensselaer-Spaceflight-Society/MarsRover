from RPi import GPIO
from time import sleep

class StepperMotor:
    def __init__(self, rpm: float, steps_per_rotation: int = 200) -> None:
        self.rpm = rpm
        self.steps_per_rotation = steps_per_rotation
        self.sleep_time = 60 / (steps_per_rotation * rpm)

    def enable(self) -> None:
        pass

    def disable(self) -> None:
        pass

    def rotate_steps(self, steps: int, direction: int) -> None:
        pass

    def rotate_relative(self, angle: float) -> None:
        pass

    def rotate_absolute(self, angle: float) -> None:
        pass

    def home(self) -> None:
        pass

    def get_current_angle(self) -> float:
        pass

    def get_rpm(self) -> float:
        return self.rpm

    def set_rpm(self, rpm: float) -> None:
        self.rpm = rpm
        self.sleep_time = 60 / (self.steps_per_rotation * rpm)


class DRV8825(StepperMotor):
    def __init__(self, step_pin: int, dir_pin: int, rpm: float, steps_per_rotation: int = 200) -> None:
        super().__init__(rpm, steps_per_rotation)
        self.step_pin = step_pin
        self.dir_pin = dir_pin
        self.angle = 0

    def enable(self) -> None:
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.step_pin, GPIO.OUT)
        GPIO.setup(self.dir_pin, GPIO.OUT)

    def disable(self) -> None:
        GPIO.cleanup()

    def rotate_steps(self, steps: int, direction: int) -> None:
        if steps < 0:
            raise ValueError("Steps must be a positive integer")
        
        if direction == 0:
            # Counter-clockwise
            GPIO.output(self.dir_pin, GPIO.LOW)
        else:
            # Clockwise
            GPIO.output(self.dir_pin, GPIO.HIGH)
        
        for _ in range(steps):
            GPIO.output(self.step_pin, GPIO.HIGH)
            sleep(self.sleep_time)
            GPIO.output(self.step_pin, GPIO.LOW)
            sleep(self.sleep_time)

    def rotate_relative(self, angle: float) -> None:
        steps = int(angle / (360 / self.steps_per_rotation))
        self.angle += steps * (360 / self.steps_per_rotation)
        if steps < 0:
            self.rotate_steps(abs(steps), 0)
        else:
            self.rotate_steps(abs(steps), 1)

    def rotate_absolute(self, angle: float) -> None:
        delta_angle = angle - self.angle
        self.rotate_relative(delta_angle)

    def home(self) -> None:
        self.rotate_absolute(0)

    def get_current_angle(self) -> float:
        return self.angle


class ULN2003(StepperMotor):
    def __init__(self, in1_pin: int, in2_pin: int, in3_pin:int, in4_pin:int, rpm: float, steps_per_rotation: int = 2048) -> None:
        super().__init__(rpm, steps_per_rotation)
        self.in1_pin = in1_pin
        self.in2_pin = in2_pin
        self.in3_pin = in3_pin
        self.in4_pin = in4_pin
        self.angle = 0
        self.clockwise_step_sequence = [
            [1, 0, 0, 0],
            [1, 1, 0, 0],
            [0, 1, 0, 0],
            [0, 1, 1, 0],
            [0, 0, 1, 0],
            [0, 0, 1, 1],
            [0, 0, 0, 1],
            [1, 0, 0, 1],
        ]
        self.counter_clockwise_step_sequence = [[1, 0, 0, 1],
            [0, 0, 0, 1],
            [0, 0, 1, 1],
            [0, 0, 1, 0],
            [0, 1, 1, 0],
            [0, 1, 0, 0],
            [1, 1, 0, 0],
            [1, 0, 0, 0],
        ]

    def enable(self) -> None:
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.step_pin, GPIO.OUT)
        GPIO.setup(self.dir_pin, GPIO.OUT)

    def disable(self) -> None:
        GPIO.cleanup()

    def rotate_steps(self, steps: int, direction: int) -> None:
        if steps < 0:
            raise ValueError("Steps must be a positive integer")
        
        if direction == 0:
            for _ in range(steps):
                for step in self.counter_clockwise_step_sequence:
                    GPIO.output(self.in1_pin, step[0])
                    GPIO.output(self.in2_pin, step[1])
                    GPIO.output(self.in3_pin, step[2])
                    GPIO.output(self.in4_pin, step[3])
                    sleep(self.sleep_time)
        else:
            for _ in range(steps):
                for step in self.clockwise_step_sequence:
                    GPIO.output(self.in1_pin, step[0])
                    GPIO.output(self.in2_pin, step[1])
                    GPIO.output(self.in3_pin, step[2])
                    GPIO.output(self.in4_pin, step[3])
                    sleep(self.sleep_time)


    def rotate_relative(self, angle: float) -> None:
        steps = int(angle / (360 / self.steps_per_rotation))
        self.angle += steps * (360 / self.steps_per_rotation)
        if steps < 0:
            self.rotate_steps(abs(steps), 0)
        else:
            self.rotate_steps(abs(steps), 1)

    def rotate_absolute(self, angle: float) -> None:
        delta_angle = angle - self.angle
        self.rotate_relative(delta_angle)

    def home(self) -> None:
        self.rotate_absolute(0)

    def get_current_angle(self) -> float:
        return self.angle
